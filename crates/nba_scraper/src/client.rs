use std::sync::Arc;
use std::time::Duration;
use reqwest::Client;
use tokio::sync::Semaphore;
use tokio::time::sleep;
use anyhow::{Result, Context};
use log::{info, warn};

pub struct ScraperClient {
    client: Client,
    semaphore: Arc<Semaphore>,
    delay: Duration,
}

impl ScraperClient {
    pub fn new(concurrency: usize, delay_ms: u64) -> Self {
        let client = Client::builder()
            .user_agent("NBA Hub Scraper (nba-hub-bot)")
            .build()
            .expect("Failed to build HTTP client");

        Self {
            client,
            semaphore: Arc::new(Semaphore::new(concurrency)),
            delay: Duration::from_millis(delay_ms),
        }
    }

    pub async fn get(&self, url: &str) -> Result<String> {
        let _permit = self.semaphore.acquire().await.context("Failed to acquire semaphore")?;
        
        info!("Fetching {}", url);
        let response = self.client.get(url).send().await.context("Failed to send request")?;
        
        if !response.status().is_success() {
            warn!("Failed to fetch {}: {}", url, response.status());
            return Err(anyhow::anyhow!("HTTP request failed: {}", response.status()));
        }

        let text = response.text().await.context("Failed to read response text")?;
        
        sleep(self.delay).await;
        
        Ok(text)
    }
}
