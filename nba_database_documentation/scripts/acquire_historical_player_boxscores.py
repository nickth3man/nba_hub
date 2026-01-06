"""
Acquire Historical NBA Player Box Scores (1946-1996)

This script downloads player box scores for the historical era (50 years)
and loads them into the DuckDB database.

Usage:
    python acquire_historical_player_boxscores.py --start-year 1990 --end-year 1996
    python acquire_historical_player_boxscores.py --start-year 1947 --end-year 1996
    python acquire_historical_player_boxscores.py --decade 1980  # 1980-1989
    python acquire_historical_player_boxscores.py --dry-run --start-year 1990 --end-year 1991

Requirements:
    pip install basketball-reference-web-scraper duckdb pandas
"""

import argparse
import json
import sys
import time
from pathlib import Path

import cloudscraper
import duckdb
import pandas as pd
import requests
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import (
    Location,
    TEAM_NAME_TO_TEAM,
    TEAM_TO_TEAM_ABBREVIATION,
)

# Configuration
DB_PATH = Path(r"c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb")
OUTPUT_DIR = Path(r"c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation\data")
CHECKPOINT_FILE = OUTPUT_DIR / "historical_acquisition_checkpoint.json"

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.basketball-reference.com/",
    "Connection": "keep-alive",
}
REQUEST_DELAY_SECONDS = 1.0
RATE_LIMIT_BACKOFF_SECONDS = 10
MAX_RETRIES = 3


def _patch_requests_headers():
    original_get = requests.get
    scraper = None

    try:
        scraper = cloudscraper.create_scraper()
    except Exception:
        scraper = None

    def _get_with_headers(*args, **kwargs):
        headers = REQUEST_HEADERS.copy()
        headers.update(kwargs.pop("headers", {}))
        kwargs["headers"] = headers
        if scraper is not None:
            return scraper.get(*args, **kwargs)
        return original_get(*args, **kwargs)

    requests.get = _get_with_headers


def _box_score_value(box_score, key, default=None):
    if isinstance(box_score, dict):
        return box_score.get(key, default)
    return getattr(box_score, key, default)


def _team_to_abbr(team):
    if team is None:
        return None
    if team in TEAM_TO_TEAM_ABBREVIATION:
        return TEAM_TO_TEAM_ABBREVIATION[team]
    if isinstance(team, str):
        normalized = team.strip().upper()
        if normalized in TEAM_NAME_TO_TEAM:
            return TEAM_TO_TEAM_ABBREVIATION[TEAM_NAME_TO_TEAM[normalized]]
        return normalized
    if hasattr(team, "value"):
        normalized = str(team.value).strip().upper()
        if normalized in TEAM_NAME_TO_TEAM:
            return TEAM_TO_TEAM_ABBREVIATION[TEAM_NAME_TO_TEAM[normalized]]
        return normalized
    return str(team).strip().upper()


_patch_requests_headers()


