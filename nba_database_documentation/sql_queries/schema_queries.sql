-- NBA Database Schema Queries
-- Generated: 2026-01-05 17:03:21

-- List all tables and views
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'main'
ORDER BY table_type, table_name;

-- Get schema for a specific table
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'team_game_stats'
ORDER BY ordinal_position;

-- Get all constraints
SELECT * FROM duckdb_constraints()
WHERE schema_name = 'main';

-- Get all indexes
SELECT * FROM duckdb_indexes()
WHERE schema_name = 'main';
