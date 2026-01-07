"""Database connection and query utilities for NBA Hub"""
import duckdb
from functools import lru_cache
from typing import Any, Dict, List, Optional
from pathlib import Path
from web.config import DATABASE_PATH


@lru_cache(maxsize=1)
def get_connection() -> duckdb.DuckDBPyConnection:
    """
    Get a read-only DuckDB connection with connection pooling.

    Returns:
        DuckDB connection object
    """
    conn = duckdb.connect(str(DATABASE_PATH), read_only=True)
    return conn


def execute_query(
    query: str,
    params: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Execute a SQL query and return results as a list of dictionaries.

    Args:
        query: SQL query string
        params: Optional dictionary of query parameters

    Returns:
        List of dictionaries containing query results
    """
    conn = get_connection()

    if params:
        result = conn.execute(query, params).fetchall()
    else:
        result = conn.execute(query).fetchall()

    # Get column names
    columns = [desc[0] for desc in conn.description]

    # Convert to list of dictionaries
    return [dict(zip(columns, row)) for row in result]


def execute_query_one(
    query: str,
    params: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Execute a SQL query and return a single result as a dictionary.

    Args:
        query: SQL query string
        params: Optional dictionary of query parameters

    Returns:
        Dictionary containing query result or None
    """
    results = execute_query(query, params)
    return results[0] if results else None


def execute_query_df(query: str, params: Optional[Dict[str, Any]] = None):
    """
    Execute a SQL query and return results as a pandas DataFrame.

    Args:
        query: SQL query string
        params: Optional dictionary of query parameters

    Returns:
        Pandas DataFrame containing query results
    """
    conn = get_connection()

    if params:
        return conn.execute(query, params).df()
    else:
        return conn.execute(query).df()


def get_table_info(table_name: str) -> List[Dict[str, Any]]:
    """
    Get information about a table's columns.

    Args:
        table_name: Name of the table

    Returns:
        List of dictionaries with column information
    """
    query = f"PRAGMA table_info('{table_name}')"
    return execute_query(query)


def table_exists(table_name: str) -> bool:
    """
    Check if a table exists in the database.

    Args:
        table_name: Name of the table to check

    Returns:
        True if table exists, False otherwise
    """
    query = """
    SELECT COUNT(*) as count
    FROM information_schema.tables
    WHERE table_name = ?
    """
    result = execute_query_one(query, {"1": table_name})
    return result and result['count'] > 0
