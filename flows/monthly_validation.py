"""
Monthly Data Quality Validation Flow

Purpose: Comprehensive data quality checks
Schedule: 1st of month at 9 AM
Features:
  - Check referential integrity (invalid foreign keys)
  - Check data completeness (missing stats, NULL values)
  - Detect statistical anomalies (impossible stats)
  - Generate validation report with pass/fail status
"""

from datetime import datetime
from prefect import flow, get_run_logger

# Import tasks
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tasks.data_quality import (
    validate_referential_integrity,
    validate_data_completeness,
    validate_statistical_anomalies,
    generate_validation_report
)


@flow(
    name="validate-data-quality",
    description="Monthly comprehensive data quality validation",
    retries=0,
    log_prints=True
)
def validate_data_quality(db_path: str = None):
    """
    Monthly flow to perform comprehensive data quality validation.

    Runs three main validation checks:
    1. Referential Integrity - Check foreign key relationships
    2. Data Completeness - Check for NULL values and missing data
    3. Statistical Anomalies - Check for impossible or suspicious values

    Args:
        db_path: Path to DuckDB database. If None, uses default.

    Returns:
        Comprehensive validation report dictionary.
    """
    logger = get_run_logger()

    logger.info("=" * 80)
    logger.info("MONTHLY DATA QUALITY VALIDATION")
    logger.info("=" * 80)
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("")

    # Step 1: Referential Integrity Check
    logger.info("[1/3] Running Referential Integrity Check...")
    logger.info("-" * 80)

    try:
        referential_check = validate_referential_integrity(db_path=db_path)
        logger.info(f"Referential Integrity: {'PASS' if referential_check['passed'] else 'FAIL'}")
        logger.info(f"Issues found: {referential_check['total_issues']}")

        if referential_check['total_issues'] > 0:
            logger.warning("Referential integrity issues detected:")
            for issue in referential_check['issues']:
                logger.warning(f"  - {issue['message']} [Severity: {issue['severity']}]")

    except Exception as e:
        logger.error(f"Referential integrity check failed: {e}")
        referential_check = {
            "check_type": "referential_integrity",
            "passed": False,
            "total_issues": 0,
            "issues": [],
            "error": str(e)
        }

    logger.info("")

    # Step 2: Data Completeness Check
    logger.info("[2/3] Running Data Completeness Check...")
    logger.info("-" * 80)

    try:
        completeness_check = validate_data_completeness(db_path=db_path)
        logger.info(f"Data Completeness: {'PASS' if completeness_check['passed'] else 'FAIL'}")
        logger.info(f"Issues found: {completeness_check['total_issues']}")

        if completeness_check.get('record_counts'):
            logger.info("Record counts:")
            for table, count in completeness_check['record_counts'].items():
                logger.info(f"  - {table}: {count:,}")

        if completeness_check['total_issues'] > 0:
            logger.warning("Data completeness issues detected:")
            for issue in completeness_check['issues'][:10]:  # Show first 10
                logger.warning(f"  - {issue['message']} [Severity: {issue['severity']}]")

    except Exception as e:
        logger.error(f"Data completeness check failed: {e}")
        completeness_check = {
            "check_type": "data_completeness",
            "passed": False,
            "total_issues": 0,
            "issues": [],
            "error": str(e)
        }

    logger.info("")

    # Step 3: Statistical Anomalies Check
    logger.info("[3/3] Running Statistical Anomalies Check...")
    logger.info("-" * 80)

    try:
        anomalies_check = validate_statistical_anomalies(db_path=db_path)
        logger.info(f"Statistical Anomalies: {'PASS' if anomalies_check['passed'] else 'FAIL'}")
        logger.info(f"Issues found: {anomalies_check['total_issues']}")

        if anomalies_check['total_issues'] > 0:
            logger.warning("Statistical anomalies detected:")
            for issue in anomalies_check['issues'][:10]:  # Show first 10
                logger.warning(f"  - {issue['message']} [Severity: {issue['severity']}]")

    except Exception as e:
        logger.error(f"Statistical anomalies check failed: {e}")
        anomalies_check = {
            "check_type": "statistical_anomalies",
            "passed": False,
            "total_issues": 0,
            "issues": [],
            "error": str(e)
        }

    logger.info("")

    # Step 4: Generate Comprehensive Report
    logger.info("[4/4] Generating Comprehensive Validation Report...")
    logger.info("-" * 80)

    try:
        report = generate_validation_report(
            referential_check=referential_check,
            completeness_check=completeness_check,
            anomalies_check=anomalies_check
        )

        logger.info("Report generated successfully")

    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        report = {
            "summary": {
                "overall_status": "ERROR",
                "error": str(e)
            },
            "checks": {
                "referential_integrity": referential_check,
                "data_completeness": completeness_check,
                "statistical_anomalies": anomalies_check
            }
        }

    # Step 5: Final Summary
    logger.info("")
    logger.info("=" * 80)
    logger.info("VALIDATION COMPLETE")
    logger.info("=" * 80)

    summary = report.get("summary", {})
    logger.info(f"Overall Status: {summary.get('overall_status', 'UNKNOWN')}")
    logger.info(f"Total Checks: {summary.get('total_checks', 0)}")
    logger.info(f"Checks Passed: {summary.get('checks_passed', 0)}")
    logger.info(f"Checks Failed: {summary.get('checks_failed', 0)}")
    logger.info(f"Total Issues: {summary.get('total_issues', 0)}")

    if summary.get('issues_by_severity'):
        logger.info("Issues by Severity:")
        for severity, count in summary['issues_by_severity'].items():
            if count > 0:
                logger.info(f"  - {severity.capitalize()}: {count}")

    logger.info("=" * 80)

    return report


if __name__ == "__main__":
    # For local testing
    result = validate_data_quality()
    print("\nValidation Report:")
    print(f"Overall Status: {result['summary']['overall_status']}")
    print(f"Total Issues: {result['summary']['total_issues']}")
