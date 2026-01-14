use anyhow::Result;
use scraper::{Html, Selector};

use crate::ScraperClient;
use nba_core::schema::{Coach, Referee};

pub async fn scrape_coaches(client: &ScraperClient) -> Result<Vec<Coach>> {
    let url = "https://www.basketball-reference.com/coaches/NBA_stats.html";
    let html_content = client.get(url).await?;
    let document = Html::parse_document(&html_content);

    let row_selector = Selector::parse("table#coaches tbody tr").unwrap();
    let coach_selector = Selector::parse("td[data-stat='coach'] a")
        .map_err(|err| anyhow::anyhow!("Failed to build coach selector: {:?}", err))?;

    let mut coaches = Vec::new();
    for row in document.select(&row_selector) {
        if row
            .value()
            .has_class("thead", scraper::CaseSensitivity::AsciiCaseInsensitive)
        {
            continue;
        }

        if let Some(link) = row.select(&coach_selector).next() {
            let display_name = link.text().collect::<String>().trim().to_string();
            let coach_id = link
                .value()
                .attr("href")
                .and_then(|href| href.split('/').last())
                .map(|slug| slug.replace(".html", ""))
                .unwrap_or_default();

            if !coach_id.is_empty() && !display_name.is_empty() {
                coaches.push(Coach {
                    coach_id,
                    nba_api_coach_id: None,
                    display_name,
                });
            }
        }
    }

    Ok(coaches)
}

pub async fn scrape_referees(client: &ScraperClient) -> Result<Vec<Referee>> {
    let url = "https://www.basketball-reference.com/referees/";
    let html_content = client.get(url).await?;
    let document = Html::parse_document(&html_content);

    let row_selector = Selector::parse("table#referees tbody tr").unwrap();
    let ref_selector = Selector::parse("td[data-stat='referee'] a")
        .map_err(|err| anyhow::anyhow!("Failed to build referee selector: {:?}", err))?;

    let mut referees = Vec::new();
    for row in document.select(&row_selector) {
        if row
            .value()
            .has_class("thead", scraper::CaseSensitivity::AsciiCaseInsensitive)
        {
            continue;
        }

        if let Some(link) = row.select(&ref_selector).next() {
            let display_name = link.text().collect::<String>().trim().to_string();
            let referee_id = link
                .value()
                .attr("href")
                .and_then(|href| href.split('/').last())
                .map(|slug| slug.replace(".html", ""))
                .unwrap_or_default();

            if !referee_id.is_empty() && !display_name.is_empty() {
                referees.push(Referee {
                    referee_id,
                    nba_api_ref_id: None,
                    display_name,
                });
            }
        }
    }

    Ok(referees)
}
