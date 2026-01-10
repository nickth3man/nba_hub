#!/usr/bin/env python3
"""
NBA Data Ingestion Script using Official NBA API
Fills missing player box scores and game schedules in DuckDB database
"""

import duckdb
import pandas as pd
from nba_api.stats.endpoints import leaguegamelog, boxscoretraditionalv3
import time
import logging
from typing import List, Dict, Set

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class NBADataIngestion:
    def __init__(self, db_path: str = "nba.duckdb"):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
        self._ensure_tables()
        logger.info(f"Connected to database: {db_path}")

    def _ensure_tables(self):
        """Ensure required tables exist with correct schema"""
        # Create tables if they don't exist
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS br_player_box_scores (
                game_id VARCHAR,
                game_date DATE,
                season_id VARCHAR,
                player_name VARCHAR,
                player_id INTEGER,
                team_abbreviation VARCHAR,
                min VARCHAR,
                fgm INTEGER,
                fga INTEGER,
                fg_pct DOUBLE,
                fg3m INTEGER,
                fg3a INTEGER,
                fg3_pct DOUBLE,
                ftm INTEGER,
                fta INTEGER,
                ft_pct DOUBLE,
                oreb INTEGER,
                dreb INTEGER,
                reb INTEGER,
                ast INTEGER,
                stl INTEGER,
                blk INTEGER,
                tov INTEGER,
                pf INTEGER,
                pts INTEGER,
                plus_minus DOUBLE,
                comment VARCHAR
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS br_schedule (
                game_id VARCHAR,
                game_date DATE,
                season_id VARCHAR,
                team_abbreviation VARCHAR,
                opponent VARCHAR,
                location VARCHAR,
                wl VARCHAR,
                pts INTEGER,
                opponent_pts INTEGER
            )
        """)

        # Check if tables exist and add missing columns for existing tables
        try:
            # Check br_player_box_scores
            existing_columns = self.conn.execute(
                "DESCRIBE br_player_box_scores"
            ).fetchall()
            column_names = [row[0] for row in existing_columns]

            missing_columns = []
            if "season_id" not in column_names:
                missing_columns.append("ADD COLUMN season_id VARCHAR")
            if "player_id" not in column_names:
                missing_columns.append("ADD COLUMN player_id INTEGER")
            if "comment" not in column_names:
                missing_columns.append("ADD COLUMN comment VARCHAR")

            if missing_columns:
                alter_sql = (
                    f"ALTER TABLE br_player_box_scores {', '.join(missing_columns)}"
                )
                self.conn.execute(alter_sql)
                logger.info(
                    f"Added missing columns to br_player_box_scores: {missing_columns}"
                )

        except Exception as e:
            logger.warning(f"Error checking table schemas: {e}")

        # Add indexes for performance if they don't exist
        try:
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_box_scores_game_id ON br_player_box_scores(game_id)"
            )
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_box_scores_season ON br_player_box_scores(season_id)"
            )
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_schedule_game_date ON br_schedule(game_date)"
            )
            self.conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_schedule_season ON br_schedule(season_id)"
            )
        except Exception as e:
            logger.warning(f"Error creating indexes: {e}")

        logger.info("Database tables and indexes verified")

    def get_existing_game_ids(self) -> Set[str]:
        """Get set of game_ids already in database"""
        try:
            result = self.conn.execute(
                "SELECT DISTINCT game_id FROM br_player_box_scores"
            ).fetchall()
            return {row[0] for row in result} if result else set()
        except Exception as e:
            logger.warning(f"Could not get existing games: {e}")
            return set()

    def get_existing_seasons(self) -> List[str]:
        """Get list of seasons already in player box scores table"""
        try:
            result = self.conn.execute("""
                SELECT DISTINCT season_id 
                FROM br_player_box_scores 
                ORDER BY season_id
            """).fetchall()
            return [row[0] for row in result] if result else []
        except Exception as e:
            logger.warning(f"Could not get existing seasons: {e}")
            return []

    def get_season_games(
        self, season: str, season_type: str = "Regular Season"
    ) -> List[str]:
        """Get all game IDs for a season using LeagueGameLog"""
        try:
            logger.info(f"Fetching games for {season} ({season_type})...")

            # Use LeagueGameLog endpoint for comprehensive game data
            gamelog = leaguegamelog.LeagueGameLog(
                season=season,
                season_type_all_star=season_type,
                player_or_team_abbreviation="T",  # Team stats
            )

            df = gamelog.get_data_frames()[0]

            if df.empty:
                logger.warning(f"No games found for {season} ({season_type})")
                return []

            game_ids = df["GAME_ID"].unique().tolist()
            logger.info(f"Found {len(game_ids)} games for {season} ({season_type})")
            return game_ids

        except Exception as e:
            logger.error(f"Error getting games for {season}: {e}")
            return []

    def get_games_with_dates(
        self, season: str, season_type: str = "Regular Season"
    ) -> pd.DataFrame:
        """Get games with their dates for a season"""
        try:
            gamelog = leaguegamelog.LeagueGameLog(
                season=season, season_type_all_star=season_type
            )

            df = gamelog.get_data_frames()[0]

            if df.empty:
                return pd.DataFrame()

            # Create schedule dataframe
            schedule_data = []
            for _, row in df.iterrows():
                game_id = row["GAME_ID"]
                game_date = pd.to_datetime(row["GAME_DATE"]).date()
                team_abbrev = row["TEAM_ABBREVIATION"]
                matchup = row["MATCHUP"]
                wl = row["WL"]
                pts = row["PTS"]

                # Parse opponent from matchup
                if "@" in matchup:
                    opponent = matchup.split(" @ ")[1]
                    location = "AWAY" if matchup.startswith(team_abbrev) else "HOME"
                elif "vs." in matchup:
                    opponent = matchup.split(" vs. ")[1]
                    location = "HOME" if matchup.startswith(team_abbrev) else "AWAY"
                else:
                    opponent = "UNKNOWN"
                    location = "NEUTRAL"

                schedule_data.append(
                    {
                        "game_id": game_id,
                        "game_date": game_date,
                        "season_id": season,
                        "team_abbreviation": team_abbrev,
                        "opponent": opponent,
                        "location": location,
                        "wl": wl,
                        "pts": pts,
                    }
                )

            return pd.DataFrame(schedule_data)

        except Exception as e:
            logger.error(f"Error getting games with dates: {e}")
            return pd.DataFrame()

    def ingest_game_schedule(self, season: str) -> int:
        """Ingest complete game schedule for a season"""
        try:
            # Get regular season games
            reg_schedule = self.get_games_with_dates(season, "Regular Season")
            reg_count = 0

            if not reg_schedule.empty:
                self.conn.execute("""
                    INSERT OR IGNORE INTO br_schedule
                    SELECT game_id, game_date, season_id, team_abbreviation,
                           opponent, location, wl, pts, NULL
                    FROM reg_schedule
                """)
                reg_count = len(reg_schedule)

            # Get playoff games
            playoff_schedule = self.get_games_with_dates(season, "Playoffs")
            playoff_count = 0

            if not playoff_schedule.empty:
                self.conn.execute("""
                    INSERT OR IGNORE INTO br_schedule
                    SELECT game_id, game_date, season_id, team_abbreviation,
                           opponent, location, wl, pts, NULL
                    FROM playoff_schedule
                """)
                playoff_count = len(playoff_schedule)

            total_count = reg_count + playoff_count
            logger.info(
                f"Added {total_count} schedule entries for {season} ({reg_count} reg, {playoff_count} playoff)"
            )
            return total_count

        except Exception as e:
            logger.error(f"Error ingesting schedule for {season}: {e}")
            return 0

    def ingest_player_box_scores(self, season: str) -> int:
        """Ingest all player box scores for a season"""
        try:
            existing_games = self.get_existing_game_ids()

            # Get games for both regular season and playoffs
            reg_games = self.get_season_games(season, "Regular Season")
            playoff_games = self.get_season_games(season, "Playoffs")
            all_games = reg_games + playoff_games

            if not all_games:
                logger.warning(f"No games found for {season}")
                return 0

            # Filter out already processed games
            new_games = [gid for gid in all_games if gid not in existing_games]

            if not new_games:
                logger.info(
                    f"All {len(all_games)} games already have box scores for {season}"
                )
                return 0

            logger.info(
                f"Processing {len(new_games)} new games for {season} box scores..."
            )

            total_box_scores = 0
            for i, game_id in enumerate(new_games):
                try:
                    box_count = self._process_single_game_box_score(game_id, season)
                    total_box_scores += box_count

                    if (i + 1) % 10 == 0:
                        logger.info(
                            f"Processed {i + 1}/{len(new_games)} games for {season} ({total_box_scores} total box scores)"
                        )

                    # Rate limiting - NBA API has limits
                    time.sleep(0.8)

                except Exception as e:
                    logger.error(f"Error processing game {game_id}: {e}")
                    continue

            logger.info(f"Total box scores added for {season}: {total_box_scores}")
            return total_box_scores

        except Exception as e:
            logger.error(f"Error ingesting box scores for {season}: {e}")
            return 0

    def _process_single_game_box_score(self, game_id: str, season: str) -> int:
        """Process box scores for a single game"""
        try:
            # Get box score data
            box_score = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=game_id)
            df = box_score.get_data_frames()[0]

            if df.empty:
                logger.warning(f"No box score data for game {game_id}")
                return 0

            # Get game date from schedule
            game_date_result = self.conn.execute(
                "SELECT game_date FROM br_schedule WHERE game_id = ? LIMIT 1",
                [game_id],
            ).fetchone()

            game_date = game_date_result[0] if game_date_result else None

            # Transform and clean data
            df["game_id"] = game_id
            df["game_date"] = game_date
            df["season_id"] = season
            df["player_name"] = df["firstName"] + " " + df["familyName"]

            # Map columns to our schema with proper NBA API field names
            column_mapping = {
                "personId": "player_id",
                "teamTricode": "team_abbreviation",
                "minutes": "min",
                "fieldGoalsMade": "fgm",
                "fieldGoalsAttempted": "fga",
                "fieldGoalsPercentage": "fg_pct",
                "threePointersMade": "fg3m",
                "threePointersAttempted": "fg3a",
                "threePointersPercentage": "fg3_pct",
                "freeThrowsMade": "ftm",
                "freeThrowsAttempted": "fta",
                "freeThrowsPercentage": "ft_pct",
                "reboundsOffensive": "oreb",
                "reboundsDefensive": "dreb",
                "reboundsTotal": "reb",
                "assists": "ast",
                "steals": "stl",
                "blocks": "blk",
                "turnovers": "tov",
                "foulsPersonal": "pf",
                "points": "pts",
                "plusMinusPoints": "plus_minus",
                "comment": "comment",
            }

            df = df.rename(columns=column_mapping)

            # Select columns in our schema order
            columns = [
                "game_id",
                "game_date",
                "player_name",
                "player_id",
                "team_abbreviation",
                "min",
                "fgm",
                "fga",
                "fg_pct",
                "fg3m",
                "fg3a",
                "fg3_pct",
                "ftm",
                "fta",
                "ft_pct",
                "oreb",
                "dreb",
                "reb",
                "ast",
                "stl",
                "blk",
                "tov",
                "pf",
                "pts",
                "plus_minus",
                "season_id",
                "comment",
            ]

            # Ensure all columns exist, fill missing with None
            for col in columns:
                if col not in df.columns:
                    df[col] = None

            df = df[columns]

            # Insert into database
            self.conn.execute("INSERT INTO br_player_box_scores SELECT * FROM df")

            return len(df)

        except Exception as e:
            logger.error(f"Error processing box score for game {game_id}: {e}")
            return 0

    def process_season(self, season: str) -> Dict:
        """Process complete season (schedule + box scores)"""
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Processing season: {season}")
        logger.info("=" * 60)

        result = {
            "season": season,
            "schedule_entries": 0,
            "box_scores": 0,
            "success": False,
            "duration": 0,
        }

        start_time = time.time()

        try:
            result["schedule_entries"] = self.ingest_game_schedule(season)
            result["box_scores"] = self.ingest_player_box_scores(season)
            result["success"] = result["box_scores"] > 0
            result["duration"] = time.time() - start_time

            logger.info(f"Season {season} complete:")
            logger.info(f"  Schedule Entries: {result['schedule_entries']}")
            logger.info(f"  Box Scores: {result['box_scores']} player stats")
            logger.info(f"  Duration: {result['duration']:.1f} seconds")

        except Exception as e:
            logger.error(f"Error processing season {season}: {e}")
            result["duration"] = time.time() - start_time

        return result

    def verify_data(self, season: str) -> bool:
        """Verify data was ingested correctly"""
        try:
            # Check box scores
            box_count = self.conn.execute(
                """
                SELECT COUNT(*)
                FROM br_player_box_scores
                WHERE season_id = ?
            """,
                [season],
            ).fetchone()[0]

            # Check schedule
            schedule_count = self.conn.execute(
                """
                SELECT COUNT(*)
                FROM br_schedule
                WHERE season_id = ?
            """,
                [season],
            ).fetchone()[0]

            logger.info(
                f"Verification for {season}: {box_count} box scores, {schedule_count} scheduled games"
            )
            return box_count > 0 and schedule_count > 0

        except Exception as e:
            logger.error(f"Error verifying data for {season}: {e}")
            return False

    def get_database_stats(self) -> Dict:
        """Get comprehensive database statistics"""
        try:
            stats = {}

            # Box scores stats
            box_stats = self.conn.execute("""
                SELECT
                    COUNT(*) as total,
                    COUNT(DISTINCT game_id) as games,
                    COUNT(DISTINCT season_id) as seasons,
                    COUNT(DISTINCT player_id) as players,
                    MIN(game_date) as earliest_date,
                    MAX(game_date) as latest_date
                FROM br_player_box_scores
            """).fetchone()

            if box_stats:
                stats["box_scores"] = {
                    "total": box_stats[0],
                    "games": box_stats[1],
                    "seasons": box_stats[2],
                    "players": box_stats[3],
                    "date_range": f"{box_stats[4]} to {box_stats[5]}"
                    if box_stats[4]
                    else None,
                }
            else:
                stats["box_scores"] = {}

            # Schedule stats
            sched_stats = self.conn.execute("""
                SELECT
                    COUNT(*) as total,
                    COUNT(DISTINCT season_id) as seasons,
                    MIN(game_date) as earliest_date,
                    MAX(game_date) as latest_date
                FROM br_schedule
            """).fetchone()

            if sched_stats:
                stats["schedule"] = {
                    "total": sched_stats[0],
                    "seasons": sched_stats[1],
                    "date_range": f"{sched_stats[2]} to {sched_stats[3]}"
                    if sched_stats[2]
                    else None,
                }
            else:
                stats["schedule"] = {}

            return stats

        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}

    def get_seasons_to_process(
        self, start_season: str = "1999-2000", end_season: str = "2025-2026"
    ) -> List[str]:
        """Generate list of seasons to process"""
        seasons = []
        start_year = int(start_season.split("-")[0])
        end_year = int(end_season.split("-")[0])

        for year in range(start_year, end_year + 1):
            season_id = f"{year}-{str(year + 1)[-2:]}"
            seasons.append(season_id)

        # Remove seasons already processed
        existing = self.get_existing_seasons()
        seasons_to_process = [s for s in seasons if s not in existing]

        logger.info(
            f"Seasons to process: {len(seasons_to_process)} (already have: {len(existing)})"
        )
        return seasons_to_process

    def run_batch_ingestion(
        self, start_season: str = "1999-2000", end_season: str = "2025-2026"
    ):
        """Run batch ingestion for multiple seasons"""
        # Generate season list
        seasons = []
        start_year = int(start_season.split("-")[0])
        end_year = int(end_season.split("-")[0])

        for year in range(start_year, end_year + 1):
            season_id = f"{year}-{str(year + 1)[-2:]}"
            seasons.append(season_id)

        logger.info(f"\n{'=' * 80}")
        logger.info(
            f"Starting batch ingestion for {len(seasons)} seasons: {start_season} to {end_season}"
        )
        logger.info("=" * 80)

        results = []
        batch_start = time.time()

        for i, season in enumerate(seasons):
            result = self.process_season(season)
            results.append(result)

            # Brief pause between seasons
            if i < len(seasons) - 1:
                time.sleep(1)

        # Summary
        batch_duration = time.time() - batch_start
        successful = sum(1 for r in results if r["success"])
        total_box_scores = sum(r["box_scores"] for r in results)

        logger.info(f"\n{'=' * 80}")
        logger.info("BATCH INGESTION COMPLETE!")
        logger.info("=" * 80)
        logger.info(f"Successful seasons: {successful}/{len(seasons)}")
        logger.info(f"Total box scores added: {total_box_scores}")
        logger.info(f"Total batch duration: {batch_duration:.1f} seconds")

        return results

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


def main():
    """Main function"""
    logger.info("=" * 80)
    logger.info("NBA Data Ingestion Script - Official NBA API")
    logger.info("=" * 80)

    ingestion = NBADataIngestion()

    try:
        # Show current stats
        logger.info("\nCurrent database statistics:")
        stats = ingestion.get_database_stats()

        if stats.get("box_scores"):
            logger.info("Box Scores:")
            for key, value in stats["box_scores"].items():
                logger.info(f"  {key}: {value}")

        if stats.get("schedule"):
            logger.info("Schedule:")
            for key, value in stats["schedule"].items():
                logger.info(f"  {key}: {value}")

        # Test with a recent season first
        logger.info("\nTesting with 2023-24 season...")
        test_result = ingestion.process_season("2023-24")

        if test_result["success"]:
            logger.info("\nTest successful! Starting full batch ingestion...")
            # Run batch ingestion for recent seasons
            ingestion.run_batch_ingestion("2020-21", "2024-25")
        else:
            logger.warning("Test failed - check API connectivity")

        # Show final stats
        logger.info("\nFinal database statistics:")
        final_stats = ingestion.get_database_stats()

        if final_stats.get("box_scores"):
            logger.info("Box Scores:")
            for key, value in final_stats["box_scores"].items():
                logger.info(f"  {key}: {value}")

        if final_stats.get("schedule"):
            logger.info("Schedule:")
            for key, value in final_stats["schedule"].items():
                logger.info(f"  {key}: {value}")

    except KeyboardInterrupt:
        logger.info("\nIngestion interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        ingestion.close()


if __name__ == "__main__":
    main()
