-- NBA Player Box Score Analysis Queries
-- Generated: 2026-01-05
-- Database: nba.duckdb
-- Coverage: 1996-2023 player box scores (player_game_stats_silver)

-- ==============================================================================
-- SECTION 1: PLAYER CAREER STATISTICS
-- ==============================================================================

-- Get complete game log for a specific player
SELECT
    g.game_date,
    g.season_id,
    pgs.player_name,
    t.full_name as team_name,
    pgs.min,
    pgs.pts,
    pgs.reb,
    pgs.ast,
    pgs.stl,
    pgs.blk,
    pgs.tov,
    pgs.fgm,
    pgs.fga,
    pgs.fg_pct,
    pgs.fg3m,
    pgs.fg3a,
    pgs.plus_minus
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
LEFT JOIN team t ON pgs.team_id = t.id
WHERE pgs.player_name = 'LeBron James'
ORDER BY g.game_date;

-- Career averages for a player
SELECT
    player_name,
    COUNT(*) as games_played,
    ROUND(AVG(pts), 1) as ppg,
    ROUND(AVG(reb), 1) as rpg,
    ROUND(AVG(ast), 1) as apg,
    ROUND(AVG(stl), 1) as spg,
    ROUND(AVG(blk), 1) as bpg,
    ROUND(AVG(fg_pct) * 100, 1) as fg_pct,
    ROUND(AVG(fg3_pct) * 100, 1) as fg3_pct,
    ROUND(AVG(ft_pct) * 100, 1) as ft_pct,
    SUM(pts) as career_points,
    SUM(reb) as career_rebounds,
    SUM(ast) as career_assists
FROM player_game_stats_silver
WHERE player_name = 'Kobe Bryant'
  AND pts IS NOT NULL;  -- Exclude DNP games

-- Season-by-season stats for a player
SELECT
    g.season_id,
    COUNT(*) as games,
    ROUND(AVG(pgs.pts), 1) as ppg,
    ROUND(AVG(pgs.reb), 1) as rpg,
    ROUND(AVG(pgs.ast), 1) as apg,
    ROUND(AVG(pgs.fg_pct) * 100, 1) as fg_pct,
    SUM(pgs.pts) as total_pts
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE pgs.player_name = 'Stephen Curry'
  AND pgs.pts IS NOT NULL
GROUP BY g.season_id
ORDER BY g.season_id;

-- ==============================================================================
-- SECTION 2: CAREER HIGHS & MILESTONES
-- ==============================================================================

-- All 50+ point games in database
SELECT
    g.game_date,
    pgs.player_name,
    t.full_name as team,
    pgs.pts,
    pgs.fgm,
    pgs.fga,
    pgs.fg3m,
    pgs.ftm,
    pgs.reb,
    pgs.ast,
    pgs.min
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
LEFT JOIN team t ON pgs.team_id = t.id
WHERE pgs.pts >= 50
ORDER BY pgs.pts DESC, g.game_date DESC;

-- Career high game for each player (points)
WITH career_highs AS (
    SELECT
        player_name,
        MAX(pts) as career_high_pts
    FROM player_game_stats_silver
    WHERE pts IS NOT NULL
    GROUP BY player_name
)
SELECT
    pgs.player_name,
    ch.career_high_pts,
    g.game_date,
    pgs.fgm,
    pgs.fga,
    pgs.fg3m,
    pgs.reb,
    pgs.ast
FROM career_highs ch
JOIN player_game_stats_silver pgs
    ON ch.player_name = pgs.player_name
    AND ch.career_high_pts = pgs.pts
JOIN games g ON pgs.game_id = g.game_id
WHERE ch.career_high_pts >= 40  -- Filter for notable performances
ORDER BY ch.career_high_pts DESC;

-- Triple-double games
SELECT
    g.game_date,
    g.season_id,
    pgs.player_name,
    pgs.pts,
    pgs.reb,
    pgs.ast,
    pgs.stl,
    pgs.blk
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE pgs.pts >= 10
  AND pgs.reb >= 10
  AND pgs.ast >= 10
ORDER BY g.game_date DESC;

-- ==============================================================================
-- SECTION 3: PLAYER COMPARISONS
-- ==============================================================================

