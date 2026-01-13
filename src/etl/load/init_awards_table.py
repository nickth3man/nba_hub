from src.core.database import get_db_connection


def init_awards_table():
    con = get_db_connection()

    # Create sequence for ID if it doesn't exist
    try:
        con.sql("CREATE SEQUENCE awards_voting_id_seq")
    except Exception:
        pass  # Sequence might already exist

    # Create table
    # Columns: id, award_type, season, player_id, name, rank, first_place_votes, points_won, points_max, share
    con.sql("""
        CREATE TABLE IF NOT EXISTS awards_voting (
            id INTEGER PRIMARY KEY DEFAULT nextval('awards_voting_id_seq'),
            award_type VARCHAR,
            season INTEGER,
            player_id VARCHAR,
            name VARCHAR,
            rank INTEGER,
            first_place_votes INTEGER,
            points_won INTEGER,
            points_max INTEGER,
            share FLOAT,
            UNIQUE(award_type, season, player_id)
        )
    """)

    print("Initialized awards_voting table.")
    con.close()


if __name__ == "__main__":
    init_awards_table()
