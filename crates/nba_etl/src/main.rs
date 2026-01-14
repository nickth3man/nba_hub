mod convex;
mod backfill;
mod validation;

use dotenv::dotenv;
use log::{info, error};
use clap::{Parser, Subcommand};
use backfill::Args as BackfillArgs;

#[derive(Parser)]
#[command(name = "nba-etl")]
#[command(about = "NBA Hub ETL Tool")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Backfill(BackfillArgs),
    Validate {
        #[arg(long, default_value = "data/nba.duckdb")]
        db_path: String,
    },
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    dotenv().ok();
    env_logger::init();
    
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Backfill(args) => {
            info!("Starting NBA ETL Backfill...");
            if let Err(e) = backfill::run_backfill(args).await {
                error!("Backfill failed: {}", e);
                std::process::exit(1);
            }
        }
        Commands::Validate { db_path } => {
            info!("Starting Validation...");
            // Validation is synchronous (DuckDB)
            if let Err(e) = tokio::task::spawn_blocking(move || {
                validation::validate_team_totals(&db_path)
            }).await? {
                error!("Validation failed: {}", e);
                std::process::exit(1);
            }
        }
    }
    
    info!("Job Complete");
    Ok(())
}
