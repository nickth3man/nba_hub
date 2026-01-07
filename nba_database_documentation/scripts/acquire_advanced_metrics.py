"""
Acquire NBA Advanced Metrics from Basketball-Reference

This script downloads advanced player statistics (PER, Win Shares, BPM, VORP)
from Basketball-Reference and loads them into the DuckDB database.

Usage:
    python acquire_advanced_metrics.py --start-year 2024 --end-year 2024
    python acquire_advanced_metrics.py --start-year 1974 --end-year 2023
    python acquire_advanced_metrics.py --dry-run --start-year 2024 --end-year 2024

Requirements:
    pip install cloudscraper duckdb pandas thefuzz

Data Source:
    https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html

Notes:
    - Advanced metrics available from 1973-74 season onwards
    - Uses cloudscraper to handle Cloudflare protection
    - Rate limiting: 1.0 second delay between requests
    - Fuzzy matching for player names to database IDs
"""

import argparse
import sys
import time
from pathlib import Path

import cloudscraper
import duckdb
import pandas as pd
from thefuzz import fuzz, process

# Configuration
DB_PATH = Path(r"c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb")
OUTPUT_DIR = Path(r"c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation\data")
REQUEST_DELAY_SECONDS = 1.0
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 5

# Basketball-Reference team abbreviation mapping to NBA API abbreviations
BREF_TO_NBA_TEAM_MAP = {
    'ATL': 'ATL', 'BOS': 'BOS', 'BRK': 'BKN', 'CHI': 'CHI', 'CHO': 'CHA',
    'CLE': 'CLE', 'DAL': 'DAL', 'DEN': 'DEN', 'DET': 'DET', 'GSW': 'GSW',
    'HOU': 'HOU', 'IND': 'IND', 'LAC': 'LAC', 'LAL': 'LAL', 'MEM': 'MEM',
    'MIA': 'MIA', 'MIL': 'MIL', 'MIN': 'MIN', 'NOP': 'NOP', 'NYK': 'NYK',
    'OKC': 'OKC', 'ORL': 'ORL', 'PHI': 'PHI', 'PHO': 'PHX', 'POR': 'POR',
    'SAC': 'SAC', 'SAS': 'SAS', 'TOR': 'TOR', 'UTA': 'UTA', 'WAS': 'WAS',

    # Historical teams
    'CHH': 'CHA',  # Charlotte Hornets (original)
    'NOH': 'NOP',  # New Orleans Hornets
    'NOK': 'NOP',  # New Orleans/Oklahoma City
    'NJN': 'BKN',  # New Jersey Nets
    'SEA': 'OKC',  # Seattle SuperSonics
    'VAN': 'MEM',  # Vancouver Grizzlies
    'WSB': 'WAS',  # Washington Bullets
    'KCK': 'SAC',  # Kansas City Kings
    'SDC': 'LAC',  # San Diego Clippers
    'CHA': 'CHA',  # Charlotte (various iterations)
}


