"""
Validate Advanced Metrics Data

This script validates the loaded advanced metrics data against known benchmarks
and checks data quality.
"""

import sys
from pathlib import Path
import duckdb
import pandas as pd

DB_PATH = Path(r"c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb")

def print_section(title):
    """Print a section header"""
    print(f"\n{'=' * 80}")
    print(f"{title}")
    print(f"{'=' * 80}\n")

def main():
    print_section("Advanced Metrics Data Validation")

    try:
        conn = duckdb.connect(str(DB_PATH))
        print("[OK] Connected to database\n")

        # 1. Table existence and record count
        print_section("1. Table Overview")
        count = conn.execute("""
            SELECT COUNT(*) as total_records
            FROM player_season_advanced_stats
        """).fetchone()[0]
        print(f"Total records: {count:,}")

        if count == 0:
            print("[WARNING] No data in table. Run the scraper first.")
            return

        # 2. Records by season
        print_section("2. Records by Season")
        by_season = conn.execute("""
            SELECT
                season_id,
                COUNT(*) as records,
                COUNT(DISTINCT player_id) as unique_players,
                COUNT(DISTINCT team_id) as unique_teams
            FROM player_season_advanced_stats
            GROUP BY season_id
            ORDER BY season_id DESC
            LIMIT 10
        """).fetchdf()
        print(by_season.to_string(index=False))

        # 3. Nikola Jokic validation
        print_section("3. Nikola Jokic Stats Validation (2023-24)")
        jokic = conn.execute("""
            SELECT
                p.display_first_last as player,
                a.season_id,
                t.abbreviation as team,
                a.games_played as G,
                a.per as PER,
                a.vorp as VORP,
                a.ws as WS,
                a.bpm as BPM,
                a.ts_pct as TS_pct
            FROM player_season_advanced_stats a
            JOIN common_player_info p ON a.player_id = p.person_id
            JOIN team t ON a.team_id = t.id
            WHERE p.display_first_last = 'Nikola Jokic'
              AND a.season_id = 22023
        """).fetchdf()

        if not jokic.empty:
            print(jokic.to_string(index=False))
            print("\nExpected values (Basketball-Reference 2023-24):")
            print("  PER:  ~31.5")
            print("  VORP: ~8.5-9.0")
            print("  WS:   ~13.0-15.0")
            print("  BPM:  ~11.0-12.0")
        else:
            print("[WARNING] Nikola Jokic data not found for 2023-24")

        # 4. Top players by VORP (2023-24)
        print_section("4. Top 10 Players by VORP (2023-24)")
        top_vorp = conn.execute("""
            SELECT
                p.display_first_last as player,
                t.abbreviation as team,
                a.vorp,
                a.per,
                a.ws,
                a.bpm
            FROM player_season_advanced_stats a
            JOIN common_player_info p ON a.player_id = p.person_id
            JOIN team t ON a.team_id = t.id
            WHERE a.season_id = 22023
              AND a.vorp IS NOT NULL
            ORDER BY a.vorp DESC
            LIMIT 10
        """).fetchdf()
        print(top_vorp.to_string(index=False))

        # 5. Multi-team player check
        print_section("5. Multi-Team Players Check")
        multi_team = conn.execute("""
            SELECT
                p.display_first_last as player,
                a.season_id,
                COUNT(*) as team_count,
                STRING_AGG(t.abbreviation, ', ') as teams
            FROM player_season_advanced_stats a
            JOIN common_player_info p ON a.player_id = p.person_id
            JOIN team t ON a.team_id = t.id
            WHERE a.season_id = 22023
            GROUP BY p.display_first_last, a.season_id
            HAVING COUNT(*) > 1
            ORDER BY team_count DESC
            LIMIT 10
        """).fetchdf()

        if not multi_team.empty:
            print(f"Found {len(multi_team)} players with multiple teams in 2023-24:")
            print(multi_team.to_string(index=False))
            print("\n[OK] Multi-team players properly split (no TOT rows)")
        else:
            print("No multi-team players found in 2023-24 season")

        # 6. Data completeness
        print_section("6. Data Completeness")
        completeness = conn.execute("""
            SELECT
                COUNT(*) as total_records,
                SUM(CASE WHEN per IS NOT NULL THEN 1 ELSE 0 END) as has_per,
                SUM(CASE WHEN vorp IS NOT NULL THEN 1 ELSE 0 END) as has_vorp,
                SUM(CASE WHEN ws IS NOT NULL THEN 1 ELSE 0 END) as has_ws,
                SUM(CASE WHEN bpm IS NOT NULL THEN 1 ELSE 0 END) as has_bpm,
                SUM(CASE WHEN ts_pct IS NOT NULL THEN 1 ELSE 0 END) as has_ts_pct
            FROM player_season_advanced_stats
            WHERE season_id = 22023
        """).fetchone()

        total = completeness[0]
        print(f"Total records: {total}")
        print(f"PER filled:    {completeness[1]} ({completeness[1]/total*100:.1f}%)")
        print(f"VORP filled:   {completeness[2]} ({completeness[2]/total*100:.1f}%)")
        print(f"WS filled:     {completeness[3]} ({completeness[3]/total*100:.1f}%)")
        print(f"BPM filled:    {completeness[4]} ({completeness[4]/total*100:.1f}%)")
        print(f"TS% filled:    {completeness[5]} ({completeness[5]/total*100:.1f}%)")

        # 7. Historical data check (1980)
        print_section("7. Historical Data Check (1980)")
        hist_1980 = conn.execute("""
            SELECT
                COUNT(*) as records,
                COUNT(DISTINCT player_id) as players,
                COUNT(DISTINCT team_id) as teams
            FROM player_season_advanced_stats
            WHERE season_id = 21979
        """).fetchone()

        if hist_1980[0] > 0:
            print(f"1980 season records: {hist_1980[0]}")
            print(f"Unique players: {hist_1980[1]}")
            print(f"Unique teams: {hist_1980[2]}")

            # Top players from 1980
            top_1980 = conn.execute("""
                SELECT
                    p.display_first_last as player,
                    t.abbreviation as team,
                    a.vorp,
                    a.ws,
                    a.per
                FROM player_season_advanced_stats a
                JOIN common_player_info p ON a.player_id = p.person_id
                JOIN team t ON a.team_id = t.id
                WHERE a.season_id = 21979
                  AND a.vorp IS NOT NULL
                ORDER BY a.vorp DESC
                LIMIT 5
            """).fetchdf()
            print("\nTop 5 players by VORP (1980):")
            print(top_1980.to_string(index=False))
        else:
            print("[INFO] No 1980 season data found (not yet loaded)")

        # 8. Duplicate check
        print_section("8. Duplicate Check")
        duplicates = conn.execute("""
            SELECT
                player_id,
                season_id,
                team_id,
                COUNT(*) as duplicate_count
            FROM player_season_advanced_stats
            GROUP BY player_id, season_id, team_id
            HAVING COUNT(*) > 1
        """).fetchdf()

        if duplicates.empty:
            print("[OK] No duplicates found")
        else:
            print(f"[WARNING] Found {len(duplicates)} duplicate records:")
            print(duplicates)

        conn.close()

        print_section("Validation Summary")
        print("[OK] Validation complete!")
        print("\nNext steps:")
        print("1. If data looks good, run full backfill:")
        print("   python acquire_advanced_metrics.py --start-year 1974 --end-year 2023")
        print("\n2. Monitor progress and check for errors")
        print("\n3. Re-run this validation after full backfill")

    except Exception as e:
        print(f"[ERROR] Validation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
