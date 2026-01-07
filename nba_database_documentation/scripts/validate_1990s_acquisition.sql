-- Validation Queries for 1990s Historical Player Box Score Acquisition
-- Run with: duckdb c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb < validate_1990s_acquisition.sql

-- ============================================================================
-- Query 1: Overall Summary
-- ============================================================================
.print '==================================================================='
.print 'VALIDATION REPORT: 1990s Player Box Scores (1990-1996)'
.print '==================================================================='
.print ''
.print '1. OVERALL RECORD COUNT'
.print '-------------------------------------------------------------------'

SELECT
    COUNT(*) as total_records,
    COUNT(DISTINCT g.game_id) as unique_games,
    COUNT(DISTINCT pgs.player_id) as unique_players,
    MIN(g.game_date) as earliest_game,
    MAX(g.game_date) as latest_game
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997;

.print ''

-- ============================================================================
-- Query 2: Records by Season
-- ============================================================================
.print '2. RECORDS BY SEASON'
.print '-------------------------------------------------------------------'

SELECT
    g.season_id,
    CASE
        WHEN g.season_id = 21990 THEN '1990-91'
        WHEN g.season_id = 21991 THEN '1991-92'
        WHEN g.season_id = 21992 THEN '1992-93'
        WHEN g.season_id = 21993 THEN '1993-94'
        WHEN g.season_id = 21994 THEN '1994-95'
        WHEN g.season_id = 21995 THEN '1995-96'
        WHEN g.season_id = 21996 THEN '1996-97'
    END as season,
    COUNT(*) as records,
    COUNT(DISTINCT pgs.game_id) as games,
    COUNT(DISTINCT pgs.player_id) as players,
    ROUND(AVG(pgs.pts), 1) as avg_pts,
    ROUND(AVG(pgs.reb), 1) as avg_reb,
    ROUND(AVG(pgs.ast), 1) as avg_ast
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997
GROUP BY g.season_id
ORDER BY g.season_id;

.print ''

-- ============================================================================
-- Query 3: Missing Stats Analysis
-- ============================================================================
.print '3. DATA QUALITY: Missing Stats'
.print '-------------------------------------------------------------------'