-- Head-to-head comparison of two players
WITH player_stats AS (
    SELECT
        player_name,
        COUNT(*) as games,
        ROUND(AVG(pts), 1) as ppg,
        ROUND(AVG(reb), 1) as rpg,
        ROUND(AVG(ast), 1) as apg,
        ROUND(AVG(fg_pct) * 100, 1) as fg_pct,
        ROUND(AVG(fg3_pct) * 100, 1) as fg3_pct,
        SUM(pts) as career_pts
    FROM player_game_stats_silver
    WHERE player_name IN ('LeBron James', 'Kobe Bryant')
      AND pts IS NOT NULL
    GROUP BY player_name
)
SELECT * FROM player_stats
ORDER BY career_pts DESC;

-- Compare players in same season
SELECT
    pgs.player_name,
    COUNT(*) as games,
    ROUND(AVG(pgs.pts), 1) as ppg,
    ROUND(AVG(pgs.reb), 1) as rpg,
    ROUND(AVG(pgs.ast), 1) as apg,
    ROUND(AVG(pgs.stl), 1) as spg,
    ROUND(AVG(pgs.blk), 1) as bpg
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id = 22022  -- 2022-23 season
  AND pgs.pts IS NOT NULL
  AND player_name IN ('Giannis Antetokounmpo', 'Joel Embiid', 'Nikola Jokic')
GROUP BY pgs.player_name
ORDER BY AVG(pgs.pts) DESC;

-- ==============================================================================
-- SECTION 4: LEAGUE LEADERS
-- ==============================================================================

-- Top 10 scorers for a season (minimum 20 games)
SELECT
    pgs.player_name,
    COUNT(*) as games,
    SUM(pgs.pts) as total_pts,
    ROUND(AVG(pgs.pts), 1) as ppg,
    ROUND(AVG(pgs.fg_pct) * 100, 1) as fg_pct
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id = 22022  -- 2022-23 season
  AND pgs.pts IS NOT NULL
GROUP BY pgs.player_name
HAVING COUNT(*) >= 20
ORDER BY AVG(pgs.pts) DESC
LIMIT 10;

-- Triple-double leaders (all-time)
SELECT
    player_name,
    COUNT(*) as triple_doubles
FROM player_game_stats_silver
WHERE pts >= 10
  AND reb >= 10
  AND ast >= 10
GROUP BY player_name
ORDER BY COUNT(*) DESC
LIMIT 20;

-- Most 30-point games
SELECT
    player_name,
    COUNT(*) as games_30plus,
    MAX(pts) as career_high
FROM player_game_stats_silver
WHERE pts >= 30
GROUP BY player_name
ORDER BY COUNT(*) DESC
LIMIT 20;

-- ==============================================================================
-- SECTION 5: PERFORMANCE TRENDS
-- ==============================================================================

-- Player performance by month
SELECT
    EXTRACT(MONTH FROM g.game_date) as month,
    COUNT(*) as games,
    ROUND(AVG(pgs.pts), 1) as ppg,
    ROUND(AVG(pgs.reb), 1) as rpg,
    ROUND(AVG(pgs.ast), 1) as apg
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE pgs.player_name = 'Stephen Curry'
  AND g.season_id = 22022
  AND pgs.pts IS NOT NULL
GROUP BY EXTRACT(MONTH FROM g.game_date)
ORDER BY month;

-- Performance in wins vs losses (requires game outcome data)
-- Note: This assumes you can determine W/L from team_game_stats
WITH game_outcomes AS (
    SELECT
        pgs.player_id,
        pgs.game_id,
        pgs.pts,
        pgs.reb,
        pgs.ast,
        CASE
            WHEN tgs.pts > opp_tgs.pts THEN 'W'
            ELSE 'L'
        END as outcome
    FROM player_game_stats_silver pgs
    JOIN team_game_stats tgs
        ON pgs.game_id = tgs.game_id
        AND pgs.team_id = tgs.team_id
    JOIN team_game_stats opp_tgs
        ON pgs.game_id = opp_tgs.game_id
        AND pgs.team_id != opp_tgs.team_id
    WHERE pgs.player_name = 'Kevin Durant'
      AND pgs.pts IS NOT NULL
)
SELECT
    outcome,
    COUNT(*) as games,
    ROUND(AVG(pts), 1) as avg_pts,
    ROUND(AVG(reb), 1) as avg_reb,
    ROUND(AVG(ast), 1) as avg_ast
