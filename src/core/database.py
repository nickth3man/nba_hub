import duckdb

from src.core.config import DB_PATH


def get_db_connection():
    """Returns a connection to the DuckDB database."""
    return duckdb.connect(str(DB_PATH))


def query_db(query, params=None):
    """Executes a query and returns the results."""
    with get_db_connection() as con:
        if params:
            return con.execute(query, params).fetchall()
        return con.execute(query).fetchall()


def execute_db(query, params=None):
    """Executes a query that doesn't return results."""
    with get_db_connection() as con:
        if params:
            con.execute(query, params)
        else:
            con.execute(query)
