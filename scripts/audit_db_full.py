import duckdb
import pandas as pd


def audit_db():
    con = duckdb.connect("data/nba.duckdb")

    # Get all tables
    tables_df = con.sql(
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY table_name"
    ).df()

    print(f"Total Tables: {len(tables_df)}")
    print("-" * 50)

    results = []
    for table in tables_df["table_name"]:
        try:
            count = con.sql(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            # Get columns
            cols = con.sql(f"DESCRIBE {table}").df()
            col_names = ", ".join(cols["column_name"].tolist())
            results.append(
                {
                    "Table": table,
                    "Rows": count,
                    "Columns": len(cols),
                    "Column Names": col_names,
                }
            )
        except Exception as e:
            results.append(
                {
                    "Table": table,
                    "Rows": "ERROR",
                    "Columns": "ERROR",
                    "Column Names": str(e),
                }
            )

    df = pd.DataFrame(results)
    # Print all rows
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    pd.set_option("display.max_colwidth", 100)
    print(df[["Table", "Rows", "Columns"]])

    # Also print column details for key tables if needed
    # print(df)


if __name__ == "__main__":
    audit_db()
