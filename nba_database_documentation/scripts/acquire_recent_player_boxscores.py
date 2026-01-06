"""
Acquire Recent NBA Player Box Scores (2023-2026)

This script downloads player box scores for the missing recent seasons
and loads them into the DuckDB database.

Usage:
    python acquire_recent_player_boxscores.py --season 2024
    python acquire_recent_player_boxscores.py --season 2024 --dry-run
    python acquire_recent_player_boxscores.py --season all

Requirements:
    pip install basketball-reference-web-scraper duckdb pandas
"""

import argparse
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


class PlayerBoxScoreAcquisition:
    """Acquire and load player box scores into DuckDB"""

    def __init__(self, db_path=DB_PATH, dry_run=False):
        self.db_path = db_path
        self.dry_run = dry_run
        self.conn = None
        self.team_abbreviation_map = {}
        self.player_name_to_id_map = {}
        self.game_id_map = {}
        self.game_dates = []

        # Season ID mapping: basketball-reference year -> DuckDB season_id format
        # For season ending in 2024 (2023-24), we use different IDs for each game type
        self.season_type_prefix = {
            'preseason': 1,
            'regular': 2,
            'allstar': 3,
            'playoffs': 4
        }

    def connect(self):
        """Connect to DuckDB database"""
        try:
            self.conn = duckdb.connect(str(self.db_path))
            print(f"[OK] Connected to database: {self.db_path}")

            # Load team abbreviation mapping
            self._load_team_mapping()
            # Load player mapping
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

            # Create mapping from Basketball-Reference abbreviations to team IDs
            for _, row in teams.iterrows():
                abbr = row['abbreviation']
                team_id = row['id']
                if abbr and team_id is not None:
                    self.team_abbreviation_map[abbr] = int(team_id)

            # Add common variations
            # Basketball-Reference uses different abbreviations than NBA sometimes
            variations = {
                'PHO': 'PHX',  # Phoenix Suns
                'BRK': 'BKN',  # Brooklyn Nets
                'CHO': 'CHA',  # Charlotte (Hornets/Bobcats)
            }

            for br_abbr, nba_abbr in variations.items():
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

    def acquire_season(self, season_end_year):
        """
        Acquire all player box scores for a season.

        Args:
            season_end_year: The year the season ends (e.g., 2024 for 2023-24 season)
        """
        print(f"\n{'=' * 80}")
        print(f"ACQUIRING SEASON {season_end_year-1}-{str(season_end_year)[-2:]}")
        print(f"{'=' * 80}\n")

        # Step 1: Load season games from database
        print(f"[1/3] Loading season games from database...")
        self._load_game_map(season_end_year)
        if not self.game_dates:
            print("[ERROR] No game dates available for this season")
            return

        # Step 2: Fetch player box scores by date
        print(f"\n[2/3] Downloading player box scores...")
        all_box_scores = []
        failed_dates = []
        unmapped_rows = 0
        unmapped_samples = []

        for idx, game_date in enumerate(self.game_dates):
            if idx % 50 == 0 and idx > 0:
                print(f"  -> Progress: {idx}/{len(self.game_dates)} games ({idx/len(self.game_dates)*100:.1f}%)")

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

                    fgm = _box_score_value(box_score, "made_field_goals")
                    ftm = _box_score_value(box_score, "made_free_throws")
                    fg3m = _box_score_value(box_score, "made_three_point_field_goals")
                    points = _box_score_value(box_score, "points")
                    if points is None and fgm is not None and ftm is not None:
                        points = (2 * fgm) + ftm + (fg3m or 0)

                    all_box_scores.append({
                        'game_id': game_id,
                        'game_date': game_date,
                        'season_year': season_end_year,
                        'player_name': _box_score_value(box_score, "name"),
                        'team': team_abbr,
                        'location': getattr(location, "value", str(location)),
                        'opponent': opponent_abbr,
                        'outcome': _box_score_value(box_score, "outcome"),
                        'seconds_played': _box_score_value(box_score, "seconds_played"),
                        'fgm': fgm,
                        'fga': _box_score_value(box_score, "attempted_field_goals"),
                        'fg3m': fg3m,
                        'fg3a': _box_score_value(box_score, "attempted_three_point_field_goals"),
                        'ftm': ftm,
                        'fta': _box_score_value(box_score, "attempted_free_throws"),
                        'oreb': _box_score_value(box_score, "offensive_rebounds"),
                        'dreb': _box_score_value(box_score, "defensive_rebounds"),
                        'ast': _box_score_value(box_score, "assists"),
                        'stl': _box_score_value(box_score, "steals"),
                        'blk': _box_score_value(box_score, "blocks"),
                        'tov': _box_score_value(box_score, "turnovers"),
                        'pf': _box_score_value(box_score, "personal_fouls"),
                        'pts': points,
                    })

                time.sleep(REQUEST_DELAY_SECONDS)

            except Exception as e:
                failed_dates.append({
                    'date': game_date,
                    'error': str(e)
                })
                if len(failed_dates) <= 10:
                    print(f"  [WARNING] Failed to fetch date {game_date}: {e}")

        print(f"  -> Downloaded {len(all_box_scores)} player box scores")
        if failed_dates:
            print(f"  [WARNING] Failed to download {len(failed_dates)} dates")
        if unmapped_rows:
            print(f"  [WARNING] {unmapped_rows} rows could not be mapped to game_id")
            for sample in unmapped_samples:
                print(f"    Sample unmapped: {sample}")

        # Step 3: Transform and load data
        print(f"\n[3/3] Transforming and loading data...")
        df = pd.DataFrame(all_box_scores)

        if len(df) == 0:
            print("[ERROR] No data to load!")
            return

        # Transform to match database schema
        df_transformed = self._transform_to_schema(df, season_end_year)

        # Save to CSV for review
        output_path = OUTPUT_DIR / f"player_boxscores_{season_end_year}.csv"
        df_transformed.to_csv(output_path, index=False)
        print(f"  -> Saved to CSV: {output_path}")

        # Load into database
        if not self.dry_run:
            self._load_to_database(df_transformed)
        else:
            print(f"  [DRY RUN] Would load {len(df_transformed)} records to database")

        print(f"\n[OK] Season {season_end_year} complete!")
        print(f"  - Total records: {len(df_transformed)}")
        print(f"  - Unique games: {df_transformed['game_id'].nunique()}")
        print(f"  - Unique players: {df_transformed['player_name'].nunique()}")

    def _transform_to_schema(self, df, season_end_year):
        """Transform Basketball-Reference format to database schema"""

        # Calculate derived fields
        df['reb'] = df['oreb'] + df['dreb']

        # Calculate percentages
        df['fg_pct'] = df.apply(
            lambda row: row['fgm'] / row['fga'] if row['fga'] > 0 else 0.0,
            axis=1
        )
        df['fg3_pct'] = df.apply(
            lambda row: row['fg3m'] / row['fg3a'] if row['fg3a'] > 0 else 0.0,
            axis=1
        )
        df['ft_pct'] = df.apply(
            lambda row: row['ftm'] / row['fta'] if row['fta'] > 0 else 0.0,
            axis=1
        )

        # Convert seconds to minutes string format (MM:SS)
        df['min'] = df['seconds_played'].apply(
            lambda s: f"{s // 60}:{s % 60:02d}" if pd.notna(s) else "0:00"
        )

        # Map team abbreviations to team_id
        df['team_id'] = df['team'].map(self.team_abbreviation_map)

        # Try to map player names to player_id
        df['player_id'] = df['player_name'].map(self.player_name_to_id_map)

        # For players not in our mapping, we'll need to assign new IDs or skip
        # For now, we'll keep player_name and handle ID assignment separately

        # Select and rename columns to match player_game_stats_silver schema
        columns_map = {
            'game_id': 'game_id',
            'team_id': 'team_id',
            'player_id': 'player_id',
            'player_name': 'player_name',
            'min': 'min',
            'fgm': 'fgm',
            'fga': 'fga',
            'fg_pct': 'fg_pct',
            'fg3m': 'fg3m',
            'fg3a': 'fg3a',
            'fg3_pct': 'fg3_pct',
            'ftm': 'ftm',
            'fta': 'fta',
            'ft_pct': 'ft_pct',
            'oreb': 'oreb',
            'dreb': 'dreb',
            'reb': 'reb',
            'ast': 'ast',
            'stl': 'stl',
            'blk': 'blk',
            'tov': 'tov',
            'pf': 'pf',
            'pts': 'pts',
        }

        df_schema = df[list(columns_map.keys())].copy()
        df_schema = df_schema.rename(columns=columns_map)

        # Add placeholder columns that might be in schema but not in data
        df_schema['start_position'] = None
        df_schema['comment'] = None
        df_schema['plus_minus'] = None

        return df_schema

    def _load_to_database(self, df):
        """Load transformed data into database"""
        try:
            # Insert into player_game_stats_silver
            # Use INSERT OR IGNORE to skip duplicates
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
            print(f"  [OK] Inserted {rows_inserted} new records into player_game_stats_silver")

        except Exception as e:
            print(f"  [ERROR] Failed to load data: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Acquire recent NBA player box scores"
    )
    parser.add_argument(
        '--season',
        required=True,
        help='Season ending year (2024 for 2023-24) or "all" for 2024-2026'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Download data but do not insert into database'
    )

    args = parser.parse_args()

    # Create acquisition instance
    acq = PlayerBoxScoreAcquisition(dry_run=args.dry_run)
    acq.connect()

    try:
        if args.season.lower() == 'all':
            # Acquire all missing recent seasons
            for year in [2024, 2025, 2026]:
                acq.acquire_season(year)
                print("\n" + "=" * 80 + "\n")
        else:
            # Acquire single season
            season_year = int(args.season)
            acq.acquire_season(season_year)

    finally:
        acq.disconnect()

    print("\n[OK] Acquisition complete!")


if __name__ == '__main__':
    main()
