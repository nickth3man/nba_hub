"""
Acquire recent NBA player box scores using nba_api (NBA.com official API).

This script uses nba_api instead of basketball-reference-web-scraper to avoid
403 Forbidden errors. The NBA.com API is more reliable for recent seasons.

Usage:
    python acquire_recent_nbaapi.py --season 2024
    python acquire_recent_nbaapi.py --season 2024 --dry-run
    python acquire_recent_nbaapi.py --season all  # Get 2024, 2025

Author: NBA Database Analysis
Date: 2026-01-05
"""

import argparse
import duckdb
import pandas as pd
import time
import warnings
from datetime import datetime
from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2
from nba_api.stats.static import teams as nba_teams

# Suppress deprecation warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)


class NBAAPIPlayerBoxScoreAcquisition:
    """Acquire player box scores using NBA.com API."""

    def __init__(self, db_path: str, dry_run: bool = False):
        self.db_path = db_path
        self.dry_run = dry_run
        self.conn = None

        # NBA season format mapping (e.g., 2024 -> "2023-24")
        self.season_format_map = {
            2024: "2023-24",
            2025: "2024-25",
            2026: "2025-26"
        }

        # Initialize team mapping (NBA API team IDs to database team IDs)
        self.team_map = self._build_team_mapping()

    def _build_team_mapping(self):
        """Build mapping from NBA API team abbreviations to database team IDs."""
        # Get NBA API teams
        api_teams = nba_teams.get_teams()

        # Common abbreviation variations
        abbr_mapping = {
            'PHX': 'PHO',  # Phoenix
            'BKN': 'BRK',  # Brooklyn
            'CHA': 'CHO',  # Charlotte (recent)
            'CHH': 'CHO',  # Charlotte Hornets (old)
            'NOP': 'NOH',  # New Orleans
            'NOH': 'NOP',  # New Orleans variations
        }

        mapping = {}
        for team in api_teams:
            abbr = team['abbreviation']
            mapping[abbr] = abbr  # Default to same
            if abbr in abbr_mapping:
                mapping[abbr] = abbr_mapping[abbr]

        return mapping

    def connect_db(self):
        """Connect to DuckDB database."""
        if self.dry_run:
            print("[DRY RUN] Would connect to database (skipped)\n")
            return

        print(f"[INFO] Connecting to database: {self.db_path}")
        self.conn = duckdb.connect(self.db_path)
        print("[OK] Connected to database\n")

    def close_db(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("[INFO] Database connection closed")

    def acquire_season(self, season_end_year: int):
        """
        Acquire all player box scores for a given season.

        Args:
            season_end_year: Season ending year (e.g., 2024 for 2023-24 season)
        """
        season_str = self.season_format_map.get(season_end_year)
        if not season_str:
            print(f"[ERROR] Invalid season year: {season_end_year}")
            print(f"[INFO] Supported seasons: {list(self.season_format_map.keys())}")
            return

        print("=" * 80)
        print(f"ACQUIRING SEASON {season_str}")
        print("=" * 80)
        print()

        # Step 1: Get all games for the season
        print(f"[1/3] Fetching all games for {season_str} season...")
        games_df = self._fetch_season_games(season_str)

        if games_df is None or len(games_df) == 0:
            print(f"[ERROR] No games found for season {season_str}")
            return

        print(f"[OK] Found {len(games_df)} team-game records ({len(games_df) // 2} games)")

        # Get unique games (each game appears twice - once per team)
        unique_game_ids = games_df['GAME_ID'].unique()
        print(f"[INFO] Processing {len(unique_game_ids)} unique games")

        # Step 2: Fetch player box scores for each game
        print(f"\n[2/3] Fetching player box scores (this may take 15-30 minutes)...")
        all_player_stats = []
        errors = []

        for idx, game_id in enumerate(unique_game_ids):
            if (idx + 1) % 100 == 0:
                print(f"  Progress: {idx + 1}/{len(unique_game_ids)} games")

            try:
                # Get box score for this game
                box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
                player_stats = box_score.player_stats.get_data_frame()

                if len(player_stats) > 0:
                    # Add game metadata
                    game_info = games_df[games_df['GAME_ID'] == game_id].iloc[0]
                    player_stats['GAME_DATE'] = game_info['GAME_DATE']
                    player_stats['SEASON_ID'] = self._determine_season_id(
                        game_info['GAME_DATE'],
                        season_end_year
                    )

                    all_player_stats.append(player_stats)

                # Rate limiting (NBA API: max ~100 requests/minute)
                time.sleep(0.6)

            except Exception as e:
                error_msg = f"Game {game_id}: {str(e)}"
                errors.append(error_msg)
                if len(errors) <= 5:  # Only print first 5 errors
                    print(f"  [WARNING] {error_msg}")
                continue

        if len(errors) > 5:
            print(f"  [WARNING] ... and {len(errors) - 5} more errors")

        if len(all_player_stats) == 0:
            print("[ERROR] No player statistics retrieved")
            return

        # Combine all player stats
        combined_stats = pd.concat(all_player_stats, ignore_index=True)
        print(f"[OK] Retrieved {len(combined_stats)} player-game records from {len(all_player_stats)} games")

        # Step 3: Transform to database schema
        print(f"\n[3/3] Transforming data to database schema...")
        transformed_df = self._transform_to_schema(combined_stats)
        print(f"[OK] Transformed {len(transformed_df)} records")

        # Step 4: Load to database
        if self.dry_run:
            print("\n[DRY RUN] Would insert records into database (skipped)")
            print(f"[DRY RUN] Sample record:")
            print(transformed_df.head(1).to_dict('records')[0])
        else:
            print(f"\n[4/4] Loading {len(transformed_df)} records to database...")
            self._load_to_database(transformed_df)
            print("[OK] Records loaded successfully")

        print(f"\n[OK] Acquisition complete!")

    def _fetch_season_games(self, season_str: str):
        """Fetch all games for a season using NBA API."""
        try:
            # Use LeagueGameFinder to get all games
            # Note: This returns team-game records (each game appears twice)
            gamefinder = leaguegamefinder.LeagueGameFinder(
                season_nullable=season_str,
                league_id_nullable='00',  # NBA
                season_type_nullable='Regular Season'
            )

            games_df = gamefinder.get_data_frames()[0]

            # Also get playoffs
            try:
                playoff_finder = leaguegamefinder.LeagueGameFinder(
                    season_nullable=season_str,
                    league_id_nullable='00',
                    season_type_nullable='Playoffs'
                )
                playoffs_df = playoff_finder.get_data_frames()[0]

                if len(playoffs_df) > 0:
                    games_df = pd.concat([games_df, playoffs_df], ignore_index=True)
                    print(f"  -> Regular season: {len(gamefinder.get_data_frames()[0]) // 2} games")
                    print(f"  -> Playoffs: {len(playoffs_df) // 2} games")

            except Exception as e:
                print(f"  [INFO] No playoffs data available: {e}")

            return games_df

        except Exception as e:
            print(f"[ERROR] Failed to fetch games: {e}")
            return None

    def _determine_season_id(self, game_date_str: str, season_end_year: int):
        """
        Determine season_id from game date.

        Season ID format:
        - 1YYYY = Preseason
        - 2YYYY = Regular Season
        - 3YYYY = All-Star
        - 4YYYY = Playoffs

        Args:
            game_date_str: Game date string (e.g., "2024-06-15")
            season_end_year: Season ending year

        Returns:
            Integer season_id
        """
        try:
            game_date = pd.to_datetime(game_date_str)

            # Determine season year (Oct-Dec uses previous calendar year)
            if game_date.month >= 10:
                season_year = game_date.year
            else:
                season_year = game_date.year - 1

            # Determine season type based on month
            # Regular season: October - April (roughly)
            # Playoffs: April - June (roughly)
            if game_date.month >= 4 and game_date.month <= 6:
                # Could be playoffs or late regular season
                # Default to playoffs if in May-June
                if game_date.month >= 5:
                    return int(f"4{season_year}")
                else:
                    # April could be either - default to regular season
                    return int(f"2{season_year}")
            else:
                # October - March: Regular season
                return int(f"2{season_year}")

        except Exception as e:
            print(f"[WARNING] Error determining season_id for {game_date_str}: {e}")
            # Default to regular season
            return int(f"2{season_end_year - 1}")

    def _transform_to_schema(self, stats_df: pd.DataFrame):
        """
        Transform NBA API box score format to player_game_stats_silver schema.

        NBA API columns include:
        - GAME_ID, TEAM_ID, TEAM_ABBREVIATION, PLAYER_ID, PLAYER_NAME
        - MIN (minutes as "MM:SS"), FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT
        - FTM, FTA, FT_PCT, OREB, DREB, REB, AST, STL, BLK, TOV, PF, PTS, PLUS_MINUS

        Database schema (player_game_stats_silver):
        - game_id, player_id, player_name, team_id, team_abbreviation
        - min, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct
        - ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, tov, pf, pts
        - plus_minus, season_id, game_date
        """
        transformed = pd.DataFrame()

        # Direct mappings (columns with same name)
        direct_map = {
            'GAME_ID': 'game_id',
            'PLAYER_ID': 'player_id',
            'PLAYER_NAME': 'player_name',
            'TEAM_ID': 'team_id',
            'TEAM_ABBREVIATION': 'team_abbreviation',
            'FGM': 'fgm',
            'FGA': 'fga',
            'FG_PCT': 'fg_pct',
            'FG3M': 'fg3m',
            'FG3A': 'fg3a',
            'FG3_PCT': 'fg3_pct',
            'FTM': 'ftm',
            'FTA': 'fta',
            'FT_PCT': 'ft_pct',
            'OREB': 'oreb',
            'DREB': 'dreb',
            'REB': 'reb',
            'AST': 'ast',
            'STL': 'stl',
            'BLK': 'blk',
            'TOV': 'tov',
            'PF': 'pf',
            'PTS': 'pts',
            'PLUS_MINUS': 'plus_minus',
        }

        for nba_col, db_col in direct_map.items():
            if nba_col in stats_df.columns:
                transformed[db_col] = stats_df[nba_col]

        # Convert minutes from "MM:SS" to total seconds
        if 'MIN' in stats_df.columns:
            transformed['min'] = stats_df['MIN'].apply(self._convert_minutes_to_seconds)
        else:
            transformed['min'] = None

        # Add game metadata
        if 'GAME_DATE' in stats_df.columns:
            transformed['game_date'] = pd.to_datetime(stats_df['GAME_DATE']).dt.date

        if 'SEASON_ID' in stats_df.columns:
            transformed['season_id'] = stats_df['SEASON_ID']

        # Convert percentages from 0.0-1.0 to 0-100 integers (if needed)
        for pct_col in ['fg_pct', 'fg3_pct', 'ft_pct']:
            if pct_col in transformed.columns:
                # NBA API returns percentages as 0.0-1.0 decimals
                transformed[pct_col] = (transformed[pct_col] * 100).fillna(0).astype(int)

        # Handle NULL values for players who didn't play (DNP)
        # Set all stats to 0 or NULL as appropriate
        dnp_mask = transformed['min'].isna() | (transformed['min'] == 0)
        stat_columns = ['fgm', 'fga', 'fg3m', 'fg3a', 'ftm', 'fta', 'oreb', 'dreb', 'reb',
                       'ast', 'stl', 'blk', 'tov', 'pf', 'pts']

        for col in stat_columns:
            if col in transformed.columns:
                transformed.loc[dnp_mask, col] = 0

        return transformed

    def _convert_minutes_to_seconds(self, min_str):
        """Convert minutes string 'MM:SS' to total seconds."""
        if pd.isna(min_str) or min_str is None or min_str == '':
            return 0

        try:
            if isinstance(min_str, str):
                parts = min_str.split(':')
                if len(parts) == 2:
                    minutes = int(parts[0])
                    seconds = int(parts[1])
                    return minutes * 60 + seconds
                else:
                    return 0
            else:
                # Already a number
                return int(min_str)
        except Exception as e:
            return 0

    def _load_to_database(self, df: pd.DataFrame):
        """Load transformed data to database."""
        if not self.conn:
            print("[ERROR] No database connection")
            return

        try:
            # Create temporary table for import
            self.conn.execute("DROP TABLE IF EXISTS player_boxscore_import_temp")
            self.conn.execute("CREATE TABLE player_boxscore_import_temp AS SELECT * FROM df")

            # Insert into player_game_stats_silver (using INSERT OR IGNORE to skip duplicates)
            result = self.conn.execute("""
                INSERT OR IGNORE INTO player_game_stats_silver
                SELECT * FROM player_boxscore_import_temp
            """)

            rows_inserted = result.fetchall()[0][0] if result else 0
            print(f"  -> Inserted {rows_inserted} new records (duplicates skipped)")

            # Clean up
            self.conn.execute("DROP TABLE IF EXISTS player_boxscore_import_temp")

        except Exception as e:
            print(f"[ERROR] Failed to load data: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Acquire recent NBA player box scores using NBA.com API"
    )
    parser.add_argument(
        '--season',
        type=str,
        required=True,
        help='Season ending year (2024, 2025, 2026) or "all" for all recent seasons'
    )
    parser.add_argument(
        '--db-path',
        type=str,
        default='c:\\Users\\nicolas\\Documents\\GitHub\\nba_hub\\nba.duckdb',
        help='Path to DuckDB database file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Fetch data but do not insert into database'
    )

    args = parser.parse_args()

    # Determine which seasons to acquire
    if args.season.lower() == 'all':
        seasons = [2024, 2025]  # 2026 season hasn't started yet
    else:
        try:
            season_year = int(args.season)
            if season_year not in [2024, 2025, 2026]:
                print(f"[ERROR] Invalid season year: {season_year}")
                print("[INFO] Valid seasons: 2024, 2025, 2026, or 'all'")
                return
            seasons = [season_year]
        except ValueError:
            print(f"[ERROR] Invalid season format: {args.season}")
            return

    # Create acquisition instance
    acquisition = NBAAPIPlayerBoxScoreAcquisition(
        db_path=args.db_path,
        dry_run=args.dry_run
    )

    # Connect to database
    acquisition.connect_db()

    try:
        # Acquire each season
        for season in seasons:
            acquisition.acquire_season(season)
            print()

    finally:
        # Always close database connection
        acquisition.close_db()


if __name__ == '__main__':
    main()
