"""
Test environment and dependencies for advanced metrics acquisition
"""

import sys
from pathlib import Path

print("Testing environment...")
print(f"Python version: {sys.version}")
print()

# Test imports
print("Testing required packages:")
packages = [
    ('duckdb', 'DuckDB database'),
    ('pandas', 'Data manipulation'),
    ('cloudscraper', 'Web scraping with Cloudflare bypass'),
    ('thefuzz', 'Fuzzy string matching'),
]

missing = []
for package, description in packages:
    try:
        __import__(package)
        print(f"  [OK] {package:15s} - {description}")
    except ImportError:
        print(f"  [MISSING] {package:15s} - {description}")
        missing.append(package)

print()

if missing:
    print(f"[ERROR] Missing packages: {', '.join(missing)}")
    print(f"\nInstall with:")
    print(f"  pip install {' '.join(missing)}")
    sys.exit(1)

# Test database connection
DB_PATH = Path(r"c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb")
print(f"Testing database connection:")
print(f"  Database: {DB_PATH}")

if not DB_PATH.exists():
    print(f"  [ERROR] Database file not found")
    sys.exit(1)

print(f"  [OK] Database file exists")

try:
    import duckdb
    conn = duckdb.connect(str(DB_PATH))

    # Test query
    tables = conn.execute("SHOW TABLES").fetchdf()
    print(f"  [OK] Connected successfully")
    print(f"  [OK] Found {len(tables)} tables")

    # Check for required tables
    required_tables = ['common_player_info', 'team']
    for table_name in required_tables:
        result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        print(f"  [OK] Table '{table_name}': {result[0]} records")

    conn.close()

except Exception as e:
    print(f"  [ERROR] Database connection failed: {e}")
    sys.exit(1)

print("\n[OK] Environment test passed!")
print("\nReady to run:")
print("  1. python create_advanced_stats_table.py")
print("  2. python acquire_advanced_metrics.py --start-year 2024 --end-year 2024 --dry-run")
