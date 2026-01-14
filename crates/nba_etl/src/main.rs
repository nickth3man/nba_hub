mod convex;
mod seed;
mod backfill;
mod validation;
mod csv_utils;

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
    Seed(seed::Args),
    Backfill(BackfillArgs),
    Validate {
        #[arg(long, default_value = "data/nba.duckdb")]
        db_path: String,
        #[arg(long, default_value = "data/raw")]
        csv_dir: String,
    },
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    dotenv().ok();
    env_logger::init();
    
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Seed(args) => {
            info!("Starting CSV seed...");
            if let Err(e) = seed::run_seed(args).await {
                error!("Seed failed: {}", e);
                std::process::exit(1);
            }
        }
        Commands::Backfill(args) => {
            info!("Starting NBA ETL Backfill...");
            if let Err(e) = backfill::run_backfill(args).await {
                error!("Backfill failed: {}", e);
                std::process::exit(1);
            }
        }
        Commands::Validate { db_path, csv_dir } => {
            info!("Starting Validation...");
            // Validation is synchronous (DuckDB)
            if let Err(e) = tokio::task::spawn_blocking(move || {
                validation::run_validations(&db_path, &csv_dir)
            }).await? {
                error!("Validation failed: {}", e);
                std::process::exit(1);
            }
        }
    }
    
    info!("Job Complete");
    Ok(())
}
