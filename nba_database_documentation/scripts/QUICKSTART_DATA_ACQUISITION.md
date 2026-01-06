# Quick Start: Acquiring Missing NBA Seasons

This guide will help you quickly acquire the missing 2023-24, 2024-25, and 2025-26 seasons to bring your database up to date.

---

## Prerequisites

### 1. Install Required Packages

```bash
pip install basketball-reference-web-scraper nba_api
```

### 2. Verify Installation

```python
# Test basketball-reference-web-scraper
from basketball_reference_web_scraper import client
print("basketball-reference-web-scraper: OK")

# Test nba_api
from nba_api.stats.endpoints import leaguegamefinder
print("nba_api: OK")

# Test duckdb
import duckdb
print("duckdb: OK")
```

---

## Quick Start: Get One Season (2023-24)

Here's a complete script to acquire the 2023-24 season:

```python
"""
Quick script to download and load 2023-24 NBA season into DuckDB
"""

import duckdb
import pandas as pd
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from datetime import datetime

# Configuration
DB_PATH = "nba.duckdb"
SEASON_YEAR = 2024  # Season ending year (2023-24 season)

print(f"[INFO] Downloading {SEASON_YEAR-1}-{SEASON_YEAR} NBA season data...")

# Step 1: Get all games for the season
print("[1/4] Downloading game schedule...")
games = client.season_schedule(season_end_year=SEASON_YEAR)

# Convert to DataFrame
games_df = pd.DataFrame([vars(game) for game in games])
print(f"  -> Downloaded {len(games_df)} games")

# Step 2: Get box scores for each game
print("[2/4] Downloading team box scores (this may take 10-15 minutes)...")
all_box_scores = []

for idx, game in enumerate(games):
    if idx % 100 == 0:
        print(f"  -> Progress: {idx}/{len(games)} games")

    try:
        # Get box scores for this game
        box_scores = client.player_box_scores(
            day=game.start_time.day,
            month=game.start_time.month,
            year=game.start_time.year
        )
        all_box_scores.extend(box_scores)
    except Exception as e:
        print(f"  -> Error downloading game on {game.start_time}: {e}")
        continue

box_scores_df = pd.DataFrame([vars(bs) for bs in all_box_scores])
print(f"  -> Downloaded {len(box_scores_df)} player box scores")

# Step 3: Transform data to match your database schema
print("[3/4] Transforming data to database format...")

# This is a simplified example - you'll need to map all fields correctly
# based on your exact schema

def determine_season_id(date, game_type):
    """
    Convert date and game type to season_id format:
    1YYYY = Preseason
    2YYYY = Regular Season
    3YYYY = All-Star
    4YYYY = Playoffs
    """
    year = date.year if date.month >= 10 else date.year - 1

    if game_type == "PRESEASON":
        return int(f"1{year}")
    elif game_type == "REGULAR_SEASON":
        return int(f"2{year}")
    elif game_type == "ALL_STAR":
        return int(f"3{year}")
    elif game_type == "PLAYOFFS":
        return int(f"4{year}")
    else:
        return int(f"2{year}")  # default to regular season

# Example transformation for games table
games_transformed = games_df.copy()
games_transformed['season_id'] = games_transformed.apply(
    lambda row: determine_season_id(row['start_time'], row['type']),
    axis=1
)

# Step 4: Load into DuckDB
print("[4/4] Loading data into DuckDB...")
conn = duckdb.connect(DB_PATH)

# Note: This is a simplified example
# You'll need to match your exact table schema
# Consider using UPSERT or INSERT OR IGNORE to avoid duplicates

conn.execute("""
    CREATE TABLE IF NOT EXISTS games_import AS
    SELECT * FROM games_transformed
""")

conn.close()

print("[OK] Season data downloaded and loaded successfully!")
print(f"[INFO] Next steps:")
print(f"  1. Review the imported data")
print(f"  2. Transform to match your exact schema")
print(f"  3. Merge into main tables")
print(f"  4. Run validation checks")
```

---

## Recommended Approach: Step by Step

Since the data transformation is complex, here's the recommended workflow:

### Phase 1: Explore Basketball-Reference Data Format

**Goal**: Understand what data you can get and in what format

```python
from basketball_reference_web_scraper import client
from datetime import datetime

# Get one day's games to see the data structure
games_sample = client.player_box_scores(
    day=15,
    month=6,
    year=2024  # NBA Finals Game 5
)

# Print first game to see structure
print(games_sample[0])

# Expected output shows fields like:
# - name (player name)
# - team
# - location (HOME/AWAY)
# - opponent
# - outcome (WIN/LOSS)
# - seconds_played
# - made_field_goals
# - attempted_field_goals
# - made_three_point_field_goals
# - attempted_three_point_field_goals
# - made_free_throws
# - attempted_free_throws
# - offensive_rebounds
# - defensive_rebounds
# - assists
# - steals
# - blocks
# - turnovers
# - personal_fouls
# - points
```

### Phase 2: Map Basketball-Reference Fields to Your Schema