class HistoricalPlayerBoxScoreAcquisition:
    """Acquire historical player box scores (1946-1996)"""

    def __init__(self, db_path=DB_PATH, dry_run=False):
        self.db_path = db_path
        self.dry_run = dry_run
        self.conn = None
        self.team_abbreviation_map = {}
        self.player_name_to_id_map = {}
        self.checkpoint = self._load_checkpoint()
        self.game_id_map = {}
        self.game_dates = []

        # Stats availability by era
        self.stats_availability = {
            'blocks_steals': 1974,  # Blocks and steals tracked starting 1973-74
            'three_pointers': 1980,  # 3-point line introduced 1979-80
            'offensive_rebounds': 1974,  # Separate OREB/DREB starting 1973-74
        }

    def connect(self):
        """Connect to DuckDB database"""
        try:
            self.conn = duckdb.connect(str(self.db_path))
            print(f"[OK] Connected to database: {self.db_path}")

            # Load mappings
            self._load_team_mapping()
            self._load_player_mapping()

        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            sys.exit(1)

    def _load_game_map(self, season_end_year):
        """Load game_id mapping and game dates for a season"""
        if not self.conn:
            raise RuntimeError("Database connection required to load game map")

        season_start_year = season_end_year - 1
        season_ids = [
            int(f"2{season_start_year}"),  # Regular season
            int(f"4{season_start_year}"),  # Playoffs
        ]

        games = self.conn.execute("""
            SELECT game_id, game_date, home_team_id, visitor_team_id
            FROM games
            WHERE season_id IN (?, ?)
        """, season_ids).fetchdf()

        if games.empty:
            print(f"[WARNING] No games found for season {season_end_year}")
            self.game_id_map = {}
            self.game_dates = []
            return

        games["game_date"] = pd.to_datetime(games["game_date"]).dt.date

        self.game_id_map = {
            (row.game_date, row.home_team_id, row.visitor_team_id): row.game_id
            for row in games.itertuples(index=False)
            if row.game_date is not None
        }
        self.game_dates = sorted({row.game_date for row in games.itertuples(index=False) if row.game_date is not None})

        print(f"[OK] Loaded {len(self.game_id_map)} game mappings")

    def _resolve_game_id(self, game_date, team_abbr, opponent_abbr, location):
        """Resolve game_id using date + home/visitor teams"""
        team_id = self.team_abbreviation_map.get(team_abbr)
        opponent_id = self.team_abbreviation_map.get(opponent_abbr)
        if team_id is None or opponent_id is None:
            return None

        if isinstance(location, Location):
            is_home = location == Location.HOME
        else:
            location_value = getattr(location, "value", str(location))
            is_home = str(location_value).upper() == "HOME"

        home_id = team_id if is_home else opponent_id
        visitor_id = opponent_id if is_home else team_id
        return self.game_id_map.get((game_date, home_id, visitor_id))

    def _fetch_box_scores_for_date(self, game_date):
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return client.player_box_scores(
                    day=game_date.day,
                    month=game_date.month,
                    year=game_date.year
                )
            except Exception as e:
                response = getattr(e, "response", None)
                status_code = getattr(response, "status_code", None)
                if status_code == 429:
                    wait_seconds = RATE_LIMIT_BACKOFF_SECONDS * attempt
                    print(f"  [RATE LIMIT] {game_date} hit 429, sleeping {wait_seconds}s "
                          f"(attempt {attempt}/{MAX_RETRIES})")
                    time.sleep(wait_seconds)
                    continue
                raise
        return None

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

            # Historical team variations
            historical_variations = {
                'PHO': 'PHX',
                'BRK': 'BKN',
                'CHO': 'CHA',
                'CHH': 'CHA',
                'NOH': 'NOP',  # New Orleans Hornets -> Pelicans
                'SEA': 'OKC',  # Seattle -> OKC (map to modern equivalent)
                'STL': 'ATL',  # St. Louis Hawks -> Atlanta
                'VAN': 'MEM',  # Vancouver -> Memphis
                'WSB': 'WAS',  # Washington Bullets -> Wizards
                'KCK': 'SAC',  # Kansas City Kings -> Sacramento
                'NJN': 'BKN',  # New Jersey -> Brooklyn
                'NOK': 'NOP',  # New Orleans/Oklahoma City -> Pelicans
            }

            for br_abbr, nba_abbr in historical_variations.items():
                if nba_abbr in self.team_abbreviation_map:
                    self.team_abbreviation_map[br_abbr] = self.team_abbreviation_map[nba_abbr]

            print(f"[OK] Loaded {len(self.team_abbreviation_map)} team mappings")

        except Exception as e:
            print(f"[WARNING] Could not load team mapping: {e}")

    def _load_player_mapping(self):
        """Load player names to player_id mapping"""
        try:
            players = self.conn.execute("""
                SELECT person_id, display_first_last
                FROM common_player_info
            """).fetchdf()

            for _, row in players.iterrows():
                name = row['display_first_last']
                person_id = row['person_id']
                if name and person_id is not None:
                    self.player_name_to_id_map[name] = int(person_id)

            print(f"[OK] Loaded {len(self.player_name_to_id_map)} player mappings")

        except Exception as e:
            print(f"[WARNING] Could not load player mapping: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("[INFO] Database connection closed")

    def _load_checkpoint(self):
        """Load checkpoint file to resume interrupted acquisition"""
        if CHECKPOINT_FILE.exists():
            with open(CHECKPOINT_FILE, 'r') as f:
                checkpoint = json.load(f)
                print(f"[INFO] Loaded checkpoint: {checkpoint}")
                return checkpoint
        return {'completed_years': []}

    def _save_checkpoint(self, year):
        """Save checkpoint after completing a year"""
        if year not in self.checkpoint['completed_years']:
            self.checkpoint['completed_years'].append(year)
            with open(CHECKPOINT_FILE, 'w') as f:
                json.dump(self.checkpoint, f)
            print(f"[INFO] Checkpoint saved: {year} complete")

    def acquire_year_range(self, start_year, end_year):
        """
        Acquire player box scores for a range of years.

        Args:
            start_year: Starting season year (e.g., 1990 for 1990-91 season)
            end_year: Ending season year (inclusive)
        """
        print(f"\n{'=' * 80}")
        print(f"ACQUIRING HISTORICAL PLAYER BOX SCORES")
        print(f"Years: {start_year}-{end_year}")
        print(f"{'=' * 80}\n")

        for year in range(start_year, end_year + 1):
            # Check if already completed
            if year in self.checkpoint['completed_years']:
                print(f"[SKIP] Season {year} already completed (from checkpoint)")
                continue

            try:
                self.acquire_season(year)
                self._save_checkpoint(year)
                print(f"\n[OK] Season {year} complete and checkpointed")

            except KeyboardInterrupt:
                print(f"\n[INTERRUPTED] Stopping at year {year}")
                print(f"[INFO] Resume by running with same parameters (checkpoint saved)")
                sys.exit(0)

            except Exception as e:
                print(f"\n[ERROR] Failed to acquire season {year}: {e}")
                print(f"[INFO] Continuing to next season...")
                continue

    def acquire_season(self, season_end_year):
        """Acquire all player box scores for one season"""
        print(f"\n{'-' * 80}")
        print(f"Season {season_end_year-1}-{str(season_end_year)[-2:]}")
        print(f"{'-' * 80}")

        # Step 1: Load season games from database
        print(f"[1/3] Loading season games from database...")
        self._load_game_map(season_end_year)
        if not self.game_dates:
            print("[ERROR] No game dates available for this season")
            return

        # Step 2: Fetch player box scores by date
        print(f"[2/3] Downloading player box scores...")
        all_box_scores = []
        failed_dates = []
        unmapped_rows = 0
        unmapped_samples = []

        for idx, game_date in enumerate(self.game_dates):
            if idx % 50 == 0 and idx > 0:
                print(f"  -> Progress: {idx}/{len(self.game_dates)} "
                      f"({idx/len(self.game_dates)*100:.0f}%), "
                      f"Records: {len(all_box_scores)}, Unmapped: {unmapped_rows}")

            try:
                box_scores = self._fetch_box_scores_for_date(game_date)
                if box_scores is None:
                    failed_dates.append({
                        'date': game_date,
                        'error': f"Failed after {MAX_RETRIES} retries"
                    })
                    continue

                for box_score in box_scores:
                    team_abbr = _team_to_abbr(_box_score_value(box_score, "team"))
                    opponent_abbr = _team_to_abbr(_box_score_value(box_score, "opponent"))
                    location = _box_score_value(box_score, "location")
                    game_id = self._resolve_game_id(game_date, team_abbr, opponent_abbr, location)
                    if game_id is None:
                        unmapped_rows += 1
                        if len(unmapped_samples) < 5:
                            unmapped_samples.append(
                                (game_date, team_abbr, opponent_abbr, location)
                            )
                        continue

                    record = self._process_historical_box_score(
                        box_score, game_id, game_date, season_end_year, team_abbr
                    )
                    all_box_scores.append(record)

                time.sleep(REQUEST_DELAY_SECONDS)

            except Exception as e:
                failed_dates.append({
                    'date': game_date,
                    'error': str(e)
                })
                if len(failed_dates) <= 10:
                    print(f"  [WARNING] Failed date {game_date}: {e}")

        print(f"  -> Downloaded {len(all_box_scores)} player box scores")
        if failed_dates:
            print(f"  [WARNING] {len(failed_dates)} dates failed")
        if unmapped_rows:
            print(f"  [WARNING] {unmapped_rows} rows could not be mapped to game_id")
            for sample in unmapped_samples:
                print(f"    Sample unmapped: {sample}")

        # Step 3: Transform and load
        print(f"[3/3] Loading data...")
        if len(all_box_scores) == 0:
            print("[WARNING] No data to load for this season!")
            return

        df = pd.DataFrame(all_box_scores)
        df_transformed = self._transform_to_schema(df)

        # Save to CSV
        output_path = OUTPUT_DIR / f"historical_boxscores_{season_end_year}.csv"
        df_transformed.to_csv(output_path, index=False)
        print(f"  -> Saved to CSV: {output_path}")

        # Load to database
        if not self.dry_run:
            self._load_to_database(df_transformed)
        else:
            print(f"  [DRY RUN] Would load {len(df_transformed)} records")

        print(f"  -> Season summary:")
        print(f"     Records: {len(df_transformed)}")
        print(f"     Games: {df_transformed['game_id'].nunique()}")
        print(f"     Players: {df_transformed['player_name'].nunique()}")

    def _process_historical_box_score(self, box_score, game_id, game_date, season_year, team_abbr):
        """Process box score with era-appropriate handling"""

        # Extract fields (supports dicts or objects)
        player_name = _box_score_value(box_score, "name")
        seconds_played = _box_score_value(box_score, "seconds_played")
        fgm = _box_score_value(box_score, "made_field_goals")
        fga = _box_score_value(box_score, "attempted_field_goals")
        ftm = _box_score_value(box_score, "made_free_throws")
        fta = _box_score_value(box_score, "attempted_free_throws")
        fg3m_raw = _box_score_value(box_score, "made_three_point_field_goals")
        fg3a_raw = _box_score_value(box_score, "attempted_three_point_field_goals")
        points = _box_score_value(box_score, "points")

        if points is None and fgm is not None and ftm is not None:
            points = (2 * fgm) + ftm + (fg3m_raw or 0)

        # Basic fields available in all eras
        record = {
            'game_id': game_id,
            'game_date': game_date,
            'season_year': season_year,
            'player_name': player_name,
            'team': team_abbr,
            'seconds_played': seconds_played,
            'fgm': fgm,
            'fga': fga,
            'ftm': ftm,
            'fta': fta,
            'pts': points,
        }

        # Assists (available in most eras)
        record['ast'] = _box_score_value(box_score, "assists")

        # Rebounds - handle OREB/DREB split
        if season_year >= self.stats_availability['offensive_rebounds']:
            record['oreb'] = _box_score_value(box_score, "offensive_rebounds", 0)
            record['dreb'] = _box_score_value(box_score, "defensive_rebounds", 0)
        else:
            # Before 1973-74, only total rebounds available
            total_reb = (_box_score_value(box_score, "offensive_rebounds", 0) +
                         _box_score_value(box_score, "defensive_rebounds", 0))
            record['oreb'] = None
            record['dreb'] = None
            record['reb_total'] = total_reb

        # 3-pointers (only from 1979-80 onwards)
        if season_year >= self.stats_availability['three_pointers']:
            record['fg3m'] = fg3m_raw if fg3m_raw is not None else 0
            record['fg3a'] = fg3a_raw if fg3a_raw is not None else 0
        else:
            record['fg3m'] = None
            record['fg3a'] = None

        # Steals and blocks (from 1973-74 onwards)
        if season_year >= self.stats_availability['blocks_steals']:
            record['stl'] = _box_score_value(box_score, "steals", 0)
            record['blk'] = _box_score_value(box_score, "blocks", 0)
        else:
            record['stl'] = None
            record['blk'] = None

        # Turnovers and personal fouls (available in most eras)
        record['tov'] = _box_score_value(box_score, "turnovers")
        record['pf'] = _box_score_value(box_score, "personal_fouls")

        return record

    def _transform_to_schema(self, df):
        """Transform to match database schema"""

        # Calculate total rebounds
        df['reb'] = df.apply(
            lambda row: (row['oreb'] + row['dreb']) if pd.notna(row['oreb']) else row.get('reb_total'),
            axis=1
        )

        # Calculate percentages
        df['fg_pct'] = df.apply(
            lambda row: row['fgm'] / row['fga'] if row['fga'] > 0 else 0.0,
            axis=1
        )
        df['fg3_pct'] = df.apply(
            lambda row: row['fg3m'] / row['fg3a'] if pd.notna(row['fg3a']) and row['fg3a'] > 0 else None,
            axis=1
        )
        df['ft_pct'] = df.apply(
            lambda row: row['ftm'] / row['fta'] if row['fta'] > 0 else 0.0,
            axis=1
        )

        # Convert seconds to minutes
        df['min'] = df['seconds_played'].apply(
            lambda s: f"{s // 60}:{s % 60:02d}" if pd.notna(s) and s > 0 else "0:00"
        )

        # Map teams
        df['team_id'] = df['team'].map(self.team_abbreviation_map)

        # Map players
        df['player_id'] = df['player_name'].map(self.player_name_to_id_map)

        # Select columns
        df_schema = df[[
            'game_id', 'team_id', 'player_id', 'player_name',
            'min', 'fgm', 'fga', 'fg_pct',
            'fg3m', 'fg3a', 'fg3_pct',
            'ftm', 'fta', 'ft_pct',
            'oreb', 'dreb', 'reb',
            'ast', 'stl', 'blk', 'tov', 'pf', 'pts'
        ]].copy()

        # Add placeholder columns
        df_schema['start_position'] = None
        df_schema['comment'] = None
        df_schema['plus_minus'] = None

        return df_schema

    def _load_to_database(self, df):
        """Load to database"""
        try:
            insert_query = """
                INSERT INTO player_game_stats_silver (
                    game_id, team_id, player_id, player_name, start_position, comment,
                    min, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct,
                    ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, tov, pf, pts, plus_minus
                )
                SELECT * FROM df AS src
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM player_game_stats_silver p
                    WHERE p.game_id = src.game_id
                      AND p.player_name = src.player_name
                      AND p.team_id IS NOT DISTINCT FROM src.team_id
                )
            """

            rows_inserted = self.conn.execute(insert_query).fetchone()[0]
            print(f"  [OK] Inserted {rows_inserted} records")

        except Exception as e:
            print(f"  [ERROR] Failed to load: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Acquire historical NBA player box scores (1946-1996)"
    )
    parser.add_argument(
        '--start-year',
        type=int,
        help='Starting season end year (e.g., 1990 for 1989-90)'
    )
    parser.add_argument(
        '--end-year',
        type=int,
        help='Ending season end year (inclusive)'
    )
    parser.add_argument(
        '--decade',
        type=int,
        choices=[1940, 1950, 1960, 1970, 1980, 1990],
        help='Acquire full decade (e.g., 1980 = 1980-1989)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Download but do not insert into database'
    )

    args = parser.parse_args()

    # Determine year range
    if args.decade:
        start_year = args.decade
        end_year = args.decade + 9
    elif args.start_year and args.end_year:
        start_year = args.start_year
        end_year = args.end_year
    else:
        parser.error("Must specify either --decade or both --start-year and --end-year")

    print(f"\nHistorical Player Box Score Acquisition")
    print(f"Year range: {start_year} to {end_year}")
    print(f"Dry run: {args.dry_run}")
    print(f"{'=' * 80}\n")

    # Create acquisition instance
    acq = HistoricalPlayerBoxScoreAcquisition(dry_run=args.dry_run)
    acq.connect()

    try:
        acq.acquire_year_range(start_year, end_year)
    finally:
        acq.disconnect()

    print("\n[OK] Historical acquisition complete!")


if __name__ == '__main__':
    main()
