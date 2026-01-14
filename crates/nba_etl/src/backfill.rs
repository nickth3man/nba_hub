use anyhow::{Context, Result};
use clap::Parser;
use chrono::{Duration, NaiveDate};
use log::{info, warn};
use std::collections::HashMap;

use nba_scraper::ScraperClient;
use nba_scraper::sites::basketball_reference::{scrape_games_for_date, scrape_boxscore};
use nba_scraper::sites::awards::scrape_awards_for_year;
use nba_scraper::sites::personnel::{scrape_coaches, scrape_referees};

use nba_core::schema::{Coach, Referee, Award};
use crate::convex::{ConvexClient, ConvexError};

#[derive(Parser, Debug)]
#[command(name = "nba-etl")]
#[command(about = "NBA Hub ETL Tool")]
pub struct Args {
    #[arg(short, long)]
    pub date: Option<String>,

    #[arg(long)]
    pub start_date: Option<String>,

    #[arg(long)]
    pub end_date: Option<String>,

    #[arg(long, default_value_t = 1)]
    pub concurrency: usize,

    #[arg(long, default_value_t = 3000)]
    pub delay_ms: u64,

    #[arg(long)]
    pub awards_start: Option<i32>,

    #[arg(long)]
    pub awards_end: Option<i32>,

    #[arg(long)]
    pub skip_awards: bool,

    #[arg(long)]
    pub skip_personnel: bool,
}

pub async fn run_backfill(args: Args) -> Result<()> {
    info!("Starting backfill...");

    let convex = ConvexClient::new()?;
    let scraper = ScraperClient::new(args.concurrency, args.delay_ms);

    if !args.skip_personnel {
        ingest_personnel(&scraper, &convex).await?;
    }

    if !args.skip_awards {
        ingest_awards(&scraper, &convex, args.awards_start, args.awards_end).await?;
    }

    ingest_game_metadata(&scraper, &convex, args).await?;
    Ok(())
}

async fn ingest_personnel(scraper: &ScraperClient, convex: &ConvexClient) -> Result<()> {
    info!("Scraping coaches and referees...");
    let coaches = scrape_coaches(scraper).await?;
    let referees = scrape_referees(scraper).await?;

    send_batches(convex, "ingest:upsertCoaches", "coaches", coaches, 200).await?;
    send_batches(convex, "ingest:upsertReferees", "referees", referees, 200).await?;
    Ok(())
}

async fn ingest_awards(
    scraper: &ScraperClient,
    convex: &ConvexClient,
    start_year: Option<i32>,
    end_year: Option<i32>,
) -> Result<()> {
    let start = start_year.unwrap_or(1956);
    let end = end_year.unwrap_or(2026);
    info!("Scraping awards for {}-{}", start, end);

    let mut awards: Vec<Award> = Vec::new();
    for year in start..=end {
        match scrape_awards_for_year(scraper, year).await {
            Ok(mut rows) => awards.append(&mut rows),
            Err(err) => warn!("Award scrape failed for {}: {}", year, err),
        }
    }

    send_batches(convex, "ingest:upsertAwards", "awards", awards, 200).await?;
    Ok(())
}

async fn ingest_game_metadata(
    scraper: &ScraperClient,
    convex: &ConvexClient,
    args: Args,
) -> Result<()> {
    let dates = collect_dates(args.date, args.start_date, args.end_date)?;
    if dates.is_empty() {
        warn!("No dates provided; skipping game metadata backfill.");
        return Ok(());
    }

    for date in dates {
        info!("Fetching games for {}", date);
        let game_links = scrape_games_for_date(scraper, &date).await?;
        info!("Found {} games on {}", game_links.len(), date);

        let mut coach_map: HashMap<String, Coach> = HashMap::new();
        let mut referee_map: HashMap<String, Referee> = HashMap::new();

        for game_url in &game_links {
            match scrape_boxscore(scraper, game_url).await {
                Ok(meta) => {
                    for coach in meta.coaches {
                        coach_map.entry(coach.coach_id.clone()).or_insert(coach);
                    }
                    for referee in meta.referees {
                        referee_map
                            .entry(referee.referee_id.clone())
                            .or_insert(referee);
                    }
                }
                Err(err) => warn!("Failed to scrape {}: {}", game_url, err),
            }
        }

        send_batches(
            convex,
            "ingest:upsertCoaches",
            "coaches",
            coach_map.into_values().collect(),
            200,
        )
        .await?;
        send_batches(
            convex,
            "ingest:upsertReferees",
            "referees",
            referee_map.into_values().collect(),
            200,
        )
        .await?;
    }

    Ok(())
}

fn collect_dates(
    single_date: Option<String>,
    start_date: Option<String>,
    end_date: Option<String>,
) -> Result<Vec<String>> {
    if let Some(date) = single_date {
        return Ok(vec![date]);
    }

    let start = match start_date {
        Some(date) => parse_date(&date)?,
        None => return Ok(Vec::new()),
    };
    let end = match end_date {
        Some(date) => parse_date(&date)?,
        None => return Ok(Vec::new()),
    };

    if end < start {
        return Err(anyhow::anyhow!("end_date must be >= start_date"));
    }

    let mut dates = Vec::new();
    let mut current = start;
    while current <= end {
        dates.push(current.format("%Y%m%d").to_string());
        current += Duration::days(1);
    }

    Ok(dates)
}

fn parse_date(value: &str) -> Result<NaiveDate> {
    NaiveDate::parse_from_str(value, "%Y%m%d")
        .with_context(|| format!("Invalid date format: {}", value))
}

async fn send_batches<T: serde::Serialize>(
    convex: &ConvexClient,
    function: &str,
    key: &str,
    items: Vec<T>,
    batch_size: usize,
) -> Result<()> {
    if items.is_empty() {
        return Ok(());
    }

    let mut start = 0;
    let mut current_batch_size = batch_size.max(1);
    while start < items.len() {
        let mut end = (start + current_batch_size).min(items.len());
        loop {
            let slice = &items[start..end];
            let payload = serde_json::json!({ key: slice });
            match convex.mutation(function, &payload).await {
                Ok(_) => {
                    info!("Inserted {} items into {}", slice.len(), function);
                    start = end;
                    break;
                }
                Err(err) => {
                    let should_shrink = err
                        .downcast_ref::<ConvexError>()
                        .map(|convex_err| convex_err.is_payload_limit())
                        .unwrap_or(false);
                    if should_shrink && current_batch_size > 1 {
                        let next_size = (current_batch_size / 2).max(1);
                        warn!(
                            "Batch too large for {} ({} items). Retrying with {}",
                            function,
                            current_batch_size,
                            next_size
                        );
                        current_batch_size = next_size;
                        end = (start + current_batch_size).min(items.len());
                        continue;
                    }
                    return Err(err);
                }
            }
        }
    }
    Ok(())
}
