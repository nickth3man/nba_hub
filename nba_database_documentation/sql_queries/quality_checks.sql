-- NBA Database Quality Check Queries
-- Generated: 2026-01-05 17:03:21

-- Find duplicate rows
SELECT *, COUNT(*) as dup_count
FROM team
GROUP BY ALL
HAVING COUNT(*) > 1;

-- Check for negative statistics
SELECT *
FROM team_game_stats
WHERE pts < 0 OR reb < 0 OR ast < 0;

-- Check FG made vs attempted
SELECT game_id, team_id, fgm, fga
FROM team_game_stats
WHERE fgm > fga;
