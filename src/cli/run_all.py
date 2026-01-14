import subprocess
import sys
import time


def run_script(script_path, description):
    print(f"\n=== {description} ===")
    start_time = time.time()
    try:
        subprocess.run([sys.executable, script_path], check=True)
        print(f"[OK] Completed in {time.time() - start_time:.2f}s")
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Failed: {e}")
        # We don't exit here to allow other independent steps to proceed,
        # but in a strict pipeline we might want to.
        # For Ralph Loop, we want to try to finish as much as possible.


def main():
    print("Starting Full NBA Data Pipeline...")
    pipeline_start = time.time()

    # 1. Initialization
    run_script(
        "src/etl/load/init_referees_coaches.py", "Initializing Referees & Coaches"
    )
    run_script("src/etl/load/init_awards_table.py", "Initializing Awards Table")

    # 2. Backfill Scraping (Historical Data)
    run_script(
        "src/scraping/backfill/scrape_coaches_history.py", "Scraping Coaches History"
    )
    run_script(
        "src/scraping/backfill/scrape_awards_voting.py", "Scraping Awards Voting"
    )
    run_script(
        "src/scraping/backfill/scrape_draft_history.py", "Scraping Draft History"
    )

    # 3. Load Raw Data
    run_script("src/etl/load/load_games.py", "Loading Raw Games")
    run_script("src/etl/load/load_box_scores.py", "Loading Raw Box Scores")

    # 4. Transform
    run_script(
        "src/etl/transform/migrate_unified_schema.py", "Migrating to Unified Schema"
    )

    # 5. Ingestion
    run_script(
        "src/etl/ingest/ingest_all_players.py", "Ingesting All Players (Common Info)"
    )
    run_script("src/etl/ingest/ingest_advanced_stats.py", "Ingesting Advanced Stats")
    run_script("src/etl/ingest/ingest_awards.py", "Ingesting Awards (Historical)")
    run_script("src/etl/ingest/ingest_transactions.py", "Ingesting Transactions")

    print(f"\n=== Pipeline Complete in {time.time() - pipeline_start:.2f}s ===")


if __name__ == "__main__":
    main()