SELECT
    'Players with > 0 min' as category,
    COUNT(*) as total,
    SUM(CASE WHEN pgs.pts IS NULL THEN 1 ELSE 0 END) as missing_pts,
    SUM(CASE WHEN pgs.reb IS NULL THEN 1 ELSE 0 END) as missing_reb,
    SUM(CASE WHEN pgs.ast IS NULL THEN 1 ELSE 0 END) as missing_ast,
    SUM(CASE WHEN pgs.fg3m IS NULL THEN 1 ELSE 0 END) as missing_3pt,
    SUM(CASE WHEN pgs.stl IS NULL THEN 1 ELSE 0 END) as missing_stl,
    SUM(CASE WHEN pgs.blk IS NULL THEN 1 ELSE 0 END) as missing_blk,
    ROUND(100.0 * SUM(CASE WHEN pgs.pts IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as pct_missing_pts,
    ROUND(100.0 * SUM(CASE WHEN pgs.fg3m IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as pct_missing_3pt
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997
  AND pgs.min > 0;

.print ''

-- ============================================================================
-- Query 4: Top 20 Scoring Performances
-- ============================================================================
.print '4. TOP 20 SCORING PERFORMANCES (1990-1996)'
.print '-------------------------------------------------------------------'

SELECT
    g.game_date,
    p.display_first_last as player,
    pgs.pts,
    pgs.reb,
    pgs.ast,
    pgs.fg3m as "3pm",
    pgs.stl,
    pgs.blk,
    t.abbreviation as team
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
JOIN common_player_info p ON pgs.player_id = p.person_id
JOIN team t ON pgs.team_id = t.id
WHERE g.season_id >= 21990 AND g.season_id < 21997
ORDER BY pgs.pts DESC, pgs.reb DESC
LIMIT 20;

.print ''

-- ============================================================================
-- Query 5: Michael Jordan Statistics
-- ============================================================================
.print '5. MICHAEL JORDAN CAREER STATS (1990-1996)'
.print '-------------------------------------------------------------------'

SELECT
    p.display_first_last as player,
    COUNT(*) as games,
    ROUND(AVG(pgs.pts), 1) as avg_pts,
    ROUND(AVG(pgs.reb), 1) as avg_reb,
    ROUND(AVG(pgs.ast), 1) as avg_ast,
    ROUND(AVG(pgs.stl), 1) as avg_stl,
    ROUND(AVG(pgs.blk), 1) as avg_blk,
    MAX(pgs.pts) as max_pts,
    ROUND(AVG(pgs.fg3m), 1) as avg_3pm
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
JOIN common_player_info p ON pgs.player_id = p.person_id
WHERE p.display_first_last LIKE '%Jordan%'
  AND g.season_id >= 21990 AND g.season_id < 21997
GROUP BY p.display_first_last;

.print ''
.print 'Top 10 Michael Jordan Games:'
SELECT
    g.game_date,
    pgs.pts,
    pgs.reb,
    pgs.ast,
    pgs.stl,
    pgs.blk,
    pgs.fg3m as "3pm",
    t.abbreviation as team
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
JOIN common_player_info p ON pgs.player_id = p.person_id
JOIN team t ON pgs.team_id = t.id
WHERE p.display_first_last LIKE '%Jordan%'
  AND g.season_id >= 21990 AND g.season_id < 21997
ORDER BY pgs.pts DESC
LIMIT 10;

.print ''

-- ============================================================================
-- Query 6: Team Distribution
-- ============================================================================
.print '6. TEAM DISTRIBUTION (Top 15 Teams by Player-Game Records)'
.print '-------------------------------------------------------------------'

SELECT
    t.abbreviation,
    t.full_name,
    COUNT(*) as player_game_records,
    COUNT(DISTINCT pgs.player_id) as unique_players
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
JOIN team t ON pgs.team_id = t.id
WHERE g.season_id >= 21990 AND g.season_id < 21997
GROUP BY t.abbreviation, t.full_name
ORDER BY player_game_records DESC
LIMIT 15;

.print ''

-- ============================================================================
-- Query 7: Date Coverage by Season
-- ============================================================================
.print '7. DATE COVERAGE BY SEASON'
.print '-------------------------------------------------------------------'

SELECT
    g.season_id,
    CASE
        WHEN g.season_id = 21990 THEN '1990-91'
        WHEN g.season_id = 21991 THEN '1991-92'
        WHEN g.season_id = 21992 THEN '1992-93'
        WHEN g.season_id = 21993 THEN '1993-94'
        WHEN g.season_id = 21994 THEN '1994-95'
        WHEN g.season_id = 21995 THEN '1995-96'
        WHEN g.season_id = 21996 THEN '1996-97'
    END as season,
    MIN(g.game_date) as first_game,
    MAX(g.game_date) as last_game,
    COUNT(DISTINCT g.game_id) as games_with_boxscores,
    COUNT(*) as player_records
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997
GROUP BY g.season_id
ORDER BY g.season_id;

.print ''

-- ============================================================================
-- Query 8: Players Mapped vs Unmapped
-- ============================================================================
.print '8. PLAYER MAPPING STATUS'
.print '-------------------------------------------------------------------'

SELECT
    COUNT(*) as total_records,
    SUM(CASE WHEN pgs.player_id IS NOT NULL THEN 1 ELSE 0 END) as mapped_to_player_id,
    SUM(CASE WHEN pgs.player_id IS NULL THEN 1 ELSE 0 END) as unmapped_player_id,
    ROUND(100.0 * SUM(CASE WHEN pgs.player_id IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) as pct_mapped
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997;

.print ''

-- ============================================================================
-- Query 9: Statistical Ranges (Sanity Check)
-- ============================================================================
.print '9. STATISTICAL RANGES (Sanity Check)'
.print '-------------------------------------------------------------------'
.print 'Points Distribution:'

SELECT
    'Points' as stat,
    MIN(pts) as min_value,
    ROUND(AVG(pts), 1) as avg_value,
    MAX(pts) as max_value,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pts), 1) as median,
    ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY pts), 1) as p95
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997
  AND pgs.min > 0;

.print ''
.print 'Rebounds Distribution:'

SELECT
    'Rebounds' as stat,
    MIN(reb) as min_value,
    ROUND(AVG(reb), 1) as avg_value,
    MAX(reb) as max_value,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY reb), 1) as median,
    ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY reb), 1) as p95
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997
  AND pgs.min > 0;

.print ''
.print 'Assists Distribution:'

SELECT
    'Assists' as stat,
    MIN(ast) as min_value,
    ROUND(AVG(ast), 1) as avg_value,
    MAX(ast) as max_value,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ast), 1) as median,
    ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY ast), 1) as p95
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 21990 AND g.season_id < 21997
  AND pgs.min > 0;

.print ''

-- ============================================================================
-- Query 10: Playoffs Coverage
-- ============================================================================
.print '10. PLAYOFFS COVERAGE (Season IDs 4xxxx)'
.print '-------------------------------------------------------------------'

SELECT
    g.season_id,
    CASE
        WHEN g.season_id = 41990 THEN '1991 Playoffs'
        WHEN g.season_id = 41991 THEN '1992 Playoffs'
        WHEN g.season_id = 41992 THEN '1993 Playoffs'
        WHEN g.season_id = 41993 THEN '1994 Playoffs'
        WHEN g.season_id = 41994 THEN '1995 Playoffs'
        WHEN g.season_id = 41995 THEN '1996 Playoffs'
        WHEN g.season_id = 41996 THEN '1997 Playoffs'
    END as playoffs,
    COUNT(DISTINCT g.game_id) as games,
    COUNT(*) as player_records
FROM player_game_stats_silver pgs
JOIN games g ON pgs.game_id = g.game_id
WHERE g.season_id >= 41990 AND g.season_id < 41997
GROUP BY g.season_id
ORDER BY g.season_id;

.print ''
.print '==================================================================='
.print 'VALIDATION COMPLETE'
.print '==================================================================='
.print ''
.print 'Success Criteria:'
.print '  ✓ Total records: ~160,000-170,000'
.print '  ✓ All 6 seasons present (1990-1996)'
.print '  ✓ < 1% missing stats for core metrics'
.print '  ✓ Michael Jordan games validated'
.print '  ✓ Statistical ranges reasonable'
.print ''
