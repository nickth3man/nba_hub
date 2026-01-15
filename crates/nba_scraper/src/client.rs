use anyhow::{Context, Result};
use log::{info, warn};
use robotstxt::DefaultMatcher;
use std::collections::HashMap;
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::sync::{Mutex, Semaphore};
use tokio::time::sleep;
use url::Url;

pub struct ScraperClient {
    client: reqwest::Client,
    semaphore: Arc<Semaphore>,
    default_delay: Duration,
    user_agent: String,
    robots_cache: Arc<Mutex<HashMap<String, RobotsRules>>>,
    host_locks: Arc<Mutex<HashMap<String, Arc<Mutex<()>>>>>,
    last_request: Arc<Mutex<HashMap<String, Instant>>>,
    max_retries: usize,
}

#[derive(Clone)]
struct RobotsRules {
    allowed: bool,
    crawl_delay: Option<Duration>,
}

impl ScraperClient {
    pub fn new(concurrency: usize, delay_ms: u64) -> Self {
        let user_agent = std::env::var("SCRAPER_USER_AGENT")
            .unwrap_or_else(|_| "NBA Hub Scraper (nba-hub-bot)".to_string());
        let client = reqwest::Client::builder()
            .user_agent(user_agent.clone())
            .build()
            .expect("Failed to build HTTP client");

        Self {
            client,
            semaphore: Arc::new(Semaphore::new(concurrency)),
            default_delay: Duration::from_millis(delay_ms),
            user_agent,
            robots_cache: Arc::new(Mutex::new(HashMap::new())),
            host_locks: Arc::new(Mutex::new(HashMap::new())),
            last_request: Arc::new(Mutex::new(HashMap::new())),
            max_retries: 3,
        }
    }

    pub async fn get(&self, url: &str) -> Result<String> {
        let _permit = self
            .semaphore
            .acquire()
            .await
            .context("Failed to acquire semaphore")?;

        let parsed = Url::parse(url).context("Invalid URL")?;
        let host = parsed.host_str().context("URL missing host")?.to_string();

        let host_lock = self.host_lock(&host).await;
        let _guard = host_lock.lock().await;

        let rules = self.robots_rules(&parsed).await?;
        if !rules.allowed {
            return Err(anyhow::anyhow!("Blocked by robots.txt: {}", url));
        }

        self.enforce_delay(&host, rules.crawl_delay).await;

        let mut attempt = 0;
        loop {
            attempt += 1;
            info!("Fetching {}", url);
            let response = self.client.get(url).send().await;
            match response {
                Ok(resp) if resp.status().is_success() => {
                    let text = resp
                        .text()
                        .await
                        .context("Failed to read response text")?;
                    return Ok(text);
                }
                Ok(resp) => {
                    let status = resp.status();
                    warn!("Failed to fetch {}: {}", url, status);
                    if attempt >= self.max_retries {
                        return Err(anyhow::anyhow!("HTTP request failed: {}", status));
                    }
                }
                Err(err) => {
                    warn!("Request error on {}: {}", url, err);
                    if attempt >= self.max_retries {
                        return Err(anyhow::anyhow!("HTTP request failed: {}", err));
                    }
                }
            }

            let backoff = Duration::from_millis(500 * attempt as u64);
            sleep(backoff).await;
        }
    }

    async fn host_lock(&self, host: &str) -> Arc<Mutex<()>> {
        let mut locks = self.host_locks.lock().await;
        locks
            .entry(host.to_string())
            .or_insert_with(|| Arc::new(Mutex::new(())))
            .clone()
    }

    async fn enforce_delay(&self, host: &str, override_delay: Option<Duration>) {
        let delay = override_delay.unwrap_or(self.default_delay);
        let mut last_request = self.last_request.lock().await;
        if let Some(previous) = last_request.get(host) {
            let elapsed = previous.elapsed();
            if elapsed < delay {
                sleep(delay - elapsed).await;
            }
        }
        last_request.insert(host.to_string(), Instant::now());
    }

    async fn robots_rules(&self, url: &Url) -> Result<RobotsRules> {
        let host = url
            .host_str()
            .context("URL missing host")?
            .to_string();
        {
            let cache = self.robots_cache.lock().await;
            if let Some(rules) = cache.get(&host) {
                return Ok(rules.clone());
            }
        }

        let robots_url = format!("{}://{}/robots.txt", url.scheme(), host);
        let body = match self.client.get(&robots_url).send().await {
            Ok(resp) if resp.status().is_success() => resp.text().await.unwrap_or_default(),
            _ => String::new(),
        };

        let mut matcher = DefaultMatcher::default();
        let allowed = matcher.one_agent_allowed_by_robots(&body, &self.user_agent, url.as_str());
        let crawl_delay = parse_crawl_delay(&body, &self.user_agent);

        let rules = RobotsRules {
            allowed,
            crawl_delay,
        };

        let mut cache = self.robots_cache.lock().await;
        cache.insert(host, rules.clone());
        Ok(rules)
    }
}

fn parse_crawl_delay(body: &str, user_agent: &str) -> Option<Duration> {
    #[derive(Default)]
    struct Group {
        agents: Vec<String>,
        crawl_delay: Option<Duration>,
    }

    let mut groups: Vec<Group> = Vec::new();
    let mut current = Group::default();
    let mut saw_directive = false;

    for line in body.lines() {
        let trimmed = line.split('#').next().unwrap_or("").trim();
        if trimmed.is_empty() {
            if !current.agents.is_empty() || saw_directive {
                groups.push(current);
                current = Group::default();
                saw_directive = false;
            }
            continue;
        }

        let parts: Vec<&str> = trimmed.splitn(2, ':').collect();
        if parts.len() != 2 {
            continue;
        }
        let field = parts[0].trim().to_lowercase();
        let value = parts[1].trim();

        if field == "user-agent" {
            if saw_directive {
                groups.push(current);
                current = Group::default();
                saw_directive = false;
            }
            current.agents.push(value.to_lowercase());
            continue;
        }

        saw_directive = true;
        if field == "crawl-delay" {
            if let Ok(delay) = value.parse::<f64>() {
                if delay >= 0.0 {
                    current.crawl_delay = Some(Duration::from_millis((delay * 1000.0) as u64));
                }
            }
        }
    }

    if !current.agents.is_empty() || saw_directive {
        groups.push(current);
    }

    let user_agent_lc = user_agent.to_lowercase();
    let mut wildcard_delay = None;
    for group in groups {
        if group.agents.iter().any(|a| a == &user_agent_lc) {
            return group.crawl_delay;
        }
        if group.agents.iter().any(|a| a == "*") {
            wildcard_delay = group.crawl_delay;
        }
    }

    wildcard_delay
}