FROM game_outcomes
GROUP BY outcome;

-- ==============================================================================
-- SECTION 6: ADVANCED STATISTICS
-- ==============================================================================

-- Calculate True Shooting Percentage
-- TS% = PTS / (2 * (FGA + 0.44 * FTA))
SELECT
    pgs.player_name,
    COUNT(*) as games,
    ROUND(AVG(pgs.pts), 1) as ppg,
    ROUND(AVG(
        CASE
            WHEN (pgs.fga + 0.44 * pgs.fta) > 0
            THEN pgs.pts / (2.0 * (pgs.fga + 0.44 * pgs.fta))
            ELSE NULL
        END
    ) * 100, 1) as ts_pct,
    ROUND(AVG(pgs.fg_pct) * 100, 1) as fg_pct
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id = 22022
  AND pgs.pts IS NOT NULL
GROUP BY pgs.player_name
HAVING COUNT(*) >= 50
ORDER BY AVG(pgs.pts) DESC
LIMIT 20;

-- Effective Field Goal Percentage
-- eFG% = (FGM + 0.5 * 3PM) / FGA
SELECT
    player_name,
    COUNT(*) as games,
    ROUND(AVG(pts), 1) as ppg,
    ROUND(AVG(
        CASE
            WHEN fga > 0
            THEN (fgm + 0.5 * fg3m) / fga
            ELSE NULL
        END
    ) * 100, 1) as efg_pct,
    ROUND(AVG(fg_pct) * 100, 1) as fg_pct
FROM player_game_stats_silver
WHERE pts IS NOT NULL
  AND game_id IN (
      SELECT game_id FROM games WHERE season_id = 22022
  )
GROUP BY player_name
HAVING COUNT(*) >= 50
ORDER BY AVG(pts) DESC
LIMIT 20;

-- Usage rate approximation (shots taken as % of available)
-- Simplified: (FGA + 0.44 * FTA) per game
SELECT
    player_name,
    COUNT(*) as games,
    ROUND(AVG(pts), 1) as ppg,
    ROUND(AVG(fga + 0.44 * fta), 1) as usage_indicator,
    ROUND(AVG(fg_pct) * 100, 1) as fg_pct
FROM player_game_stats_silver
WHERE pts IS NOT NULL
  AND game_id IN (
      SELECT game_id FROM games WHERE season_id = 22022
  )
GROUP BY player_name
HAVING COUNT(*) >= 50
ORDER BY AVG(fga + 0.44 * fta) DESC
LIMIT 20;

-- ==============================================================================
-- SECTION 7: CLUTCH PERFORMANCE
-- ==============================================================================

-- Games with 40+ points, 10+ rebounds, 10+ assists (rare feat)
SELECT
    g.game_date,
    g.season_id,
    pgs.player_name,
    pgs.pts,
    pgs.reb,
    pgs.ast,
    pgs.fgm,
    pgs.fga,
    pgs.min
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE pgs.pts >= 40
  AND pgs.reb >= 10
  AND pgs.ast >= 10
ORDER BY pgs.pts DESC;

-- Most efficient 30+ point games (high scoring, high efficiency)
SELECT
    g.game_date,
    pgs.player_name,
    pgs.pts,
    pgs.fgm,
    pgs.fga,
    ROUND(pgs.fg_pct * 100, 1) as fg_pct,
    pgs.fg3m,
    pgs.reb,
    pgs.ast
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE pgs.pts >= 30
  AND pgs.fg_pct >= 0.60  -- 60% shooting
  AND pgs.fga >= 10  -- Minimum shot attempts
ORDER BY pgs.pts DESC, pgs.fg_pct DESC
LIMIT 50;

-- ==============================================================================
-- SECTION 8: CONSISTENCY ANALYSIS
-- ==============================================================================

-- Players with most consecutive 20+ point games
-- Note: This is simplified - true streak analysis requires window functions
SELECT
    player_name,
    COUNT(*) as games_20plus,
    ROUND(AVG(pts), 1) as avg_pts_in_20plus_games,
    MAX(pts) as max_pts
