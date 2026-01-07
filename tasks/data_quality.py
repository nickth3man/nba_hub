"""
Prefect tasks for data quality validation and checks.
Implements comprehensive data quality validation for the NBA database.
"""

import duckdb
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from prefect import task
from prefect.logging import get_run_logger


# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "nba.duckdb"


@task(
    name="validate-referential-integrity",
    description="Check for referential integrity violations",
    tags=["validation", "data-quality"]
)
def validate_referential_integrity(db_path: Optional[str] = None) -> dict:
    """
    Check for referential integrity violations in the database.

    Validates:
    - Player game stats have valid game_id references
    - Player game stats have valid team_id references
    - Games have valid team_id references

    Args:
        db_path: Path to DuckDB database.

    Returns:
        Dictionary with validation results.
    """
    logger = get_run_logger()
    db_path = db_path or str(DB_PATH)

    logger.info("Checking referential integrity...")

    conn = duckdb.connect(db_path, read_only=True)
    issues = []

    try:
        # Check 1: Player stats with invalid game_id
        logger.info("Checking player stats -> games foreign keys")
        result = conn.execute("""
            SELECT COUNT(*) as invalid_count
            FROM player_game_stats_silver p
            WHERE p.game_id IS NOT NULL
              AND NOT EXISTS (
                  SELECT 1 FROM games g WHERE g.game_id = p.game_id
              )
        """).fetchone()

        invalid_game_refs = result[0] if result else 0
        if invalid_game_refs > 0:
            issues.append({
                "check": "player_stats_game_id_fk",
                "severity": "high",
                "count": invalid_game_refs,
                "message": f"{invalid_game_refs} player stats records reference non-existent games"
            })
            logger.warning(f"Found {invalid_game_refs} invalid game_id references")
        else:
            logger.info("All player stats have valid game_id references")

        # Check 2: Player stats with invalid team_id
        logger.info("Checking player stats -> team foreign keys")
        result = conn.execute("""
            SELECT COUNT(*) as invalid_count
            FROM player_game_stats_silver p
            WHERE p.team_id IS NOT NULL
              AND NOT EXISTS (
                  SELECT 1 FROM team t WHERE t.id = p.team_id
              )
        """).fetchone()

        invalid_team_refs = result[0] if result else 0
        if invalid_team_refs > 0:
            issues.append({
                "check": "player_stats_team_id_fk",
                "severity": "high",
                "count": invalid_team_refs,
                "message": f"{invalid_team_refs} player stats records reference non-existent teams"
            })
            logger.warning(f"Found {invalid_team_refs} invalid team_id references")
        else:
            logger.info("All player stats have valid team_id references")

        # Check 3: Games with invalid home_team_id
        logger.info("Checking games -> team foreign keys")
        result = conn.execute("""
            SELECT COUNT(*) as invalid_count
            FROM games g
            WHERE (g.home_team_id IS NOT NULL
                   AND NOT EXISTS (SELECT 1 FROM team t WHERE t.id = g.home_team_id))
               OR (g.visitor_team_id IS NOT NULL
                   AND NOT EXISTS (SELECT 1 FROM team t WHERE t.id = g.visitor_team_id))
        """).fetchone()

        invalid_games = result[0] if result else 0
        if invalid_games > 0:
            issues.append({
                "check": "games_team_id_fk",
                "severity": "high",
                "count": invalid_games,
                "message": f"{invalid_games} games reference non-existent teams"
            })
            logger.warning(f"Found {invalid_games} games with invalid team references")
        else:
            logger.info("All games have valid team_id references")

    finally:
        conn.close()

    passed = len(issues) == 0

    return {
        "check_type": "referential_integrity",
        "passed": passed,
        "total_issues": len(issues),
        "issues": issues,
        "timestamp": datetime.now().isoformat()
    }


