"""Configuration for NBA Hub Web Application"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database configuration
DATABASE_PATH = BASE_DIR / "nba.duckdb"

# Application settings
APP_TITLE = "NBA Hub"
APP_DESCRIPTION = "Comprehensive NBA Statistics and Analysis Platform"
APP_VERSION = "1.0.0"

# Cache settings
CACHE_TTL = 3600  # 1 hour in seconds

# Pagination
DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 100

# Minimum games threshold for league leaders
MIN_GAMES_PLAYED = 20

# Static files
STATIC_DIR = Path(__file__).parent / "static"
TEMPLATES_DIR = Path(__file__).parent / "templates"
