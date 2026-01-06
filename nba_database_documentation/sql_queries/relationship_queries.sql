-- NBA Database Relationship Queries
-- Generated: 2026-01-05 17:03:21

-- Test FK relationship integrity
SELECT COUNT(*) as orphan_count
FROM team_game_stats
WHERE team_id IS NOT NULL
    AND team_id NOT IN (SELECT id FROM team);

-- Join teams with their game stats
SELECT t.full_name, tgs.*
FROM team t
JOIN team_game_stats tgs ON t.id = tgs.team_id
LIMIT 100;
