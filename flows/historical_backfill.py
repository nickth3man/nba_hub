"""
Historical Data Backfill Flow

Purpose: Long-running historical data acquisition for past decades
Schedule: Manual execution only
Features:
  - Decade-by-decade acquisition
  - 5-hour timeout for long-running jobs
  - Comprehensive error handling and progress tracking
  - Checkpoint integration for resumability
"""

from datetime import datetime
from prefect import flow, get_run_logger

# Import tasks
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tasks.data_acquisition import historical_backfill_decade
from tasks.data_quality import quick_record_count_check


@flow(
    name="historical-backfill",
    description="Ad-hoc historical data backfill for past decades",
    retries=0,  # Don't retry entire backfill, handle at task level
    timeout_seconds=18000,  # 5 hours
    log_prints=True
)
def historical_backfill(
    start_year: int = 2000,
    end_year: int = 2024,
    db_path: str = None
):
    """
    Flow to backfill historical NBA data for multiple years.

    This is a long-running flow intended for manual execution to populate
    historical data. It processes data decade by decade with checkpointing.

    Args:
        start_year: First season ending year to acquire (e.g., 2000 for 1999-2000).
        end_year: Last season ending year to acquire (e.g., 2024 for 2023-24).
        db_path: Path to DuckDB database. If None, uses default.

    Returns:
        Dictionary with backfill results.
    """
    logger = get_run_logger()

    logger.info("=" * 80)
    logger.info("HISTORICAL DATA BACKFILL")
    logger.info("=" * 80)
    logger.info(f"Start Year: {start_year}")
    logger.info(f"End Year: {end_year}")
    logger.info(f"Total Seasons: {end_year - start_year + 1}")
    logger.info(f"Estimated Duration: {(end_year - start_year + 1) * 10} minutes")
    logger.info("")

    # Validate input
    if start_year >= end_year:
        logger.error("start_year must be less than end_year")
        return {
            "status": "error",
            "error": "Invalid year range"
        }

    if end_year > datetime.now().year + 1:
        logger.warning(f"end_year {end_year} is in the future, adjusting to current season")
        end_year = datetime.now().year + 1

    # Get initial record count
    logger.info("Checking initial database state...")
    try:
        initial_check = quick_record_count_check(db_path=db_path)
        initial_records = initial_check.get('total_records', 0)
        logger.info(f"Initial record count: {initial_records:,}")
    except Exception as e:
        logger.warning(f"Could not get initial record count: {e}")
        initial_records = 0

    logger.info("")

    # Split into decades for better progress tracking
    decade_ranges = []
    current_start = start_year

    while current_start <= end_year:
        decade_end = min(current_start + 9, end_year)
        decade_ranges.append((current_start, decade_end))
        current_start = decade_end + 1

    logger.info(f"Split into {len(decade_ranges)} decade batches:")
    for i, (decade_start, decade_end) in enumerate(decade_ranges, 1):
        logger.info(f"  Batch {i}: {decade_start}-{decade_end} ({decade_end - decade_start + 1} seasons)")

    logger.info("")

    # Process each decade
    all_results = []
    total_successful = 0
    total_failed = 0

    for batch_num, (decade_start, decade_end) in enumerate(decade_ranges, 1):
        logger.info("=" * 80)
        logger.info(f"BATCH {batch_num}/{len(decade_ranges)}: {decade_start}-{decade_end}")
        logger.info("=" * 80)

        try:
            result = historical_backfill_decade(
                start_year=decade_start,
                end_year=decade_end,
                db_path=db_path
            )

            all_results.append(result)
            batch_successful = result.get('successful', 0)
            batch_failed = result.get('failed', 0)

            total_successful += batch_successful
            total_failed += batch_failed

            logger.info(f"Batch {batch_num} complete: {batch_successful} successful, {batch_failed} failed")

        except Exception as e:
            logger.error(f"Batch {batch_num} failed with error: {e}")
            all_results.append({
                "start_year": decade_start,
                "end_year": decade_end,
                "status": "error",
                "error": str(e)
            })
            total_failed += (decade_end - decade_start + 1)

        logger.info("")

    # Get final record count
    logger.info("Checking final database state...")
    try:
        final_check = quick_record_count_check(db_path=db_path)
        final_records = final_check.get('total_records', 0)
        records_added = final_records - initial_records
        logger.info(f"Final record count: {final_records:,}")
        logger.info(f"Records added: {records_added:,}")
    except Exception as e:
        logger.warning(f"Could not get final record count: {e}")
        final_records = initial_records
        records_added = 0

    # Final summary
    logger.info("")
    logger.info("=" * 80)
    logger.info("BACKFILL COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Total Seasons Processed: {end_year - start_year + 1}")
    logger.info(f"Successful: {total_successful}")
    logger.info(f"Failed: {total_failed}")
    logger.info(f"Records Added: {records_added:,}")
    logger.info("=" * 80)

    overall_status = "success" if total_failed == 0 else ("partial" if total_successful > 0 else "failed")

    return {
        "status": overall_status,
        "start_year": start_year,
        "end_year": end_year,
        "total_seasons": end_year - start_year + 1,
        "total_successful": total_successful,
        "total_failed": total_failed,
        "initial_records": initial_records,
        "final_records": final_records,
        "records_added": records_added,
        "batches": all_results,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    # For local testing - small range
    result = historical_backfill(
        start_year=2020,
        end_year=2023
    )
    print("\nBackfill Result:")
    print(f"Status: {result['status']}")
    print(f"Successful: {result['total_successful']}")
    print(f"Failed: {result['total_failed']}")
    print(f"Records Added: {result['records_added']:,}")
