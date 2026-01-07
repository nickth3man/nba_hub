"""
Weekly Advanced Metrics Update Flow

Purpose: Scrape latest advanced metrics for current season
Schedule: Sundays at 8 AM
Features:
  - Calls advanced metrics scraper for current season
  - Updates player_season_advanced_stats table
  - Includes retry logic for web scraping failures
"""

from datetime import datetime
from prefect import flow, get_run_logger

# Import tasks
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tasks.data_acquisition import fetch_advanced_metrics, check_nba_season_active


@flow(
    name="update-advanced-metrics",
    description="Weekly update of advanced metrics from Basketball Reference",
    retries=1,
    retry_delay_seconds=1800,  # 30 minutes
    log_prints=True
)
def update_advanced_metrics(season_year: int = None, force: bool = False):
    """
    Weekly flow to update advanced metrics for the current season.

    Args:
        season_year: Season ending year. If None, auto-detected.
        force: Force execution even if season is not active.

    Returns:
        Dictionary with flow execution results.
    """
    logger = get_run_logger()

    logger.info("=" * 80)
    logger.info("WEEKLY ADVANCED METRICS UPDATE")
    logger.info("=" * 80)

    # Step 1: Check if NBA season is active
    if not force:
        is_active = check_nba_season_active()

        if not is_active:
            logger.info("NBA season is not currently active (July-September)")
            logger.info("Skipping weekly advanced metrics update")
            return {
                "status": "skipped",
                "reason": "season_inactive",
                "timestamp": datetime.now().isoformat()
            }
    else:
        logger.info("Force flag enabled - running regardless of season status")

    # Step 2: Determine current season
    if season_year is None:
        current_date = datetime.now()
        if current_date.month >= 10:
            season_year = current_date.year + 1
        else:
            season_year = current_date.year

    logger.info(f"Target season: {season_year-1}-{str(season_year)[-2:]}")

    # Step 3: Fetch advanced metrics
    logger.info("Starting advanced metrics acquisition...")
    logger.info("Source: Basketball Reference")

    try:
        acquisition_result = fetch_advanced_metrics(
            season_year=season_year
        )

        status = acquisition_result.get("status")
        logger.info(f"Acquisition status: {status}")

        if status == "not_implemented":
            logger.warning("Advanced metrics acquisition not yet implemented")
            logger.info("This feature will be added in a future update")
            return {
                "status": "not_implemented",
                "message": "Advanced metrics scraper not yet implemented",
                "timestamp": datetime.now().isoformat()
            }

    except Exception as e:
        logger.error(f"Advanced metrics acquisition failed: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

    # Step 4: Return results
    result = {
        "status": "success" if acquisition_result.get("status") == "success" else "partial",
        "season_year": season_year,
        "acquisition": acquisition_result,
        "timestamp": datetime.now().isoformat()
    }

    logger.info("=" * 80)
    logger.info(f"WEEKLY UPDATE COMPLETE - Status: {result['status'].upper()}")
    logger.info("=" * 80)

    return result


if __name__ == "__main__":
    # For local testing
    result = update_advanced_metrics(force=True)
    print("\nFlow Result:")
    print(result)
