import duckdb

con = duckdb.connect("data/nba.duckdb")
try:
    # Extract year from gameDateTimeEst
    # Using try_cast to be safe, although schema should be consistent
    query = """
        SELECT 
            YEAR(CAST(gameDateTimeEst AS TIMESTAMP)) as yr,
            COUNT(*) as count
        FROM games
        WHERE yr BETWEEN 1946 AND 1956
        GROUP BY yr
        ORDER BY yr
    """
    results = con.sql(query).fetchall()
    print("Games per year (1946-1956):")
    for row in results:
        print(f"{row[0]}: {row[1]}")

    # Also check total count
    total = con.sql("SELECT COUNT(*) FROM games").fetchone()[0]
    print(f"Total games: {total}")

except Exception as e:
    print(f"Error: {e}")
    # Fallback to check table schema if query fails
    try:
        print("\nTable Schema:")
        print(con.sql("DESCRIBE games").fetchall())
    except:
        print("Could not describe table 'games'.")

con.close()