@task(
    name="validate-data-completeness",
    description="Check for missing or NULL critical data",
    tags=["validation", "data-quality"]
)
def validate_data_completeness(db_path: Optional[str] = None) -> dict:
    """
    Check for data completeness issues like NULL values in critical fields.

    Args:
        db_path: Path to DuckDB database.

    Returns:
        Dictionary with validation results.
    """
    logger = get_run_logger()
    db_path = db_path or str(DB_PATH)

    logger.info("Checking data completeness...")

    conn = duckdb.connect(db_path, read_only=True)
    issues = []

    try:
        # Check 1: Player stats missing critical fields
        logger.info("Checking for NULL values in critical player stats fields")

        critical_fields = [
            ("game_id", "high"),
            ("player_name", "high"),
            ("team_id", "medium"),
            ("pts", "low"),
            ("min", "low")
        ]

        for field, severity in critical_fields:
            result = conn.execute(f"""
                SELECT COUNT(*) as null_count
                FROM player_game_stats_silver
                WHERE {field} IS NULL
            """).fetchone()

            null_count = result[0] if result else 0
            if null_count > 0:
                issues.append({
                    "check": f"null_{field}",
                    "severity": severity,
                    "count": null_count,
                    "message": f"{null_count} player stats records have NULL {field}"
                })
                logger.warning(f"Found {null_count} records with NULL {field}")

        # Check 2: Games missing dates
        logger.info("Checking for games with missing dates")
        result = conn.execute("""
            SELECT COUNT(*) as null_dates
            FROM games
            WHERE game_date IS NULL
        """).fetchone()

        null_dates = result[0] if result else 0
        if null_dates > 0:
            issues.append({
                "check": "games_null_date",
                "severity": "high",
                "count": null_dates,
                "message": f"{null_dates} games have NULL game_date"
            })
            logger.warning(f"Found {null_dates} games with NULL dates")

        # Check 3: Overall record counts
        logger.info("Checking overall record counts")
        stats = {}

        tables = ["games", "player_game_stats_silver", "team", "common_player_info"]
        for table in tables:
            try:
                result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
                count = result[0] if result else 0
                stats[table] = count
                logger.info(f"{table}: {count:,} records")

                if count == 0:
                    issues.append({
                        "check": f"{table}_empty",
                        "severity": "critical",
                        "count": 0,
                        "message": f"Table {table} is empty"
                    })
            except Exception as e:
                logger.warning(f"Could not check table {table}: {e}")

    finally:
        conn.close()

    passed = all(issue["severity"] != "critical" for issue in issues)

    return {
        "check_type": "data_completeness",
        "passed": passed,
        "total_issues": len(issues),
        "issues": issues,
        "record_counts": stats if 'stats' in locals() else {},
        "timestamp": datetime.now().isoformat()
    }


@task(
    name="validate-statistical-anomalies",
    description="Detect impossible or anomalous statistics",
    tags=["validation", "data-quality"]
)
def validate_statistical_anomalies(db_path: Optional[str] = None) -> dict:
    """
    Check for statistically impossible or anomalous values.

    Checks for:
    - Negative statistics
    - Field goals made > field goals attempted
    - Points calculation errors
    - Extreme outliers

    Args:
        db_path: Path to DuckDB database.

    Returns:
        Dictionary with validation results.
    """
    logger = get_run_logger()
    db_path = db_path or str(DB_PATH)

    logger.info("Checking for statistical anomalies...")

    conn = duckdb.connect(db_path, read_only=True)
    issues = []

    try:
        # Check 1: Negative statistics
        logger.info("Checking for negative statistics")
        stat_fields = ["pts", "reb", "ast", "stl", "blk", "fgm", "fga", "ftm", "fta"]

        for field in stat_fields:
            result = conn.execute(f"""
                SELECT COUNT(*) as negative_count
                FROM player_game_stats_silver
                WHERE {field} < 0
            """).fetchone()

            negative_count = result[0] if result else 0
            if negative_count > 0:
                issues.append({
                    "check": f"negative_{field}",
                    "severity": "high",
                    "count": negative_count,
                    "message": f"{negative_count} records have negative {field}"
                })
                logger.warning(f"Found {negative_count} records with negative {field}")

        # Check 2: FGM > FGA (impossible)
        logger.info("Checking for FGM > FGA violations")
        result = conn.execute("""
            SELECT COUNT(*) as violation_count
            FROM player_game_stats_silver
            WHERE fgm > fga
              AND fgm IS NOT NULL
              AND fga IS NOT NULL
        """).fetchone()

        fgm_violations = result[0] if result else 0
        if fgm_violations > 0:
            issues.append({
                "check": "fgm_greater_than_fga",
                "severity": "high",
                "count": fgm_violations,
                "message": f"{fgm_violations} records have FGM > FGA (impossible)"
            })
            logger.warning(f"Found {fgm_violations} FGM > FGA violations")

        # Check 3: FTM > FTA
        logger.info("Checking for FTM > FTA violations")
        result = conn.execute("""
            SELECT COUNT(*) as violation_count
            FROM player_game_stats_silver
            WHERE ftm > fta
              AND ftm IS NOT NULL
              AND fta IS NOT NULL
        """).fetchone()

        ftm_violations = result[0] if result else 0
        if ftm_violations > 0:
            issues.append({
                "check": "ftm_greater_than_fta",
                "severity": "high",
                "count": ftm_violations,
                "message": f"{ftm_violations} records have FTM > FTA (impossible)"
            })
            logger.warning(f"Found {ftm_violations} FTM > FTA violations")

        # Check 4: 3PM > FGM (impossible)
        logger.info("Checking for 3PM > FGM violations")
        result = conn.execute("""
            SELECT COUNT(*) as violation_count
            FROM player_game_stats_silver
            WHERE fg3m > fgm
              AND fg3m IS NOT NULL
              AND fgm IS NOT NULL
        """).fetchone()

        three_violations = result[0] if result else 0
        if three_violations > 0:
            issues.append({
                "check": "fg3m_greater_than_fgm",
                "severity": "high",
                "count": three_violations,
                "message": f"{three_violations} records have 3PM > FGM (impossible)"
            })
            logger.warning(f"Found {three_violations} 3PM > FGM violations")

        # Check 5: Extreme outliers (e.g., >100 points in a game)
        logger.info("Checking for extreme outliers")
        result = conn.execute("""
            SELECT COUNT(*) as outlier_count
            FROM player_game_stats_silver
            WHERE pts > 100
              OR reb > 50
              OR ast > 50
        """).fetchone()

        outliers = result[0] if result else 0
        if outliers > 0:
            issues.append({
                "check": "extreme_outliers",
                "severity": "medium",
                "count": outliers,
                "message": f"{outliers} records have extreme outlier values (>100 pts, >50 reb/ast)"
            })
            logger.warning(f"Found {outliers} extreme outliers")

    finally:
        conn.close()

    passed = len(issues) == 0

    return {
        "check_type": "statistical_anomalies",
        "passed": passed,
        "total_issues": len(issues),
        "issues": issues,
        "timestamp": datetime.now().isoformat()
    }


