"""
Daily NBA Data Update Flow

Purpose: Download yesterday's games for current season (2025-26)
Schedule: Daily at 6 AM during NBA season (October-June)
Features:
  - Only runs during NBA season
  - Fetches yesterday's player box scores using nba_api
  - Quick validation of new data
  - Retry logic: 3 attempts with 5-min delay
"""

from datetime import datetime
from prefect import flow, get_run_logger
from prefect.tasks import task_input_hash
from datetime import timedelta

# Import tasks
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tasks.data_acquisition import (
    fetch_recent_player_boxscores,
    check_nba_season_active,
    get_yesterday_date
)
from tasks.data_quality import quick_record_count_check


@flow(
    name="daily-player-boxscores",
    description="Daily update of player box scores for current NBA season",
    retries=0,  # Retries handled at task level
    log_prints=True
)
def daily_player_boxscores(season_year: int = None, force: bool = False):
    """
    Daily flow to update player box scores for the current season.

    Args:
        season_year: Season ending year. If None, auto-detected.
        force: Force execution even if season is not active.

    Returns:
        Dictionary with flow execution results.
    """
    logger = get_run_logger()

    logger.info("=" * 80)
    logger.info("DAILY PLAYER BOX SCORES UPDATE")
    logger.info("=" * 80)

    # Step 1: Check if NBA season is active
    if not force:
        is_active = check_nba_season_active()

        if not is_active:
            logger.info("NBA season is not currently active (July-September)")
            logger.info("Skipping daily update")
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

    # Step 3: Get yesterday's date for logging
    yesterday = get_yesterday_date()
    logger.info(f"Fetching games for: {yesterday}")

    # Step 4: Fetch player box scores
    logger.info("Starting data acquisition...")

    try:
        acquisition_result = fetch_recent_player_boxscores(
            season_year=season_year
        )

        logger.info("Data acquisition completed successfully")
        logger.info(f"Status: {acquisition_result.get('status')}")

    except Exception as e:
        logger.error(f"Data acquisition failed: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

    # Step 5: Quick validation
    logger.info("Running quick validation checks...")

    try:
        validation_result = quick_record_count_check(
            expected_min_records=1000  # Expect at least 1000 player-game records
        )

        logger.info(f"Validation: {'PASSED' if validation_result['passed'] else 'FAILED'}")
        logger.info(f"Total records in database: {validation_result['total_records']:,}")

    except Exception as e:
        logger.warning(f"Validation check failed: {e}")
        validation_result = {
            "passed": False,
            "error": str(e)
        }

    # Step 6: Return results
    result = {
        "status": "success" if acquisition_result.get("status") == "success" else "partial",
        "season_year": season_year,
        "acquisition": acquisition_result,
        "validation": validation_result,
        "timestamp": datetime.now().isoformat()
    }

    logger.info("=" * 80)
    logger.info(f"DAILY UPDATE COMPLETE - Status: {result['status'].upper()}")
    logger.info("=" * 80)

    return result


if __name__ == "__main__":
    # For local testing
    result = daily_player_boxscores()
    print("\nFlow Result:")
    print(result)
