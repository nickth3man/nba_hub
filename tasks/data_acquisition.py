"""
Prefect tasks for NBA data acquisition.
Wraps existing acquisition scripts as reusable Prefect tasks.
"""

import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from prefect import task
from prefect.logging import get_run_logger


# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "nba_database_documentation" / "scripts"
DB_PATH = PROJECT_ROOT / "nba.duckdb"


@task(
    name="fetch-recent-player-boxscores",
    description="Fetch recent player box scores using nba_api",
    retries=3,
    retry_delay_seconds=300,  # 5 minutes
    tags=["nba-api", "acquisition"]
)
def fetch_recent_player_boxscores(
    season_year: Optional[int] = None,
    db_path: Optional[str] = None
) -> dict:
    """
    Fetch recent player box scores for a specific season using nba_api.

    Args:
        season_year: Season ending year (e.g., 2025 for 2024-25 season).
                    If None, uses current season.
        db_path: Path to DuckDB database. If None, uses default.

    Returns:
        Dictionary with acquisition results including record counts.
    """
    logger = get_run_logger()

    # Determine current season if not specified
    if season_year is None:
        current_date = datetime.now()
        # NBA season runs Oct-June, so if we're in Oct-Dec, use current year + 1
        # Otherwise use current year
        if current_date.month >= 10:
            season_year = current_date.year + 1
        else:
            season_year = current_date.year

    db_path = db_path or str(DB_PATH)
    script_path = SCRIPTS_DIR / "acquire_recent_nbaapi.py"

    logger.info(f"Fetching player box scores for {season_year-1}-{str(season_year)[-2:]} season")
    logger.info(f"Using database: {db_path}")
    logger.info(f"Script: {script_path}")

    # Check if script exists
    if not script_path.exists():
        logger.error(f"Acquisition script not found: {script_path}")
        raise FileNotFoundError(f"Script not found: {script_path}")

    # Run acquisition script
    cmd = [
        sys.executable,
        str(script_path),
        "--season", str(season_year),
        "--db-path", db_path
    ]

    logger.info(f"Running command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=str(PROJECT_ROOT)
        )

        logger.info("Acquisition completed successfully")
        logger.info(f"STDOUT: {result.stdout}")

        if result.stderr:
            logger.warning(f"STDERR: {result.stderr}")

        return {
            "status": "success",
            "season_year": season_year,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.CalledProcessError as e:
        logger.error(f"Acquisition failed with exit code {e.returncode}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        raise


@task(
    name="fetch-advanced-metrics",
    description="Scrape advanced metrics from Basketball Reference",
    retries=2,
    retry_delay_seconds=600,  # 10 minutes
    tags=["basketball-reference", "advanced-stats"]
)
def fetch_advanced_metrics(
    season_year: Optional[int] = None,
    db_path: Optional[str] = None
) -> dict:
    """
    Scrape advanced metrics for a specific season from Basketball Reference.

    Args:
        season_year: Season ending year (e.g., 2025 for 2024-25 season).
                    If None, uses current season.
        db_path: Path to DuckDB database. If None, uses default.

    Returns:
        Dictionary with scraping results.
    """
    logger = get_run_logger()

    # Determine current season if not specified
    if season_year is None:
        current_date = datetime.now()
        if current_date.month >= 10:
            season_year = current_date.year + 1
        else:
            season_year = current_date.year

    db_path = db_path or str(DB_PATH)

    logger.info(f"Fetching advanced metrics for {season_year-1}-{str(season_year)[-2:]} season")
    logger.warning("Advanced metrics script not yet implemented")
    logger.info("This would scrape Basketball Reference for advanced stats")

    # TODO: Implement advanced metrics acquisition
    # This would involve web scraping Basketball Reference or using an API
    # For now, return a placeholder

    return {
        "status": "not_implemented",
        "season_year": season_year,
        "message": "Advanced metrics acquisition not yet implemented"
    }


@task(
    name="check-nba-season-active",
    description="Check if NBA season is currently active",
    cache_key_fn=lambda *args, **kwargs: datetime.now().strftime("%Y-%m-%d"),
    cache_expiration=timedelta(hours=24),
    tags=["validation"]
)
def check_nba_season_active() -> bool:
    """
    Check if the NBA season is currently active.
    Season typically runs October through June.

    Returns:
        True if season is active, False otherwise.
    """
    logger = get_run_logger()
    current_date = datetime.now()
    month = current_date.month

    # NBA season months: October (10) through June (6)
    is_active = month >= 10 or month <= 6

    logger.info(f"Current month: {month}")
    logger.info(f"NBA season active: {is_active}")

    return is_active


@task(
    name="get-yesterday-date",
    description="Get yesterday's date for incremental updates",
    tags=["utility"]
)
def get_yesterday_date() -> str:
    """
    Get yesterday's date in YYYY-MM-DD format.

    Returns:
        Yesterday's date as string.
    """
    logger = get_run_logger()
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")
    logger.info(f"Yesterday's date: {date_str}")
    return date_str


@task(
    name="historical-backfill-decade",
    description="Backfill historical data for a decade",
    timeout_seconds=18000,  # 5 hours
    retries=1,
    tags=["historical", "backfill"]
)
def historical_backfill_decade(
    start_year: int,
    end_year: int,
    db_path: Optional[str] = None
) -> dict:
    """
    Backfill historical player box scores for a range of years.

    Args:
        start_year: First season ending year to acquire.
        end_year: Last season ending year to acquire.
        db_path: Path to DuckDB database. If None, uses default.

    Returns:
        Dictionary with backfill results.
    """
    logger = get_run_logger()

    db_path = db_path or str(DB_PATH)
    script_path = SCRIPTS_DIR / "acquire_historical_player_boxscores.py"

    logger.info(f"Starting historical backfill for {start_year}-{end_year}")
    logger.info(f"Database: {db_path}")

    if not script_path.exists():
        logger.warning(f"Historical acquisition script not found: {script_path}")
        logger.info("Using recent acquisition script as fallback")
        script_path = SCRIPTS_DIR / "acquire_recent_player_boxscores.py"

    results = []

    for year in range(start_year, end_year + 1):
        logger.info(f"Acquiring season {year-1}-{str(year)[-2:]}")

        cmd = [
            sys.executable,
            str(script_path),
            "--season", str(year),
            "--db-path", db_path
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=str(PROJECT_ROOT)
            )

            logger.info(f"Season {year} completed successfully")
            results.append({
                "year": year,
                "status": "success",
                "stdout": result.stdout[:500]  # Truncate for logging
            })

        except subprocess.CalledProcessError as e:
            logger.error(f"Season {year} failed: {e}")
            results.append({
                "year": year,
                "status": "failed",
                "error": str(e)
            })
            # Continue with next year even if one fails
            continue

    successful = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - successful

    logger.info(f"Backfill complete: {successful} successful, {failed} failed")

    return {
        "start_year": start_year,
        "end_year": end_year,
        "total_seasons": len(results),
        "successful": successful,
        "failed": failed,
        "results": results
    }