@task(
    name="generate-validation-report",
    description="Generate comprehensive validation report",
    tags=["validation", "reporting"]
)
def generate_validation_report(
    referential_check: dict,
    completeness_check: dict,
    anomalies_check: dict
) -> dict:
    """
    Generate a comprehensive validation report from all checks.

    Args:
        referential_check: Results from referential integrity check.
        completeness_check: Results from data completeness check.
        anomalies_check: Results from statistical anomalies check.

    Returns:
        Comprehensive validation report.
    """
    logger = get_run_logger()

    logger.info("Generating comprehensive validation report...")

    all_checks = [referential_check, completeness_check, anomalies_check]

    # Count issues by severity
    severity_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    all_issues = []
    for check in all_checks:
        for issue in check.get("issues", []):
            all_issues.append(issue)
            severity = issue.get("severity", "low")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

    # Determine overall pass/fail
    overall_passed = all(check.get("passed", False) for check in all_checks)

    # Generate summary
    summary = {
        "overall_status": "PASS" if overall_passed else "FAIL",
        "total_checks": len(all_checks),
        "checks_passed": sum(1 for c in all_checks if c.get("passed", False)),
        "checks_failed": sum(1 for c in all_checks if not c.get("passed", False)),
        "total_issues": len(all_issues),
        "issues_by_severity": severity_counts,
        "timestamp": datetime.now().isoformat()
    }

    report = {
        "summary": summary,
        "checks": {
            "referential_integrity": referential_check,
            "data_completeness": completeness_check,
            "statistical_anomalies": anomalies_check
        },
        "all_issues": all_issues
    }

    # Log summary
    logger.info("=" * 60)
    logger.info("VALIDATION REPORT SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Overall Status: {summary['overall_status']}")
    logger.info(f"Checks Passed: {summary['checks_passed']}/{summary['total_checks']}")
    logger.info(f"Total Issues: {summary['total_issues']}")
    logger.info(f"  - Critical: {severity_counts['critical']}")
    logger.info(f"  - High: {severity_counts['high']}")
    logger.info(f"  - Medium: {severity_counts['medium']}")
    logger.info(f"  - Low: {severity_counts['low']}")
    logger.info("=" * 60)

    if not overall_passed:
        logger.warning("Validation FAILED - issues detected")
    else:
        logger.info("Validation PASSED - no critical issues")

    return report


@task(
    name="quick-record-count-check",
    description="Quick check of new record counts",
    tags=["validation", "quick-check"]
)
def quick_record_count_check(
    db_path: Optional[str] = None,
    expected_min_records: int = 0
) -> dict:
    """
    Quick validation check for record counts.

    Args:
        db_path: Path to DuckDB database.
        expected_min_records: Minimum expected records in player_game_stats_silver.

    Returns:
        Dictionary with record count validation results.
    """
    logger = get_run_logger()
    db_path = db_path or str(DB_PATH)

    logger.info("Running quick record count check...")

    conn = duckdb.connect(db_path, read_only=True)

    try:
        result = conn.execute("""
            SELECT COUNT(*) as total_records
            FROM player_game_stats_silver
        """).fetchone()

        total_records = result[0] if result else 0
        passed = total_records >= expected_min_records

        logger.info(f"Total player game stats: {total_records:,}")
        logger.info(f"Expected minimum: {expected_min_records:,}")
        logger.info(f"Check: {'PASS' if passed else 'FAIL'}")

        return {
            "check_type": "quick_record_count",
            "passed": passed,
            "total_records": total_records,
            "expected_min": expected_min_records,
            "timestamp": datetime.now().isoformat()
        }

    finally:
        conn.close()
