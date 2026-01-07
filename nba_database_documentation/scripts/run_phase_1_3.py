"""
Execute Phase 1.3: Advanced Metrics Scraper Implementation

This script orchestrates the complete implementation:
1. Creates the database table
2. Tests the scraper
3. Validates results
4. Optionally runs full backfill
"""

import sys
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

def run_command(description, command):
    """Run a command and handle output"""
    print(f"\n{'=' * 80}")
    print(f"{description}")
    print(f"{'=' * 80}")
    print(f"Command: {' '.join(command)}\n")

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed with exit code {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to run command: {e}")
        return False

def main():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                    NBA Hub Phase 1.3 Execution                          ║
    ║                  Advanced Metrics Scraper Implementation                 ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)

    # Step 1: Test environment
    if not run_command(
        "Step 1: Testing Environment",
        [sys.executable, str(SCRIPTS_DIR / "test_environment.py")]
    ):
        print("\n[ERROR] Environment test failed. Please install missing dependencies.")
        sys.exit(1)

    # Step 2: Create database table
    if not run_command(
        "Step 2: Creating Database Table",
        [sys.executable, str(SCRIPTS_DIR / "create_advanced_stats_table.py")]
    ):
        print("\n[ERROR] Table creation failed.")
        sys.exit(1)

    # Step 3: Test with 2023-24 season (dry run)
    if not run_command(
        "Step 3: Testing with 2023-24 Season (Dry Run)",
        [
            sys.executable,
            str(SCRIPTS_DIR / "acquire_advanced_metrics.py"),
            "--start-year", "2024",
            "--end-year", "2024",
            "--dry-run"
        ]
    ):
        print("\n[ERROR] 2024 season test failed.")
        sys.exit(1)

    # Step 4: Test with 2023-24 season (actual insert)
    if not run_command(
        "Step 4: Inserting 2023-24 Season Data",
        [
            sys.executable,
            str(SCRIPTS_DIR / "acquire_advanced_metrics.py"),
            "--start-year", "2024",
            "--end-year", "2024"
        ]
    ):
        print("\n[ERROR] 2024 season insertion failed.")
        sys.exit(1)

    # Step 5: Test with 1980 season
    if not run_command(
        "Step 5: Testing with 1980 Season",
        [
            sys.executable,
            str(SCRIPTS_DIR / "acquire_advanced_metrics.py"),
            "--start-year", "1980",
            "--end-year", "1980"
        ]
    ):
        print("\n[ERROR] 1980 season test failed.")
        sys.exit(1)

    # Step 6: Validate results
    print(f"\n{'=' * 80}")
    print("Step 6: Validation")
    print(f"{'=' * 80}")
    print("\nPlease run validation queries to check:")
    print("1. Nikola Jokic's 2023-24 VORP and PER")
    print("2. Total record counts")
    print("3. Multi-team player handling")
    print("\nSample validation query:")
    print("""
    SELECT p.display_first_last, a.season_id, a.per, a.vorp, a.ws
    FROM player_season_advanced_stats a
    JOIN common_player_info p ON a.player_id = p.person_id
    WHERE p.display_first_last = 'Nikola Jokic'
      AND a.season_id = 22023
    ORDER BY a.season_id DESC;
    """)

    # Ask about full backfill
    print(f"\n{'=' * 80}")
    print("Step 7: Full Historical Backfill (Optional)")
    print(f"{'=' * 80}")
    print("\nTo backfill all historical data (1974-2023), run:")
    print(f"  python {SCRIPTS_DIR / 'acquire_advanced_metrics.py'} --start-year 1974 --end-year 2023")
    print("\nThis will take 2-3 hours and insert ~22,500 records.")
    print("The script includes checkpointing so it can be safely interrupted and resumed.")

    print("\n" + "=" * 80)
    print("[OK] Phase 1.3 Initial Implementation Complete!")
    print("=" * 80)

if __name__ == '__main__':
    main()