Create a mapping between Basketball-Reference data and your database:

```python
# Basketball-Reference -> Your Database Column Mapping
FIELD_MAPPING = {
    # Player/Team info
    'name': 'player_name',
    'team': 'team_abbreviation',

    # Game stats
    'made_field_goals': 'fgm',
    'attempted_field_goals': 'fga',
    'made_three_point_field_goals': 'fg3m',
    'attempted_three_point_field_goals': 'fg3a',
    'made_free_throws': 'ftm',
    'attempted_free_throws': 'fta',
    'offensive_rebounds': 'oreb',
    'defensive_rebounds': 'dreb',
    'assists': 'ast',
    'steals': 'stl',
    'blocks': 'blk',
    'turnovers': 'tov',
    'personal_fouls': 'pf',
    'points': 'pts',

    # Calculated fields
    # total_rebounds = offensive_rebounds + defensive_rebounds
}
```

### Phase 3: Create Transformation Function

```python
import pandas as pd

def transform_box_scores_to_team_game_stats(box_scores, game_info):
    """
    Transform Basketball-Reference box scores to your team_game_stats format.

    Args:
        box_scores: List of player box scores from Basketball-Reference
        game_info: Dictionary with game metadata (game_id, date, etc.)

    Returns:
        DataFrame with team-level aggregated stats in your schema format
    """
    df = pd.DataFrame([vars(bs) for bs in box_scores])

    # Aggregate player stats to team level
    team_stats = df.groupby(['team', 'location']).agg({
        'made_field_goals': 'sum',
        'attempted_field_goals': 'sum',
        'made_three_point_field_goals': 'sum',
        'attempted_three_point_field_goals': 'sum',
        'made_free_throws': 'sum',
        'attempted_free_throws': 'sum',
        'offensive_rebounds': 'sum',
        'defensive_rebounds': 'sum',
        'assists': 'sum',
        'steals': 'sum',
        'blocks': 'sum',
        'turnovers': 'sum',
        'personal_fouls': 'sum',
        'points': 'sum'
    }).reset_index()

    # Rename columns to match your schema
    team_stats = team_stats.rename(columns={
        'made_field_goals': 'fgm',
        'attempted_field_goals': 'fga',
        'made_three_point_field_goals': 'fg3m',
        'attempted_three_point_field_goals': 'fg3a',
        'made_free_throws': 'ftm',
        'attempted_free_throws': 'fta',
        'offensive_rebounds': 'oreb',
        'defensive_rebounds': 'dreb',
        'assists': 'ast',
        'steals': 'stl',
        'blocks': 'blk',
        'turnovers': 'tov',
        'personal_fouls': 'pf',
        'points': 'pts'
    })

    # Calculate total rebounds
    team_stats['reb'] = team_stats['oreb'] + team_stats['dreb']

    # Calculate percentages (stored as integers 0-100 in your DB)
    team_stats['fg_pct'] = (
        (team_stats['fgm'] / team_stats['fga'] * 100)
        .fillna(0)
        .astype(int)
    )
    team_stats['fg3_pct'] = (
        (team_stats['fg3m'] / team_stats['fg3a'] * 100)
        .fillna(0)
        .astype(int)
    )
    team_stats['ft_pct'] = (
        (team_stats['ftm'] / team_stats['fta'] * 100)
        .fillna(0)
        .astype(int)
    )

    # Add game metadata
    team_stats['game_id'] = game_info['game_id']
    team_stats['game_date'] = game_info['game_date']
    team_stats['season_id'] = game_info['season_id']

    # Map team abbreviations to team_ids (you'll need a lookup table)
    # team_stats['team_id'] = team_stats['team'].map(TEAM_ABBR_TO_ID)

    # Determine is_home
    team_stats['is_home'] = team_stats['location'] == 'HOME'

    return team_stats
```

### Phase 4: Create Complete Acquisition Script

See `nba_database_documentation/scripts/acquire_missing_seasons.py` (create this file):

```python
"""
Complete script to acquire missing NBA seasons and load into DuckDB.

Usage:
    python acquire_missing_seasons.py --season 2024 --db-path nba.duckdb

Options:
    --season: Season ending year (e.g., 2024 for 2023-24 season)
    --db-path: Path to DuckDB database
    --dry-run: Download but don't insert into database
"""

# See full implementation below
```

---

## Alternative: Use nba_api for Recent Seasons

For 2024-25 and 2025-26 seasons, `nba_api` may be faster and more reliable:

