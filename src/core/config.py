import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
DB_PATH = DATA_DIR / "nba.duckdb"

# Scraper paths
SCRAPER_DATA_DIR = RAW_DATA_DIR / "html"

# CSV Files
GAMES_CSV = RAW_DATA_DIR / "Games.csv"
TEAM_HISTORIES_CSV = RAW_DATA_DIR / "TeamHistories.csv"
PLAYERS_CSV = RAW_DATA_DIR / "Players.csv"
PLAYER_STATISTICS_CSV = RAW_DATA_DIR / "PlayerStatistics.csv"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(SCRAPER_DATA_DIR, exist_ok=True)
