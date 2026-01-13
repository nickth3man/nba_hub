from src.core.database import get_db_connection


def migrate_depth():
    con = get_db_connection()

    print("Creating depth tables (Draft, PBP, Awards)...")

    # Drop in order
    tables = [
        "unified_pbp_events",
        "unified_draft_picks",
        "unified_drafts",
        "unified_award_results",
        "unified_season_awards",
        "unified_awards",
    ]
    for t in tables:
        con.execute(f"DROP TABLE IF EXISTS {t} CASCADE")

    # 1. Awards Table Definition
    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_awards (
      award_id           INTEGER PRIMARY KEY,
      award_code         VARCHAR NOT NULL UNIQUE,
      award_name         VARCHAR NOT NULL
    );
    """)

    awards_data = [
        (1, "MVP", "Most Valuable Player"),
        (2, "ROY", "Rookie of the Year"),
        (3, "DPOY", "Defensive Player of the Year"),
        (4, "SMOY", "Sixth Man of the Year"),
        (5, "MIP", "Most Improved Player"),
    ]
    con.executemany(
        "INSERT OR IGNORE INTO unified_awards (award_id, award_code, award_name) VALUES (?, ?, ?)",
        awards_data,
    )

    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_season_awards (
      season_award_id    INTEGER PRIMARY KEY,
      season_id          INTEGER NOT NULL REFERENCES unified_seasons(season_id),
      award_id           INTEGER NOT NULL REFERENCES unified_awards(award_id),
      season_type        VARCHAR NOT NULL,
      UNIQUE (season_id, award_id, season_type)
    );
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_award_results (
      season_award_id    INTEGER NOT NULL REFERENCES unified_season_awards(season_award_id),
      rank               INTEGER,
      is_winner          BOOLEAN NOT NULL DEFAULT FALSE,
      player_id          BIGINT REFERENCES unified_players(player_id),
      points_won         DOUBLE,
      points_max         DOUBLE,
      vote_share         DOUBLE,
      first_place_votes  INTEGER,
      PRIMARY KEY (season_award_id, player_id)
    );
    """)

    # 2. Draft Table Definition
    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_drafts (
      draft_id           INTEGER PRIMARY KEY,
      season_id          INTEGER NOT NULL REFERENCES unified_seasons(season_id),
      UNIQUE (season_id)
    );
    """)

    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_draft_picks (
      draft_pick_id      INTEGER PRIMARY KEY,
      draft_id           INTEGER NOT NULL REFERENCES unified_drafts(draft_id),
      round_number       INTEGER,
      pick_in_round      INTEGER NOT NULL,
      overall_pick       INTEGER,
      selecting_team_id  BIGINT REFERENCES unified_teams(team_id),
      player_id          BIGINT REFERENCES unified_players(player_id),
      player_name        VARCHAR
    );
    """)

    # 3. PBP Table Definition
    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_pbp_events (
      pbp_event_id       BIGINT PRIMARY KEY,
      game_id            VARCHAR NOT NULL REFERENCES unified_games(game_id),
      event_num          INTEGER NOT NULL,
      period             INTEGER NOT NULL,
      clock_seconds      INTEGER,
      event_type         VARCHAR NOT NULL,
      description        VARCHAR,
      home_score         INTEGER,
      away_score         INTEGER,
      possession_team_id BIGINT REFERENCES unified_teams(team_id)
    );
    """)

    print("Depth tables created.")

    # MIGRATION
    # 1. Draft
    print("Migrating draft data...")
    con.execute("""
    INSERT OR IGNORE INTO unified_drafts (draft_id, season_id)
    SELECT DISTINCT season, s.season_id
    FROM read_csv('data/raw/Draft Pick History.csv', nullstr='NA', auto_detect=true) d
    JOIN unified_seasons s ON d.season = s.season_year
    """)

    con.execute("""
    INSERT OR IGNORE INTO unified_draft_picks (draft_pick_id, draft_id, round_number, pick_in_round, overall_pick, selecting_team_id, player_name)
    SELECT
        row_number() over() as draft_pick_id,
        season,
        round,
        row_number() over(partition by season, round order by overall_pick) as pick_in_round,
        overall_pick,
        (select team_id from unified_team_history where abbreviation = d.tm limit 1) as selecting_team_id,
        player
    FROM read_csv('data/raw/Draft Pick History.csv', nullstr='NA', auto_detect=true) d
    """)

    # 2. Awards
    print("Migrating award data from CSV...")
    con.execute("""
    INSERT OR IGNORE INTO unified_season_awards (season_award_id, season_id, award_id, season_type)
    SELECT DISTINCT
        row_number() over() as season_award_id,
        s.season_id,
        a.award_id,
        'REG'
    FROM read_csv('data/raw/Player Award Shares.csv', nullstr='NA', auto_detect=true) raw
    JOIN unified_seasons s ON raw.season = s.season_year
    JOIN unified_awards a ON (
        CASE
            WHEN raw.award LIKE '%mvp%' THEN 'MVP'
            WHEN raw.award LIKE '%roy%' THEN 'ROY'
            WHEN raw.award LIKE '%dpoy%' THEN 'DPOY'
            WHEN raw.award LIKE '%smoy%' THEN 'SMOY'
            WHEN raw.award LIKE '%mip%' THEN 'MIP'
            ELSE 'OTHER'
        END
    ) = a.award_code
    """)

    con.execute("""
    INSERT OR IGNORE INTO unified_award_results (season_award_id, rank, is_winner, player_id, points_won, points_max, vote_share, first_place_votes)
    SELECT
        sa.season_award_id,
        row_number() over(partition by sa.season_award_id order by raw.share DESC) as rank,
        raw.winner,
        p.player_id,
        raw.pts_won,
        raw.pts_max,
        raw.share,
        raw.first
    FROM read_csv('data/raw/Player Award Shares.csv', nullstr='NA', auto_detect=true) raw
    JOIN unified_seasons s ON raw.season = s.season_year
    JOIN unified_awards a ON (
        CASE
            WHEN raw.award LIKE '%mvp%' THEN 'MVP'
            WHEN raw.award LIKE '%roy%' THEN 'ROY'
            WHEN raw.award LIKE '%dpoy%' THEN 'DPOY'
            WHEN raw.award LIKE '%smoy%' THEN 'SMOY'
            WHEN raw.award LIKE '%mip%' THEN 'MIP'
            ELSE 'OTHER'
        END
    ) = a.award_code
    JOIN unified_season_awards sa ON sa.season_id = s.season_id AND sa.award_id = a.award_id
    JOIN unified_players p ON LOWER(p.display_name) = LOWER(raw.player)
    """)

    # 3. PBP (Aggregated Seasonal)
    print("Migrating Seasonal PBP stats...")
    con.execute("""
    CREATE TABLE IF NOT EXISTS unified_player_season_pbp (
        season_id INTEGER REFERENCES unified_seasons(season_id),
        player_id BIGINT REFERENCES unified_players(player_id),
        team_id BIGINT REFERENCES unified_teams(team_id),
        bad_pass_tov INTEGER,
        lost_ball_tov INTEGER,
        shooting_foul_drawn INTEGER,
        and1 INTEGER,
        PRIMARY KEY (season_id, player_id, team_id)
    );
    """)

    con.execute("""
    INSERT OR IGNORE INTO unified_player_season_pbp (season_id, player_id, team_id, bad_pass_tov, lost_ball_tov, shooting_foul_drawn, and1)
    SELECT
        s.season_id,
        p.player_id,
        t.team_id,
        raw.bad_pass_turnover,
        raw.lost_ball_turnover,
        raw.shooting_foul_drawn,
        raw.and1
    FROM read_csv_auto('data/raw/Player Play By Play.csv') raw
    JOIN unified_seasons s ON raw.season = s.season_year
    JOIN unified_players p ON raw.player_id = (SELECT cast(nba_api_person_id as varchar) from unified_players where player_id = p.player_id) -- Again, ID mapping
    OR p.display_name = raw.player
    JOIN unified_team_history t ON raw.team = t.abbreviation
    """)

    con.close()
    print("Depth migration complete.")


if __name__ == "__main__":
    migrate_depth()
