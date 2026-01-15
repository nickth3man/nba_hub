use scraper::{Html, Selector};
use anyhow::Result;
use crate::ScraperClient;
use nba_core::schema::{Referee, Coach};
use regex::Regex;

pub async fn scrape_games_for_date(client: &ScraperClient, date: &str) -> Result<Vec<String>> {
    let year = &date[0..4];
    let month = &date[4..6];
    let day = &date[6..8];
    
    let url = format!("https://www.basketball-reference.com/boxscores/?month={}&day={}&year={}", month, day, year);
    let html_content = client.get(&url).await?;
    
    let document = Html::parse_document(&html_content);
    let summary_selector = Selector::parse("div.game_summary").unwrap();
    let link_selector = Selector::parse("a[href*='boxscores']").unwrap();
    
    let mut game_links = Vec::new();
    
    for summary in document.select(&summary_selector) {
        for link in summary.select(&link_selector) {
            if link.text().collect::<Vec<_>>().join("").trim() == "Final" {
                if let Some(href) = link.value().attr("href") {
                    game_links.push(format!("https://www.basketball-reference.com{}", href));
                }
            }
        }
    }
    
    Ok(game_links)
}

pub struct BoxscoreMeta {
    pub referees: Vec<Referee>,
    pub coaches: Vec<Coach>,
}

pub async fn scrape_boxscore(client: &ScraperClient, url: &str) -> Result<BoxscoreMeta> {
    let html_content = client.get(url).await?;
    let document = Html::parse_document(&html_content);
    
    // Parse Referees
    let mut referees = Vec::new();
    // Using regex for officials block to match Python logic
    let officials_regex = Regex::new(r#"Officials:.*?(<a.*?/referees/.*?</a>.*?)</div>"#).unwrap();
    let link_regex = Regex::new(r#"href="(/referees/(.*?)\.html)">(.*?)</a>"#).unwrap();
    
    if let Some(cap) = officials_regex.captures(&html_content) {
        let officials_block = &cap[1];
        for link_cap in link_regex.captures_iter(officials_block) {
            let ref_id = link_cap[2].to_string();
            let display_name = link_cap[3].to_string();
            referees.push(Referee {
                referee_id: ref_id,
                nba_api_ref_id: None,
                display_name,
            });
        }
    }

    // Parse Coaches
    let mut coaches = Vec::new();
    let coach_link_selector = Selector::parse("a[href*='/coaches/']").unwrap();
    
    for element in document.select(&coach_link_selector) {
        if let Some(href) = element.value().attr("href") {
            let coach_id = href.split('/').last().unwrap().replace(".html", "");
            let display_name = element.text().collect::<Vec<_>>().join("");
            
            // Avoid "Coaches" header link if it exists
            if !href.ends_with("NBA_stats.html") {
                 coaches.push(Coach {
                    coach_id,
                    nba_api_coach_id: None,
                    display_name,
                });
            }
        }
    }

    Ok(BoxscoreMeta { referees, coaches })
}