FROM player_game_stats_silver
WHERE pts >= 20
GROUP BY player_name
ORDER BY COUNT(*) DESC
LIMIT 20;

-- Standard deviation of scoring (consistency measure)
WITH player_scoring AS (
    SELECT
        player_name,
        pts
    FROM player_game_stats_silver
    WHERE pts IS NOT NULL
      AND game_id IN (SELECT game_id FROM games WHERE season_id = 22022)
)
SELECT
    player_name,
    COUNT(*) as games,
    ROUND(AVG(pts), 1) as avg_pts,
    ROUND(STDDEV(pts), 1) as pts_stddev,
    MIN(pts) as min_pts,
    MAX(pts) as max_pts
FROM player_scoring
GROUP BY player_name
HAVING COUNT(*) >= 50
ORDER BY AVG(pts) DESC
LIMIT 20;

-- ==============================================================================
-- SECTION 9: PLAYING TIME ANALYSIS
-- ==============================================================================

-- Average minutes per game by player
-- Note: minutes stored as VARCHAR (MM:SS), need to parse
WITH minutes_parsed AS (
    SELECT
        player_name,
        game_id,
        CAST(SPLIT_PART(min, ':', 1) AS INTEGER) +
        CAST(SPLIT_PART(min, ':', 2) AS INTEGER) / 60.0 as minutes_decimal
    FROM player_game_stats_silver
    WHERE min IS NOT NULL
      AND min != '0:00'
      AND game_id IN (SELECT game_id FROM games WHERE season_id = 22022)
)
SELECT
    player_name,
    COUNT(*) as games,
    ROUND(AVG(minutes_decimal), 1) as avg_mpg,
    MAX(minutes_decimal) as max_minutes
FROM minutes_parsed
GROUP BY player_name
HAVING COUNT(*) >= 50
ORDER BY AVG(minutes_decimal) DESC
LIMIT 20;

-- ==============================================================================
-- SECTION 10: DATA QUALITY CHECKS
-- ==============================================================================

-- Find potential data quality issues
SELECT
    'FGM > FGA' as issue_type,
    COUNT(*) as violation_count
FROM player_game_stats_silver
WHERE fgm > fga
UNION ALL
SELECT
    'Negative stats',
    COUNT(*)
FROM player_game_stats_silver
WHERE pts < 0 OR reb < 0 OR ast < 0
UNION ALL
SELECT
    '3PM > FGM',
    COUNT(*)
FROM player_game_stats_silver
WHERE fg3m > fgm
UNION ALL
SELECT
    'Missing player_id',
    COUNT(*)
FROM player_game_stats_silver
WHERE player_id IS NULL;

-- Games with unusual box score totals
SELECT
    game_id,
    COUNT(*) as player_count,
    SUM(pts) as team_total_pts
FROM player_game_stats_silver
WHERE pts IS NOT NULL
GROUP BY game_id
HAVING SUM(pts) < 50 OR SUM(pts) > 200  -- Unusual team totals
ORDER BY SUM(pts);

-- ==============================================================================
-- SECTION 11: COVERAGE ANALYSIS
-- ==============================================================================

-- Check player box score coverage by season
SELECT
    g.season_id,
    COUNT(DISTINCT g.game_id) as total_games,
    COUNT(DISTINCT pgs.game_id) as games_with_player_stats,
    ROUND(100.0 * COUNT(DISTINCT pgs.game_id) / COUNT(DISTINCT g.game_id), 1) as coverage_pct
FROM games g
LEFT JOIN player_game_stats_silver pgs ON g.game_id = pgs.game_id
WHERE g.season_id >= 21996  -- From 1996 onwards
GROUP BY g.season_id
ORDER BY g.season_id DESC;

-- Find games without player box scores
SELECT
    g.game_id,
    g.game_date,
    g.season_id
FROM games g
LEFT JOIN player_game_stats_silver pgs ON g.game_id = pgs.game_id
WHERE pgs.game_id IS NULL
  AND g.game_date >= '1996-11-01'  -- Should have data from this point
ORDER BY g.game_date DESC
LIMIT 100;

-- ==============================================================================
-- END OF PLAYER ANALYSIS QUERIES
-- ==============================================================================
