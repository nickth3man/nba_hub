from src.core.database import get_db_connection


def migrate():
    con = get_db_connection()

    print("Creating unified relational schema with prefix 'unified_'...")

    # Drop in order
    tables = [
        "unified_pbp_events",
        "unified_player_season_pbp",
        "unified_draft_picks",
        "unified_drafts",
        "unified_award_results",
        "unified_season_awards",
        "unified_awards",
        "unified_player_season_advanced",
        "unified_player_boxscores",
        "unified_games",
        "unified_team_history",
        "unified_teams",
        "unified_players",
        "unified_seasons",
        "unified_leagues",
        "unified_arenas",
        "unified_coaches",
        "unified_referees",
    ]
    for t in tables:
        con.execute(f"DROP TABLE IF EXISTS {t} CASCADE")

    # 1. Core Dimensions
    con.execute("""
    CREATE TABLE unified_leagues (
      league_id        INTEGER PRIMARY KEY,
      league_code      VARCHAR NOT NULL UNIQUE,
      league_name      VARCHAR NOT NULL
    );
    """)

    con.execute(
        "INSERT INTO unified_leagues (league_id, league_code, league_name) VALUES (1, 'NBA', 'National Basketball Association'), (2, 'BAA', 'Basketball Association of America'), (3, 'ABA', 'American Basketball Association')"
    )

    con.execute("""
    CREATE TABLE unified_seasons (
      season_id        INTEGER PRIMARY KEY,
      league_id        INTEGER NOT NULL REFERENCES unified_leagues(league_id),
      season_year      INTEGER NOT NULL,
      start_date       DATE,
      end_date         DATE,
      UNIQUE (league_id, season_year)
    );
    """)

    con.execute("""
    CREATE TABLE unified_arenas (
      arena_id         INTEGER PRIMARY KEY,
      arena_name       VARCHAR NOT NULL,
      city             VARCHAR
    );
    """)

    con.execute("""
    CREATE TABLE unified_teams (
      team_id          BIGINT PRIMARY KEY,
      league_id        INTEGER NOT NULL REFERENCES unified_leagues(league_id),
      franchise_code   VARCHAR,
      nba_api_team_id  BIGINT UNIQUE
    );
    """)

    con.execute("""
    CREATE TABLE unified_team_history (
      team_history_id  INTEGER PRIMARY KEY,
      team_id          BIGINT NOT NULL REFERENCES unified_teams(team_id),
      effective_start  DATE NOT NULL,
      effective_end    DATE,
      city             VARCHAR NOT NULL,
      nickname         VARCHAR NOT NULL,
      abbreviation     VARCHAR,
      is_active        BOOLEAN NOT NULL DEFAULT TRUE
    );
    """)

    con.execute("""
    CREATE TABLE unified_players (
      player_id          BIGINT PRIMARY KEY,
      nba_api_person_id  BIGINT UNIQUE,
      first_name         VARCHAR,
      last_name          VARCHAR,
      display_name       VARCHAR,
      birth_date         DATE,
      from_year          INTEGER,
      to_year            INTEGER
    );
    """)

    con.execute("""
    CREATE TABLE unified_coaches (
      coach_id           VARCHAR PRIMARY KEY,
      nba_api_coach_id   BIGINT UNIQUE,
      display_name       VARCHAR NOT NULL
    );
    """)

    con.execute("""
    CREATE TABLE unified_referees (
      referee_id         VARCHAR PRIMARY KEY,
      nba_api_ref_id     BIGINT UNIQUE,
      display_name       VARCHAR NOT NULL
    );
    """)

    con.execute("""
    CREATE TABLE unified_games (
      game_id            VARCHAR PRIMARY KEY,
      league_id          INTEGER NOT NULL REFERENCES unified_leagues(league_id),
      season_id          INTEGER NOT NULL REFERENCES unified_seasons(season_id),
      season_type        VARCHAR NOT NULL,
      game_date          DATE NOT NULL,
      home_team_id       BIGINT NOT NULL REFERENCES unified_teams(team_id),
      away_team_id       BIGINT NOT NULL REFERENCES unified_teams(team_id),
      home_points        INTEGER,
      away_points        INTEGER,
      attendance         INTEGER,
      arena_id           INTEGER REFERENCES unified_arenas(arena_id)
    );
    """)

    con.execute("""
    CREATE TABLE unified_player_boxscores (
      game_id            VARCHAR NOT NULL REFERENCES unified_games(game_id),
      player_id          BIGINT NOT NULL REFERENCES unified_players(player_id),
      team_id            BIGINT NOT NULL REFERENCES unified_teams(team_id),
      minutes            DOUBLE,
      points             INTEGER,
      assists            INTEGER,
      rebounds_total     INTEGER,
      steals             INTEGER,
      blocks             INTEGER,
      fgm                INTEGER,
      fga                INTEGER,
      fg3m               INTEGER,
      fg3a               INTEGER,
      ftm                INTEGER,
      fta                INTEGER,
      pf                 INTEGER,
      turnovers          INTEGER,
      plus_minus         INTEGER,
      PRIMARY KEY (game_id, player_id)
    );
    """)

    con.execute("""
    CREATE TABLE unified_drafts (
        season_year      INTEGER NOT NULL,
        pick_overall     INTEGER NOT NULL,
        round_number     INTEGER,
        pick_in_round    INTEGER,
        team_id          BIGINT REFERENCES unified_teams(team_id),
        player_id        BIGINT REFERENCES unified_players(player_id),
        college          VARCHAR,
        PRIMARY KEY (season_year, pick_overall)
    );
    """)

    print("Schema created successfully.")

    # Data Migration logic
    # 1. Seasons
    print("Migrating seasons...")
    con.execute("""
    INSERT INTO unified_seasons (season_id, league_id, season_year)
    SELECT row_number() over() as season_id, (case when league='BAA' then 2 else 1 end) as league_id, start_year
    FROM raw_dim_seasons
    """)

    # 2. Teams
    print("Migrating teams...")
    # First from dim_teams
    con.execute("""
    INSERT OR IGNORE INTO unified_teams (team_id, league_id, nba_api_team_id)
    SELECT CAST(team_id AS BIGINT), MAX(case when league='BAA' then 2 else 1 end), CAST(team_id AS BIGINT)
    FROM raw_dim_teams
    GROUP BY team_id
    """)

    # Then fill missing from games
    con.execute("""
    INSERT OR IGNORE INTO unified_teams (team_id, league_id, nba_api_team_id)
    SELECT DISTINCT CAST(hometeamId AS BIGINT), 1, CAST(hometeamId AS BIGINT) FROM raw_games WHERE hometeamId IS NOT NULL
    """)
    con.execute("""
    INSERT OR IGNORE INTO unified_teams (team_id, league_id, nba_api_team_id)
    SELECT DISTINCT CAST(awayteamId AS BIGINT), 1, CAST(awayteamId AS BIGINT) FROM raw_games WHERE awayteamId IS NOT NULL
    """)

    con.execute("""
    INSERT OR IGNORE INTO unified_team_history (team_history_id, team_id, effective_start, city, nickname, abbreviation, is_active)
    SELECT row_number() over() as team_history_id, CAST(team_id AS BIGINT), '1946-01-01'::DATE, city, nickname, abbreviation, (year_active_till >= 2025)
    FROM raw_dim_teams
    """)

    # 3. Players
    print("Migrating players...")
    con.execute("""
    INSERT INTO unified_players (player_id, first_name, last_name, display_name)
    SELECT personId, ANY_VALUE(firstName), ANY_VALUE(lastName), ANY_VALUE(firstName || ' ' || lastName)
    FROM raw_player_box_scores
    GROUP BY personId
    """)

    # 4. Games
    print("Migrating games...")
    con.execute("""
    INSERT INTO unified_games (game_id, league_id, season_id, season_type, game_date, home_team_id, away_team_id, home_points, away_points, attendance)
    SELECT
        g.gameId,
        s.league_id,
        s.season_id,
        'REG',
        g.gameDateTimeEst::DATE,
        CAST(g.hometeamId AS BIGINT),
        CAST(g.awayteamId AS BIGINT),
        g.homeScore,
        g.awayScore,
        CAST(g.attendance AS INTEGER)
    FROM raw_games g
    JOIN unified_seasons s ON (CASE WHEN MONTH(g.gameDateTimeEst::TIMESTAMP) >= 10 THEN YEAR(g.gameDateTimeEst::TIMESTAMP) ELSE YEAR(g.gameDateTimeEst::TIMESTAMP) - 1 END) = s.season_year
    """)

    # 5. Boxscores
    print("Migrating boxscores...")
    con.execute("""
    INSERT INTO unified_player_boxscores (game_id, player_id, team_id, minutes, points, assists, rebounds_total, steals, blocks, fgm, fga, fg3m, fg3a, ftm, fta, pf, turnovers, plus_minus)
    SELECT
        CAST(pb.gameId AS VARCHAR),
        pb.personId,
        CAST((case when pb.home=1 then g.hometeamId else g.awayteamId end) AS BIGINT),
        numMinutes,
        points,
        assists,
        reboundsTotal,
        steals,
        blocks,
        fieldGoalsMade,
        fieldGoalsAttempted,
        threePointersMade,
        threePointersAttempted,
        freeThrowsMade,
        freeThrowsAttempted,
        foulsPersonal,
        turnovers,
        plusMinusPoints
    FROM raw_player_box_scores pb
    JOIN raw_games g ON CAST(pb.gameId AS VARCHAR) = CAST(g.gameId AS VARCHAR)
    """)

    print("Migrating coaches...")
    con.execute("""
    INSERT INTO unified_coaches (coach_id, display_name)
    SELECT DISTINCT coach_id, coach_name
    FROM coach_season_summary
    WHERE coach_id IS NOT NULL
    ON CONFLICT (coach_id) DO UPDATE SET display_name = EXCLUDED.display_name
    """)

    # 7. Drafts
    print("Migrating drafts...")
    con.execute("""
    INSERT INTO unified_drafts (season_year, pick_overall, round_number, pick_in_round, team_id, player_id, college)
    SELECT 
        dh.season_year,
        dh.pick_overall,
        dh.round_number,
        dh.pick_in_round,
        t.team_id,
        p.player_id,
        dh.college
    FROM draft_history dh
    LEFT JOIN unified_team_history t ON dh.team_id = t.abbreviation
    LEFT JOIN unified_players p ON LOWER(dh.player_name) = LOWER(p.display_name)
    QUALIFY ROW_NUMBER() OVER (PARTITION BY dh.season_year, dh.pick_overall ORDER BY t.is_active DESC, t.effective_end DESC NULLS FIRST) = 1
    """)

    con.close()
    print("Migration to unified_ schema complete.")


if __name__ == "__main__":
    migrate()
