"""
NBA Database Validation Script

Validates the completeness and accuracy of the NBA DuckDB database
against known NBA history from 1946-2026.

Usage:
    python validate_nba_database.py [--db-path PATH] [--output-dir DIR]

Requirements:
    - duckdb>=0.9.0
    - pandas>=2.0.0
    - numpy>=1.24.0
"""

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
import argparse


class NBADatabaseValidator:
    """Validates NBA database completeness and quality."""

    def __init__(self, db_path: str, output_dir: str = None):
        """Initialize validator with database path."""
        self.db_path = Path(db_path)
        self.output_dir = Path(output_dir) if output_dir else self.db_path.parent / "nba_database_documentation"
        self.conn = None
        self.validation_results = []

        # Expected NBA history data
        self.EXPECTED_SEASONS = self._define_expected_seasons()
        self.EXPECTED_TEAM_COUNTS = self._define_expected_team_counts()
        self.LOCKOUT_SEASONS = {
            '1998-99': 50,  # games per team
            '2011-12': 66,
            '2019-20': 72  # approximate, COVID shortened
        }

    def _define_expected_seasons(self):
        """Define all expected NBA/BAA seasons from 1946-2026."""
        seasons = []

        # Generate season IDs: 1946-47, 1947-48, etc.
        for year in range(1946, 2026):
            season_id = f"{year}-{str(year + 1)[-2:]}"
            era = "BAA" if year < 1949 else "NBA"
            status = "COMPLETED"

            # Mark in-progress season
            if year == 2025:
                status = "IN_PROGRESS"

            seasons.append({
                'season_id': season_id,
                'start_year': year,
                'end_year': year + 1,
                'era': era,
                'status': status
            })

        return pd.DataFrame(seasons)

    def _define_expected_team_counts(self):
        """Define expected team counts per season based on NBA expansion history."""
        # Key expansion/contraction points
        team_counts = {
            '1946-47': 11,  # BAA founding
            '1947-48': 8,   # Contraction
            '1948-49': 12,  # Expansion
            '1949-50': 17,  # NBA-NBL merger
            '1950-51': 11,
            '1951-52': 10,
            '1952-53': 10,
            '1953-54': 9,
            '1954-55': 8,   # Major contraction
            '1961-62': 9,   # Chicago Packers added
            '1966-67': 10,  # Chicago Bulls added
            '1967-68': 12,  # Rockets, SuperSonics added
            '1968-69': 14,  # Bucks, Suns added
            '1970-71': 17,  # Blazers, Cavaliers, Braves added
            '1974-75': 18,  # Jazz added
            '1976-77': 22,  # ABA merger: Nuggets, Pacers, Spurs, Nets
            '1980-81': 23,  # Mavericks added
            '1988-89': 25,  # Heat, Hornets added
            '1989-90': 27,  # Magic, Timberwolves added
            '1995-96': 29,  # Raptors, Grizzlies added
            '2004-05': 30,  # Bobcats added - modern era begins
        }

        # Fill in gaps (stable periods)
        all_seasons = {}
        current_count = 11

        for season_data in self.EXPECTED_SEASONS.itertuples():
            season = season_data.season_id
            if season in team_counts:
                current_count = team_counts[season]
            all_seasons[season] = current_count

        return all_seasons

    def connect(self):
        """Connect to the DuckDB database."""
        try:
            if not self.db_path.exists():
                print(f"[ERROR] Database not found: {self.db_path}")
                sys.exit(1)

            print(f"[INFO] Connecting to database: {self.db_path}")
            self.conn = duckdb.connect(str(self.db_path), read_only=True)
            print(f"[OK] Connected successfully")

        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            sys.exit(1)

    def disconnect(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print("[INFO] Database connection closed")

    def add_result(self, check_name, status, details, severity="INFO"):
        """Add validation result."""
        self.validation_results.append({
            'check': check_name,
            'status': status,  # PASS, FAIL, WARNING, INFO
            'severity': severity,  # CRITICAL, HIGH, MEDIUM, LOW, INFO
            'details': details
        })

    def validate_season_coverage(self):
        """Validate which seasons exist in the database."""
        print("\n" + "=" * 60)
        print("VALIDATING SEASON COVERAGE")
        print("=" * 60)

        try:
            # Try to find season information from games table
            query = """
                SELECT DISTINCT
                    season_id,
                    COUNT(DISTINCT game_id) as game_count,
                    MIN(game_date) as first_game,
                    MAX(game_date) as last_game
                FROM games
                GROUP BY season_id
                ORDER BY season_id
            """
            db_seasons = self.conn.execute(query).fetchdf()

            print(f"[INFO] Found {len(db_seasons)} seasons in database")

            # Compare with expected seasons
            expected_count = len(self.EXPECTED_SEASONS[self.EXPECTED_SEASONS['status'] == 'COMPLETED'])
            expected_count_with_progress = len(self.EXPECTED_SEASONS)

            print(f"[INFO] Expected completed seasons: {expected_count} (1946-47 to 2024-25)")
            print(f"[INFO] Expected total seasons: {expected_count_with_progress} (including in-progress)")

            # Find missing seasons
            db_season_ids = set(db_seasons['season_id'].tolist())
            expected_season_ids = set(self.EXPECTED_SEASONS['season_id'].tolist())
            missing_seasons = expected_season_ids - db_season_ids

            if missing_seasons:
                missing_sorted = sorted(missing_seasons)
                print(f"\n[WARNING] Missing {len(missing_seasons)} seasons:")
                for season in missing_sorted:
                    era_info = self.EXPECTED_SEASONS[self.EXPECTED_SEASONS['season_id'] == season]
                    if not era_info.empty:
                        era = era_info.iloc[0]['era']
                        status = era_info.iloc[0]['status']
                        print(f"  - {season} ({era}, {status})")

                self.add_result(
                    "Season Coverage",
                    "FAIL",
                    f"Missing {len(missing_seasons)} seasons: {', '.join(missing_sorted[:5])}{'...' if len(missing_sorted) > 5 else ''}",
                    "CRITICAL" if len(missing_seasons) > 5 else "HIGH"
                )
            else:
                print("[OK] All expected seasons found!")
                self.add_result("Season Coverage", "PASS", "All expected seasons present", "INFO")

            # Check for unexpected seasons
            unexpected_seasons = db_season_ids - expected_season_ids
            if unexpected_seasons:
                print(f"\n[WARNING] Found {len(unexpected_seasons)} unexpected seasons:")
                for season in sorted(unexpected_seasons):
                    print(f"  - {season}")
                self.add_result(
                    "Season Coverage",
                    "WARNING",
                    f"Unexpected seasons found: {', '.join(sorted(unexpected_seasons))}",
                    "LOW"
                )

            # Display season summary
            print(f"\n[INFO] Season Summary:")
            print(f"  Database seasons: {len(db_seasons)}")
            print(f"  Expected seasons: {expected_count_with_progress}")
            print(f"  Missing: {len(missing_seasons)}")
            print(f"  Coverage: {(len(db_seasons) / expected_count_with_progress * 100):.1f}%")

            return db_seasons, missing_seasons

        except Exception as e:
            print(f"[ERROR] Season validation failed: {e}")
            self.add_result("Season Coverage", "FAIL", f"Error: {e}", "CRITICAL")
            return None, None

    def validate_team_counts(self, db_seasons):
        """Validate team counts per season against expected NBA history."""
        print("\n" + "=" * 60)
        print("VALIDATING TEAM COUNTS PER SEASON")
        print("=" * 60)

        try:
            query = """
                SELECT
                    season_id,
                    COUNT(DISTINCT team_id) as team_count
                FROM team_game_stats
                GROUP BY season_id
                ORDER BY season_id
            """
            team_counts = self.conn.execute(query).fetchdf()

            print(f"[INFO] Analyzing team counts for {len(team_counts)} seasons")

            mismatches = []
            for _, row in team_counts.iterrows():
                season = row['season_id']
                actual_count = row['team_count']
                expected_count = self.EXPECTED_TEAM_COUNTS.get(season)

                if expected_count and actual_count != expected_count:
                    mismatches.append({
                        'season': season,
                        'expected': expected_count,
                        'actual': actual_count,
                        'difference': actual_count - expected_count
                    })

            if mismatches:
                print(f"\n[WARNING] Found {len(mismatches)} seasons with team count mismatches:")
                for m in mismatches[:10]:  # Show first 10
                    print(f"  - {m['season']}: Expected {m['expected']}, Found {m['actual']} (diff: {m['difference']:+d})")

                if len(mismatches) > 10:
                    print(f"  ... and {len(mismatches) - 10} more")

                self.add_result(
                    "Team Count Validation",
                    "FAIL",
                    f"{len(mismatches)} seasons have incorrect team counts",
                    "HIGH"
                )
            else:
                print("[OK] All seasons have correct team counts!")
                self.add_result("Team Count Validation", "PASS", "Team counts match expectations", "INFO")

            # Show sample of team counts
            print(f"\n[INFO] Sample team counts by era:")
            sample_seasons = ['1946-47', '1954-55', '1976-77', '2004-05', '2022-23']
            for season in sample_seasons:
                season_data = team_counts[team_counts['season_id'] == season]
                if not season_data.empty:
                    actual = season_data.iloc[0]['team_count']
                    expected = self.EXPECTED_TEAM_COUNTS.get(season, 'N/A')
                    status = "[OK]" if actual == expected else "[MISMATCH]"
                    print(f"  {status} {season}: {actual} teams (expected: {expected})")

            return team_counts, mismatches

        except Exception as e:
            print(f"[ERROR] Team count validation failed: {e}")
            self.add_result("Team Count Validation", "FAIL", f"Error: {e}", "CRITICAL")
            return None, None

    def validate_game_counts(self, db_seasons):
        """Validate game counts per season."""
        print("\n" + "=" * 60)
        print("VALIDATING GAME COUNTS PER SEASON")
        print("=" * 60)

        try:
            query = """
                SELECT
                    season_id,
                    COUNT(*) as total_games,
                    COUNT(DISTINCT game_id) as unique_games,
                    MIN(game_date) as first_game,
                    MAX(game_date) as last_game
                FROM games
                GROUP BY season_id
                ORDER BY season_id DESC
                LIMIT 10
            """
            recent_games = self.conn.execute(query).fetchdf()

            print(f"[INFO] Recent season game counts:")
            for _, row in recent_games.iterrows():
                season = row['season_id']
                games = row['unique_games']
                date_range = f"{row['first_game']} to {row['last_game']}"

                # Expected games for modern era (rough estimate)
                if season in self.LOCKOUT_SEASONS:
                    expected_approx = (30 * self.LOCKOUT_SEASONS[season]) // 2
                    note = f"(lockout season, ~{expected_approx} expected)"
                elif season >= '2004-05':
                    expected_approx = (30 * 82) // 2  # 1,230 games
                    note = f"(normal season, ~{expected_approx} expected)"
                else:
                    note = "(historical season)"

                print(f"  {season}: {games} games {note}")
                print(f"           Date range: {date_range}")

            # Check for duplicate game_ids
            dup_query = """
                SELECT game_id, COUNT(*) as dup_count
                FROM games
                GROUP BY game_id
                HAVING COUNT(*) > 1
            """
            duplicates = self.conn.execute(dup_query).fetchdf()

            if len(duplicates) > 0:
                print(f"\n[ERROR] Found {len(duplicates)} duplicate game_ids!")
                print(duplicates.head(10))
                self.add_result(
                    "Game Count Validation",
                    "FAIL",
                    f"{len(duplicates)} duplicate game IDs found",
                    "CRITICAL"
                )
            else:
                print("\n[OK] No duplicate game_ids found")
                self.add_result("Game Count Validation", "PASS", "No duplicate game IDs", "INFO")

            return recent_games

        except Exception as e:
            print(f"[ERROR] Game count validation failed: {e}")
            self.add_result("Game Count Validation", "FAIL", f"Error: {e}", "CRITICAL")
            return None

    def validate_player_coverage(self):
        """Validate player coverage and completeness."""
        print("\n" + "=" * 60)
        print("VALIDATING PLAYER COVERAGE")
        print("=" * 60)

        try:
            # Get player count by season
            query = """
                SELECT
                    COUNT(DISTINCT person_id) as total_players
                FROM common_player_info
            """
            player_count = self.conn.execute(query).fetchone()

            print(f"[INFO] Total unique players in database: {player_count[0]}")

            # Expected: ~4,500+ players in NBA history
            if player_count[0] < 4000:
                print(f"[WARNING] Player count seems low (expected 4,000+)")
                self.add_result(
                    "Player Coverage",
                    "WARNING",
                    f"Only {player_count[0]} players found (expected 4,000+)",
                    "MEDIUM"
                )
            else:
                print(f"[OK] Player count seems reasonable")
                self.add_result("Player Coverage", "PASS", f"{player_count[0]} players found", "INFO")

            # Check for Hall of Fame players (sample check)
            hof_players = [
                'Michael Jordan',
                'LeBron James',
                'Kobe Bryant',
                'Magic Johnson',
                'Larry Bird',
                'Kareem Abdul-Jabbar',
                'Bill Russell',
                'Wilt Chamberlain'
            ]

            print(f"\n[INFO] Checking for Hall of Fame players:")
            for player_name in hof_players:
                check_query = f"""
                    SELECT display_first_last, person_id
                    FROM common_player_info
                    WHERE display_first_last LIKE '%{player_name}%'
                    LIMIT 1
                """
                result = self.conn.execute(check_query).fetchdf()
                if len(result) > 0:
                    print(f"  [OK] Found: {result.iloc[0]['display_first_last']}")
                else:
                    print(f"  [MISSING] Not found: {player_name}")

        except Exception as e:
            print(f"[ERROR] Player coverage validation failed: {e}")
            self.add_result("Player Coverage", "FAIL", f"Error: {e}", "MEDIUM")

    def validate_statistical_integrity(self):
        """Validate statistical integrity and logical consistency."""
        print("\n" + "=" * 60)
        print("VALIDATING STATISTICAL INTEGRITY")
        print("=" * 60)

        try:
            # Check 1: FGM > FGA violations
            query1 = """
                SELECT COUNT(*) as violation_count
                FROM team_game_stats
                WHERE field_goals_made > field_goals_attempted
            """
            result1 = self.conn.execute(query1).fetchone()
            fgm_violations = result1[0]

            if fgm_violations > 0:
                print(f"[ERROR] Found {fgm_violations} cases where FGM > FGA")
                self.add_result(
                    "Statistical Integrity - FGM/FGA",
                    "FAIL",
                    f"{fgm_violations} violations found",
                    "CRITICAL"
                )
            else:
                print(f"[OK] No FGM > FGA violations")
                self.add_result("Statistical Integrity - FGM/FGA", "PASS", "No violations", "INFO")

            # Check 2: Negative statistics
            query2 = """
                SELECT COUNT(*) as violation_count
                FROM team_game_stats
                WHERE points < 0 OR rebounds < 0 OR assists < 0
            """
            result2 = self.conn.execute(query2).fetchone()
            negative_stats = result2[0]

            if negative_stats > 0:
                print(f"[ERROR] Found {negative_stats} cases with negative statistics")
                self.add_result(
                    "Statistical Integrity - Negative Stats",
                    "FAIL",
                    f"{negative_stats} violations found",
                    "CRITICAL"
                )
            else:
                print(f"[OK] No negative statistics")
                self.add_result("Statistical Integrity - Negative Stats", "PASS", "No violations", "INFO")

            # Check 3: 3-point stats before 1979-80
            query3 = """
                SELECT COUNT(*) as violation_count
                FROM team_game_stats tgs
                JOIN games g ON tgs.game_id = g.game_id
                WHERE g.season_id < '1979-80'
                  AND (tgs.three_pointers_made > 0 OR tgs.three_pointers_attempted > 0)
            """
            result3 = self.conn.execute(query3).fetchone()
            three_point_violations = result3[0]

            if three_point_violations > 0:
                print(f"[ERROR] Found {three_point_violations} games with 3-point stats before 1979-80")
                self.add_result(
                    "Statistical Integrity - 3PT Timeline",
                    "FAIL",
                    f"{three_point_violations} violations found",
                    "HIGH"
                )
            else:
                print(f"[OK] No 3-point statistics before 1979-80")
                self.add_result("Statistical Integrity - 3PT Timeline", "PASS", "No violations", "INFO")

            # Check 4: Two teams per game
            query4 = """
                SELECT game_id, COUNT(DISTINCT team_id) as team_count
                FROM team_game_stats
                GROUP BY game_id
                HAVING COUNT(DISTINCT team_id) != 2
            """
            result4 = self.conn.execute(query4).fetchdf()
            team_count_violations = len(result4)

            if team_count_violations > 0:
                print(f"[ERROR] Found {team_count_violations} games without exactly 2 teams")
                self.add_result(
                    "Statistical Integrity - Teams per Game",
                    "FAIL",
                    f"{team_count_violations} violations found",
                    "CRITICAL"
                )
            else:
                print(f"[OK] All games have exactly 2 teams")
                self.add_result("Statistical Integrity - Teams per Game", "PASS", "No violations", "INFO")

        except Exception as e:
            print(f"[ERROR] Statistical integrity validation failed: {e}")
            self.add_result("Statistical Integrity", "FAIL", f"Error: {e}", "HIGH")

    def validate_referential_integrity(self):
        """Validate foreign key relationships."""
        print("\n" + "=" * 60)
        print("VALIDATING REFERENTIAL INTEGRITY")
        print("=" * 60)

        try:
            # Check 1: team_game_stats -> team
            query1 = """
                SELECT COUNT(*) as orphan_count
                FROM team_game_stats tgs
                WHERE tgs.team_id IS NOT NULL
                  AND NOT EXISTS (SELECT 1 FROM team t WHERE t.id = tgs.team_id)
            """
            result1 = self.conn.execute(query1).fetchone()
            orphan_teams = result1[0]

            total_team_stats = self.conn.execute("SELECT COUNT(*) FROM team_game_stats").fetchone()[0]
            integrity_pct = ((total_team_stats - orphan_teams) / total_team_stats * 100) if total_team_stats > 0 else 0

            print(f"[INFO] team_game_stats -> team: {integrity_pct:.2f}% integrity")
            if orphan_teams > 0:
                print(f"  [WARNING] {orphan_teams} orphaned team_id references")
                self.add_result(
                    "Referential Integrity - Teams",
                    "WARNING",
                    f"{orphan_teams} orphaned team_id references ({integrity_pct:.2f}% integrity)",
                    "MEDIUM"
                )
            else:
                print(f"  [OK] 100% referential integrity")
                self.add_result("Referential Integrity - Teams", "PASS", "100% integrity", "INFO")

            # Check 2: team_game_stats -> games
            query2 = """
                SELECT COUNT(*) as orphan_count
                FROM team_game_stats tgs
                WHERE tgs.game_id IS NOT NULL
                  AND NOT EXISTS (SELECT 1 FROM games g WHERE g.game_id = tgs.game_id)
            """
            result2 = self.conn.execute(query2).fetchone()
            orphan_games = result2[0]

            integrity_pct = ((total_team_stats - orphan_games) / total_team_stats * 100) if total_team_stats > 0 else 0

            print(f"\n[INFO] team_game_stats -> games: {integrity_pct:.2f}% integrity")
            if orphan_games > 0:
                print(f"  [WARNING] {orphan_games} orphaned game_id references")
                self.add_result(
                    "Referential Integrity - Games",
                    "WARNING",
                    f"{orphan_games} orphaned game_id references ({integrity_pct:.2f}% integrity)",
                    "MEDIUM"
                )
            else:
                print(f"  [OK] 100% referential integrity")
                self.add_result("Referential Integrity - Games", "PASS", "100% integrity", "INFO")

        except Exception as e:
            print(f"[ERROR] Referential integrity validation failed: {e}")
            self.add_result("Referential Integrity", "FAIL", f"Error: {e}", "MEDIUM")

    def generate_report(self):
        """Generate validation report."""
        print("\n" + "=" * 60)
        print("GENERATING VALIDATION REPORT")
        print("=" * 60)

        # Create validation results DataFrame
        results_df = pd.DataFrame(self.validation_results)

        # Summary statistics
        total_checks = len(results_df)
        passed = len(results_df[results_df['status'] == 'PASS'])
        failed = len(results_df[results_df['status'] == 'FAIL'])
        warnings = len(results_df[results_df['status'] == 'WARNING'])

        print(f"\n[INFO] Validation Summary:")
        print(f"  Total checks: {total_checks}")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")
        print(f"  Warnings: {warnings}")
        print(f"  Success rate: {(passed / total_checks * 100):.1f}%")

        # Save detailed report
        report_path = self.output_dir / "08_database_validation_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# NBA Database Validation Report\n\n")
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Database**: {self.db_path}\n\n")

            f.write("## Summary\n\n")
            f.write(f"- Total validation checks: {total_checks}\n")
            f.write(f"- Passed: {passed}\n")
            f.write(f"- Failed: {failed}\n")
            f.write(f"- Warnings: {warnings}\n")
            f.write(f"- Success rate: {(passed / total_checks * 100):.1f}%\n\n")

            f.write("## Detailed Results\n\n")
            f.write("| Check | Status | Severity | Details |\n")
            f.write("|-------|--------|----------|----------|\n")

            for _, row in results_df.iterrows():
                status_icon = {
                    'PASS': '[OK]',
                    'FAIL': '[ERROR]',
                    'WARNING': '[WARNING]',
                    'INFO': '[INFO]'
                }.get(row['status'], '[?]')

                f.write(f"| {row['check']} | {status_icon} {row['status']} | {row['severity']} | {row['details']} |\n")

            f.write("\n## Critical Issues\n\n")
            critical = results_df[results_df['severity'] == 'CRITICAL']
            if len(critical) > 0:
                for _, row in critical.iterrows():
                    f.write(f"- **{row['check']}**: {row['details']}\n")
            else:
                f.write("No critical issues found.\n")

            f.write("\n## Recommendations\n\n")
            if failed > 0 or warnings > 0:
                f.write("1. Address all CRITICAL and HIGH severity issues immediately\n")
                f.write("2. Review MEDIUM severity issues for data quality improvements\n")
                f.write("3. Acquire missing seasons (2023-24, 2024-25, 2025-26)\n")
                f.write("4. Re-run validation after fixes\n")
            else:
                f.write("Database passes all validation checks. Proceed with acquiring missing seasons.\n")

        print(f"\n[OK] Validation report saved to: {report_path}")

        # Save results CSV
        csv_path = self.output_dir / "data" / "validation_results.csv"
        results_df.to_csv(csv_path, index=False)
        print(f"[OK] Validation results CSV saved to: {csv_path}")

        return results_df

    def run_all_validations(self):
        """Run all validation checks."""
        print("\n" + "=" * 80)
        print("NBA DATABASE VALIDATION")
        print("=" * 80)
        print(f"Database: {self.db_path}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        self.connect()

        try:
            # Run all validation checks
            db_seasons, missing_seasons = self.validate_season_coverage()
            if db_seasons is not None:
                self.validate_team_counts(db_seasons)
                self.validate_game_counts(db_seasons)

            self.validate_player_coverage()
            self.validate_statistical_integrity()
            self.validate_referential_integrity()

            # Generate final report
            results_df = self.generate_report()

            print("\n" + "=" * 80)
            print("VALIDATION COMPLETE")
            print("=" * 80)

            return results_df

        finally:
            self.disconnect()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate NBA DuckDB database completeness and quality"
    )
    parser.add_argument(
        '--db-path',
        default='nba.duckdb',
        help='Path to DuckDB database file'
    )
    parser.add_argument(
        '--output-dir',
        default=None,
        help='Output directory for validation reports'
    )

    args = parser.parse_args()

    # Run validation
    validator = NBADatabaseValidator(args.db_path, args.output_dir)
    results = validator.run_all_validations()

    # Exit with appropriate code
    failed_count = len(results[results['status'] == 'FAIL'])
    sys.exit(0 if failed_count == 0 else 1)


if __name__ == '__main__':
    main()
