use clap::Parser;
use nba_scraper::{ScraperClient, sites::basketball_reference::{scrape_games_for_date, scrape_boxscore}};
use crate::convex::ConvexClient;
use log::{info, warn};

#[derive(Parser, Debug)]
#[command(name = "nba-etl")]
#[command(about = "NBA Hub ETL Tool")]
pub struct Args {
    #[arg(short, long)]
    pub date: Option<String>,
    
    #[arg(long)]
    pub backfill: bool,
    
    #[arg(long, default_value_t = 1)]
    pub concurrency: usize,
    
    #[arg(long, default_value_t = 3000)]
    pub delay_ms: u64,
}

pub async fn run_backfill(args: Args) -> anyhow::Result<()> {
    info!("Starting backfill...");
    
    let convex = ConvexClient::new()?;
    let scraper = ScraperClient::new(args.concurrency, args.delay_ms);
    
    // Initialize reference data
    info!("Initializing reference data...");
    init_reference_data(&convex).await?;
    
    if let Some(date_str) = args.date {
        info!("Backfilling single date: {}", date_str);
        backfill_date(&scraper, &convex, &date_str).await?;
    } else if args.backfill {
        info!("Running full backfill (not implemented yet - requires date range config)");
        warn!("Full backfill requires implementing date iteration. For now, use --date YYYYMMDD");
    } else {
        warn!("Please specify --date YYYYMMDD for single date or --backfill for full run");
    }
    
    Ok(())
}

async fn init_reference_data(convex: &ConvexClient) -> anyhow::Result<()> {
    // Initialize Leagues
    let leagues = vec![
        serde_json::json!({"league_id": 1, "league_code": "NBA", "league_name": "National Basketball Association"}),
        serde_json::json!({"league_id": 2, "league_code": "BAA", "league_name": "Basketball Association of America"}),
        serde_json::json!({"league_id": 3, "league_code": "ABA", "league_name": "American Basketball Association"}),
    ];
    
    for league in &leagues {
        match convex.mutation("leagues:insert", league).await {
            Ok(_) => info!("Inserted league"),
            Err(e) => warn!("Failed to insert league: {}", e),
        }
    }
    
    // Initialize Seasons
    let mut seasons = Vec::new();
    for year in 1946..=2026 {
        let league_id = if year < 1949 { 2 } else { 1 }; // BAA before 1949
        let season_id = (year - 1946 + 1) as i32;
        seasons.push(serde_json::json!({
            "season_id": season_id,
            "league_id": league_id,
            "season_year": year,
        }));
    }
    
    info!("Initializing {} seasons", seasons.len());
    // Batch insert would be better, but for now, loop
    for season in seasons.iter().take(5) { // Insert first 5 for testing
        match convex.mutation("seasons:insert", season).await {
            Ok(_) => {},
            Err(e) => warn!("Failed to insert season: {}", e),
        }
    }
    
    Ok(())
}

async fn backfill_date(scraper: &ScraperClient, convex: &ConvexClient, date: &str) -> anyhow::Result<()> {
    info!("Fetching games for {}", date);
    
    let game_links = scrape_games_for_date(scraper, date).await?;
    info!("Found {} game links", game_links.len());
    
    for game_url in &game_links {
        info!("Processing: {}", game_url);
        match scrape_boxscore(scraper, game_url).await {
            Ok(meta) => {
                // Insert referees
                for referee in &meta.referees {
                    let ref_data = serde_json::json!({
                        "referee_id": &referee.referee_id,
                        "display_name": &referee.display_name,
                    });
                    match convex.mutation("referees:insert", &ref_data).await {
                        Ok(_) => info!("Inserted referee: {}", referee.display_name),
                        Err(e) => warn!("Failed to insert referee: {}", e),
                    }
                }
                
                // Insert coaches
                for coach in &meta.coaches {
                    let coach_data = serde_json::json!({
                        "coach_id": &coach.coach_id,
                        "display_name": &coach.display_name,
                    });
                    match convex.mutation("coaches:insert", &coach_data).await {
                        Ok(_) => info!("Inserted coach: {}", coach.display_name),
                        Err(e) => warn!("Failed to insert coach: {}", e),
                    }
                }
            }
            Err(e) => {
                warn!("Failed to scrape boxscore {}: {}", game_url, e);
            }
        }
    }
    
    Ok(())
}
