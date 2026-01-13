from src.core.database import get_db_connection


def audit():
    con = get_db_connection()

    print("--- Games Table Schema ---")
    cols = con.execute("DESCRIBE games").fetchall()
    for c in cols:
        print(f"{c[0]} ({c[1]})")

    print("\n--- Game Table Schema ---")
    try:
        cols = con.execute("DESCRIBE game").fetchall()
        for c in cols:
            print(f"{c[0]} ({c[1]})")
    except:
        print("Table 'game' does not exist or error describing it.")

    print("\n--- Tables with 0 rows ---")
    tables = con.execute("SHOW TABLES").fetchall()
    for t in tables:
        table_name = t[0]
        try:
            count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            if count == 0:
                print(table_name)
        except:
            pass

    con.close()


if __name__ == "__main__":
    audit()
