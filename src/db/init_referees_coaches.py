import duckdb


def init_db():
    con = duckdb.connect("data/nba.duckdb")

    # Referees table
    con.execute("""
        CREATE TABLE IF NOT EXISTS referees (
            referee_id VARCHAR PRIMARY KEY,
            name VARCHAR
        );
    """)

    # Game Referees table
    # Assuming game_id links to a games table, but we won't enforce FK constraint strictly
    # if the parent table doesn't exist yet, unless we know it does.
    # DuckDB supports FKs but usually requires the parent table to exist.
    # For now, I will define columns without explicit FOREIGN KEY clauses to avoid errors if games table is missing,
    # unless I can verify it exists.

    con.execute("""
        CREATE TABLE IF NOT EXISTS game_referees (
            game_id VARCHAR,
            referee_id VARCHAR,
            role VARCHAR,
            PRIMARY KEY (game_id, referee_id)
        );
    """)

    # Coaches table
    con.execute("""
        CREATE TABLE IF NOT EXISTS coaches (
            coach_id VARCHAR PRIMARY KEY,
            name VARCHAR
        );
    """)

    # Coach Game Log table
    # id (PK), game_id (FK), team_id, coach_id (FK), result
    con.execute("""
        CREATE SEQUENCE IF NOT EXISTS coach_game_log_id_seq;
        CREATE TABLE IF NOT EXISTS coach_game_log (
            id INTEGER PRIMARY KEY DEFAULT nextval('coach_game_log_id_seq'),
            game_id VARCHAR,
            team_id VARCHAR,
            coach_id VARCHAR,
            result VARCHAR
        );
    """)

    con.close()
    print("Referees and Coaches tables initialized successfully.")


if __name__ == "__main__":
    init_db()
