use anyhow::Result;
use log::warn;
use scraper::{Html, Selector};

use crate::ScraperClient;
use nba_core::awards::build_award_key;
use nba_core::schema::Award;

const AWARD_TABLES: [(&str, &str); 5] = [
    ("mvp", "MVP"),
    ("roy", "ROY"),
    ("dpoy", "DPOY"),
    ("smoy", "SMOY"),
    ("mip", "MIP"),
];

pub async fn scrape_awards_for_year(
    client: &ScraperClient,
    year: i32,
) -> Result<Vec<Award>> {
    let url = format!("https://www.basketball-reference.com/awards/awards_{year}.html");
    let html_content = client.get(&url).await?;
    let document = Html::parse_document(&html_content);

    let mut awards = Vec::new();
    for (table_id, award_type) in AWARD_TABLES {
        let selector = Selector::parse(&format!("table#{table_id} tbody tr"))
            .map_err(|err| anyhow::anyhow!("Failed to build selector: {:?}", err))?;
        let rank_selector = Selector::parse("th[data-stat='rank']").unwrap();
        let player_selector = Selector::parse("td[data-stat='player']").unwrap();
        let first_selector = Selector::parse("td[data-stat='votes_first']").unwrap();
        let points_selector = Selector::parse("td[data-stat='points_won']").unwrap();
        let max_selector = Selector::parse("td[data-stat='points_max']").unwrap();
        let share_selector = Selector::parse("td[data-stat='award_share']").unwrap();

        for row in document.select(&selector) {
            if row
                .value()
                .has_class("thead", scraper::CaseSensitivity::AsciiCaseInsensitive)
            {
                continue;
            }

            let rank_text = row
                .select(&rank_selector)
                .next()
                .map(|node| node.text().collect::<String>().trim().to_string())
                .unwrap_or_default();
            if rank_text.is_empty() {
                continue;
            }

            let rank = rank_text
                .replace('T', "")
                .parse::<i32>()
                .ok();

            let player_cell = match row.select(&player_selector).next() {
                Some(cell) => cell,
                None => continue,
            };
            let player_name = player_cell.text().collect::<String>().trim().to_string();
            let player_bref_id = player_cell
                .value()
                .attr("data-append-csv")
                .map(|val| val.to_string())
                .or_else(|| {
                    player_cell
                        .select(&Selector::parse("a").unwrap())
                        .next()
                        .and_then(|link| link.value().attr("href"))
                        .and_then(|href| href.split('/').last())
                        .map(|slug| slug.replace(".html", ""))
                });

            let player_name = if player_name.is_empty() {
                None
            } else {
                Some(player_name)
            };
            let award_key = match build_award_key(
                award_type,
                year,
                player_bref_id.as_deref(),
                player_name.as_deref(),
            ) {
                Some(key) => key,
                None => {
                    warn!("Skipping award row with missing player identifier for {award_type} {year}");
                    continue;
                }
            };

            let _first_place = parse_int_cell(&row, &first_selector);
            let points_won = parse_int_cell(&row, &points_selector);
            let points_max = parse_int_cell(&row, &max_selector);
            let share = parse_float_cell(&row, &share_selector);

            awards.push(Award {
                award_key,
                award_type: award_type.to_string(),
                season_year: year,
                player_bref_id,
                player_name,
                team_abbrev: None,
                rank,
                points_won,
                points_max,
                share,
            });
        }
    }

    Ok(awards)
}

fn parse_int_cell(row: &scraper::ElementRef, selector: &Selector) -> Option<i32> {
    row.select(selector)
        .next()
        .and_then(|node| node.text().collect::<String>().trim().parse::<f64>().ok())
        .map(|val| val as i32)
}

fn parse_float_cell(row: &scraper::ElementRef, selector: &Selector) -> Option<f64> {
    row.select(selector)
        .next()
        .and_then(|node| node.text().collect::<String>().trim().parse::<f64>().ok())
}