```python
from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2
import pandas as pd
import time

# Get all games for 2024-25 season
print("Fetching 2024-25 season games...")
gamefinder = leaguegamefinder.LeagueGameFinder(
    season_nullable='2024-25',
    league_id_nullable='00',
    season_type_nullable='Regular Season'  # or 'Playoffs'
)
games_df = gamefinder.get_data_frames()[0]
print(f"Found {len(games_df)} team-game records")

# Note: This returns team-game level data, not individual games
# Each game appears twice (once for each team)

# Get unique games
unique_games = games_df.drop_duplicates(subset=['GAME_ID'])
print(f"Unique games: {len(unique_games)}")

# For each game, get detailed box score if needed
for game_id in unique_games['GAME_ID'].head(5):  # Test with first 5
    print(f"Getting box score for game {game_id}...")

    box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
    team_stats = box_score.team_stats.get_data_frame()
    player_stats = box_score.player_stats.get_data_frame()

    print(f"  Teams: {len(team_stats)}, Players: {len(player_stats)}")

    # Rate limiting: NBA API blocks aggressive scraping
    time.sleep(0.6)  # Max ~100 requests per minute
```

---

## Validation Checklist

After importing each season, run these checks:

```python
import duckdb

conn = duckdb.connect("nba.duckdb")

# Check 1: Count games for the season
result = conn.execute("""
    SELECT season_id, COUNT(*) as game_count
    FROM games
    WHERE season_id IN (22023, 42023)  -- Regular + Playoffs for 2023-24
    GROUP BY season_id
""").fetchdf()
print("Game counts by season_id:")
print(result)
# Expected: 22023 ~= 1,230 games, 42023 ~= 80 games

# Check 2: Verify no FGM > FGA violations
violations = conn.execute("""
    SELECT COUNT(*) as violations
    FROM team_game_stats
    WHERE season_id IN (22023, 42023)
      AND fgm > fga
""").fetchone()[0]
print(f"FGM > FGA violations: {violations}")
# Expected: 0

# Check 3: All games have 2 teams
team_counts = conn.execute("""
    SELECT game_id, COUNT(DISTINCT team_id) as team_count
    FROM team_game_stats
    WHERE season_id IN (22023, 42023)
    GROUP BY game_id
    HAVING COUNT(DISTINCT team_id) != 2
""").fetchdf()
print(f"Games without exactly 2 teams: {len(team_counts)}")
# Expected: 0

# Check 4: Verify Finals result (2023-24)
finals_games = conn.execute("""
    SELECT
        g.game_id,
        g.game_date,
        t1.team_id as team1_id,
        t1.pts as team1_pts,
        t2.team_id as team2_id,
        t2.pts as team2_pts
    FROM games g
    JOIN team_game_stats t1 ON g.game_id = t1.game_id AND t1.is_home = true
    JOIN team_game_stats t2 ON g.game_id = t2.game_id AND t2.is_home = false
    WHERE g.season_id = 42023
      AND g.game_date >= '2024-06-06'  -- Finals started ~June 6
    ORDER BY g.game_date
""").fetchdf()
print("\n2024 Finals games:")
print(finals_games)
# Expected: 5 games, Celtics win 4-1 vs Mavericks

conn.close()
```

---

## Common Issues & Solutions

### Issue 1: Rate Limiting

**Problem**: Basketball-Reference or NBA API blocks your IP for too many requests

**Solution**:
```python
import time

# Add delays between requests
for game in games:
    # ... download game data ...
    time.sleep(1.0)  # Wait 1 second between games
```

### Issue 2: Team Abbreviation Mismatches

**Problem**: Basketball-Reference uses different team abbreviations than your database

**Solution**: Create a mapping table
```python
TEAM_ABBR_MAPPING = {
    'BRK': 'BKN',  # Brooklyn Nets
    'PHO': 'PHX',  # Phoenix Suns
    # Add all mappings
}

df['team'] = df['team'].map(TEAM_ABBR_MAPPING).fillna(df['team'])
```

### Issue 3: Duplicate Game IDs

**Problem**: Trying to insert games that already exist

**Solution**: Use INSERT OR IGNORE
```python
conn.execute("""
    INSERT OR IGNORE INTO games (game_id, season_id, game_date, ...)
    SELECT game_id, season_id, game_date, ...
    FROM games_import
""")
```

### Issue 4: Missing Team IDs

**Problem**: Can't find team_id for a team abbreviation

**Solution**: Check your team table
```python
teams = conn.execute("SELECT id, abbreviation, full_name FROM team").fetchdf()
print(teams)

# Add missing teams if needed
conn.execute("""
    INSERT INTO team (id, abbreviation, full_name, ...)
    VALUES (?, ?, ?, ...)
""", [team_id, abbr, name, ...])
```

---

## Next Steps

1. **Start small**: Test with 1 week of games from 2023-24
2. **Verify transformation**: Check the imported data matches your schema
3. **Scale up**: Once working, import full seasons
4. **Automate**: Create scripts for ongoing 2025-26 updates

---

## Additional Resources

- **basketball-reference-web-scraper docs**: https://github.com/jaebradley/basketball_reference_web_scraper
- **nba_api docs**: https://github.com/swar/nba_api
- **DuckDB Python API**: https://duckdb.org/docs/api/python/overview
- **Validation plan**: See `07_validation_and_gap_analysis_plan.md`
- **Recommendations**: See `09_validation_findings_and_recommendations.md`

---

**Good luck! You're on your way to a complete 1946-2026 NBA database.**