class AdvancedMetricsAcquisition:
    """Acquire advanced metrics from Basketball-Reference"""

    def __init__(self, db_path=DB_PATH, dry_run=False):
        self.db_path = db_path
        self.dry_run = dry_run
        self.conn = None
        self.scraper = cloudscraper.create_scraper()
        self.player_name_to_id_map = {}
        self.player_id_to_name_map = {}
        self.team_abbreviation_map = {}
        self.team_id_to_abbr_map = {}

    def connect(self):
        """Connect to DuckDB database"""
        try:
            self.conn = duckdb.connect(str(self.db_path))
            print(f"[OK] Connected to database: {self.db_path}")

            # Load mappings
            self._load_player_mapping()
            self._load_team_mapping()

        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            sys.exit(1)

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("[INFO] Database connection closed")

    def _load_player_mapping(self):
        """Load player names to player_id mapping"""
        try:
            players = self.conn.execute("""
                SELECT person_id, display_first_last, first_name, last_name
                FROM common_player_info
            """).fetchdf()

            for _, row in players.iterrows():
                person_id = row['person_id']
                display_name = row['display_first_last']
                first_name = row['first_name']
                last_name = row['last_name']

                if person_id is not None and display_name:
                    self.player_name_to_id_map[display_name] = int(person_id)
                    self.player_id_to_name_map[int(person_id)] = display_name

                    # Also map alternate name format
                    if first_name and last_name:
                        alt_name = f"{first_name} {last_name}"
                        if alt_name != display_name:
                            self.player_name_to_id_map[alt_name] = int(person_id)

            print(f"[OK] Loaded {len(self.player_id_to_name_map)} player mappings")

        except Exception as e:
            print(f"[WARNING] Could not load player mapping: {e}")

    def _load_team_mapping(self):
        """Load team abbreviations to team_id mapping"""
        try:
            teams = self.conn.execute("""
                SELECT id, abbreviation, full_name
                FROM team
            """).fetchdf()

            for _, row in teams.iterrows():
                abbr = row['abbreviation']
                team_id = row['id']
                if abbr and team_id is not None:
                    self.team_abbreviation_map[abbr] = int(team_id)
                    self.team_id_to_abbr_map[int(team_id)] = abbr

            print(f"[OK] Loaded {len(self.team_abbreviation_map)} team mappings")

        except Exception as e:
            print(f"[WARNING] Could not load team mapping: {e}")

    def _fuzzy_match_player(self, bref_name):
        """
        Fuzzy match Basketball-Reference player name to database player_id

        Args:
            bref_name: Player name from Basketball-Reference

        Returns:
            player_id or None if no good match found
        """
        # Try exact match first
        if bref_name in self.player_name_to_id_map:
            return self.player_name_to_id_map[bref_name]

        # Try fuzzy match with high threshold
        result = process.extractOne(
            bref_name,
            self.player_name_to_id_map.keys(),
            scorer=fuzz.ratio
        )

        if result and result[1] >= 85:  # 85% similarity threshold
            matched_name = result[0]
            return self.player_name_to_id_map[matched_name]

        return None

    def _map_team_abbreviation(self, bref_abbr):
        """
        Map Basketball-Reference team abbreviation to database team_id

        Args:
            bref_abbr: Team abbreviation from Basketball-Reference

        Returns:
            team_id or None if not found
        """
        if bref_abbr == 'TOT':  # Total for multi-team players
            return None

        # Map to NBA API abbreviation
        nba_abbr = BREF_TO_NBA_TEAM_MAP.get(bref_abbr, bref_abbr)

        # Get team_id from database
        return self.team_abbreviation_map.get(nba_abbr)

    def fetch_advanced_stats(self, year):
        """
        Fetch advanced stats for a season from Basketball-Reference

        Args:
            year: Season end year (e.g., 2024 for 2023-24 season)

        Returns:
            DataFrame with advanced stats or None if failed
        """
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"  -> Fetching {url}")
                response = self.scraper.get(url, timeout=30)
                response.raise_for_status()

                # Parse HTML table
                tables = pd.read_html(response.text)

                if not tables:
                    print(f"  [WARNING] No tables found for year {year}")
                    return None

                df = tables[0]  # First table is the advanced stats table

                # Remove header rows that appear mid-table
                df = df[df['Player'] != 'Player']

                # Remove rows with no player name
                df = df[df['Player'].notna()]

                print(f"  [OK] Fetched {len(df)} player records")
                return df

            except Exception as e:
                print(f"  [WARNING] Attempt {attempt}/{MAX_RETRIES} failed: {e}")
                if attempt < MAX_RETRIES:
                    wait_time = RETRY_BACKOFF_SECONDS * attempt
                    print(f"  -> Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"  [ERROR] Failed to fetch data for year {year}")
                    return None

        return None

    def process_advanced_stats(self, df, year):
        """
        Process and clean advanced stats DataFrame

        Args:
            df: Raw DataFrame from Basketball-Reference
            year: Season end year

        Returns:
            Processed DataFrame ready for database insertion
        """
        records = []
        skipped_tot = 0
        unmapped_players = 0
        unmapped_teams = 0
        unmapped_player_samples = []

        for idx, row in df.iterrows():
            # Skip TOT (total) rows for multi-team players
            team_abbr = str(row.get('Tm', '')).strip()
            if team_abbr == 'TOT':
                skipped_tot += 1
                continue

            # Extract player name
            player_name = str(row.get('Player', '')).strip()
            if not player_name or player_name == 'Player':
                continue

            # Remove asterisks and other special characters
            player_name = player_name.replace('*', '').strip()

            # Map player to database ID
            player_id = self._fuzzy_match_player(player_name)
            if player_id is None:
                unmapped_players += 1
                if len(unmapped_player_samples) < 5:
                    unmapped_player_samples.append(player_name)
                continue

            # Map team to database ID
            team_id = self._map_team_abbreviation(team_abbr)
            if team_id is None:
                unmapped_teams += 1
                continue

            # Calculate season_id (format: 2YYYY for regular season)
            season_id = int(f"2{year - 1}")

            # Extract statistics
            def safe_float(value):
                """Convert value to float, return None if empty or invalid"""
                if pd.isna(value) or value == '' or value == 'None':
                    return None
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return None

            def safe_int(value):
                """Convert value to int, return None if empty or invalid"""
                if pd.isna(value) or value == '' or value == 'None':
                    return None
                try:
                    return int(float(value))
                except (ValueError, TypeError):
                    return None

            record = {
                'player_id': player_id,
                'season_id': season_id,
                'team_id': team_id,
                'games_played': safe_int(row.get('G')),
                'minutes_played': safe_int(row.get('MP')),

                # Advanced Metrics
                'per': safe_float(row.get('PER')),
                'ts_pct': safe_float(row.get('TS%')),
                'efg_pct': safe_float(row.get('eFG%')),
                'fg3a_rate': safe_float(row.get('3PAr')),
                'fta_rate': safe_float(row.get('FTr')),

                'orb_pct': safe_float(row.get('ORB%')),
                'drb_pct': safe_float(row.get('DRB%')),
                'trb_pct': safe_float(row.get('TRB%')),
                'ast_pct': safe_float(row.get('AST%')),
                'stl_pct': safe_float(row.get('STL%')),
                'blk_pct': safe_float(row.get('BLK%')),
                'tov_pct': safe_float(row.get('TOV%')),
                'usg_pct': safe_float(row.get('USG%')),

                # Impact Metrics
                'ows': safe_float(row.get('OWS')),
                'dws': safe_float(row.get('DWS')),
                'ws': safe_float(row.get('WS')),
                'ws_48': safe_float(row.get('WS/48')),

                'obpm': safe_float(row.get('OBPM')),
                'dbpm': safe_float(row.get('DBPM')),
                'bpm': safe_float(row.get('BPM')),
                'vorp': safe_float(row.get('VORP')),
            }

            records.append(record)

        print(f"  -> Processed {len(records)} records")
        if skipped_tot > 0:
            print(f"  -> Skipped {skipped_tot} TOT rows (multi-team players)")
        if unmapped_players > 0:
            print(f"  [WARNING] {unmapped_players} players could not be mapped")
            for sample in unmapped_player_samples:
                print(f"    Sample unmapped: {sample}")
        if unmapped_teams > 0:
            print(f"  [WARNING] {unmapped_teams} team mappings failed")

        return pd.DataFrame(records)

    def load_to_database(self, df):
        """
        Load processed data into database

        Args:
            df: Processed DataFrame ready for insertion
        """
        if df.empty:
            print("  [WARNING] No data to load")
            return

        try:
            # Use INSERT OR IGNORE to prevent duplicates
            insert_query = """
                INSERT INTO player_season_advanced_stats (
                    player_id, season_id, team_id, games_played, minutes_played,
                    per, ts_pct, efg_pct, fg3a_rate, fta_rate,
                    orb_pct, drb_pct, trb_pct, ast_pct, stl_pct, blk_pct, tov_pct, usg_pct,
                    ows, dws, ws, ws_48,
                    obpm, dbpm, bpm, vorp
                )
                SELECT * FROM df
                WHERE NOT EXISTS (
                    SELECT 1 FROM player_season_advanced_stats p
                    WHERE p.player_id = df.player_id
                      AND p.season_id = df.season_id
                      AND p.team_id = df.team_id
                )
            """

            result = self.conn.execute(insert_query)
            rows_inserted = result.fetchone()[0]
            print(f"  [OK] Inserted {rows_inserted} records into database")

        except Exception as e:
            print(f"  [ERROR] Failed to load data: {e}")
            raise

    def acquire_season(self, year):
        """
        Acquire advanced stats for a single season

        Args:
            year: Season end year (e.g., 2024 for 2023-24 season)
        """
        print(f"\n{'-' * 80}")
        print(f"Season {year-1}-{str(year)[-2:]}")
        print(f"{'-' * 80}")

        # Step 1: Fetch data
        print(f"[1/3] Fetching data from Basketball-Reference...")
        df_raw = self.fetch_advanced_stats(year)
        if df_raw is None:
            print(f"[ERROR] Failed to fetch data for season {year}")
            return

        # Step 2: Process data
        print(f"[2/3] Processing and mapping data...")
        df_processed = self.process_advanced_stats(df_raw, year)

        if df_processed.empty:
            print(f"[WARNING] No data to load for season {year}")
            return

        # Save to CSV
        output_path = OUTPUT_DIR / f"advanced_metrics_{year}.csv"
        df_processed.to_csv(output_path, index=False)
        print(f"  -> Saved to CSV: {output_path}")

        # Step 3: Load to database
        print(f"[3/3] Loading to database...")
        if not self.dry_run:
            self.load_to_database(df_processed)
        else:
            print(f"  [DRY RUN] Would load {len(df_processed)} records")

        # Summary
        print(f"\n  -> Season summary:")
        print(f"     Records: {len(df_processed)}")
        print(f"     Players: {df_processed['player_id'].nunique()}")
        print(f"     Teams: {df_processed['team_id'].nunique()}")

        # Rate limiting
        time.sleep(REQUEST_DELAY_SECONDS)

    def acquire_year_range(self, start_year, end_year):
        """
        Acquire advanced stats for a range of years

        Args:
            start_year: Starting season year (e.g., 1974)
            end_year: Ending season year (inclusive, e.g., 2023)
        """
        print(f"\n{'=' * 80}")
        print(f"ACQUIRING ADVANCED METRICS")
        print(f"Years: {start_year}-{end_year}")
        print(f"Database: {self.db_path}")
        print(f"Dry run: {self.dry_run}")
        print(f"{'=' * 80}\n")

        successful = 0
        failed = 0

        for year in range(start_year, end_year + 1):
            try:
                self.acquire_season(year)
                successful += 1
                print(f"\n[OK] Season {year} complete")

            except KeyboardInterrupt:
                print(f"\n[INTERRUPTED] Stopping at year {year}")
                print(f"[INFO] Run again with same parameters to resume")
                sys.exit(0)

            except Exception as e:
                print(f"\n[ERROR] Failed to acquire season {year}: {e}")
                failed += 1
                continue

        # Final summary
        print(f"\n{'=' * 80}")
        print(f"ACQUISITION COMPLETE")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"{'=' * 80}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Acquire NBA advanced metrics from Basketball-Reference"
    )
    parser.add_argument(
        '--start-year',
        type=int,
        required=True,
        help='Starting season end year (e.g., 2024 for 2023-24 season)'
    )
    parser.add_argument(
        '--end-year',
        type=int,
        required=True,
        help='Ending season end year (inclusive)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Download and process but do not insert into database'
    )

    args = parser.parse_args()

    # Validate year range
    if args.start_year < 1974:
        print("[ERROR] Advanced metrics not available before 1973-74 season")
        sys.exit(1)

    if args.start_year > args.end_year:
        print("[ERROR] Start year must be <= end year")
        sys.exit(1)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Run acquisition
    acq = AdvancedMetricsAcquisition(dry_run=args.dry_run)
    acq.connect()

    try:
        acq.acquire_year_range(args.start_year, args.end_year)
    finally:
        acq.disconnect()

    print("\n[OK] Advanced metrics acquisition complete!")


if __name__ == '__main__':
    main()
