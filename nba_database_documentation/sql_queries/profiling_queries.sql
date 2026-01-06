-- NBA Database Profiling Queries
-- Generated: 2026-01-05 17:03:21

-- Quick profile with SUMMARIZE
SUMMARIZE team_game_stats;

-- Detailed column statistics
SELECT 
    COUNT(*) as total_rows,
    COUNT(pts) as non_null_count,
    COUNT(DISTINCT pts) as distinct_count,
    MIN(pts) as min_value,
    MAX(pts) as max_value,
    AVG(pts) as mean_value,
    MEDIAN(pts) as median_value,
    STDDEV(pts) as std_dev
FROM team_game_stats;

-- Top 20 most common values
SELECT team_id, COUNT(*) as frequency
FROM team_game_stats
GROUP BY team_id
ORDER BY frequency DESC
LIMIT 20;
