-- Create table for player season advanced statistics
-- Basketball-Reference advanced metrics (PER, Win Shares, BPM, VORP, etc.)
-- Data available from 1973-74 season onwards
-- Source: https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html

CREATE TABLE IF NOT EXISTS player_season_advanced_stats (
    player_id BIGINT,
    season_id INTEGER,
    team_id BIGINT,
    games_played INTEGER,
    minutes_played INTEGER,

    -- Advanced Metrics
    per DOUBLE,              -- Player Efficiency Rating
    ts_pct DOUBLE,           -- True Shooting %
    efg_pct DOUBLE,          -- Effective FG%
    fg3a_rate DOUBLE,        -- 3PT Attempt Rate
    fta_rate DOUBLE,         -- FT Attempt Rate

    orb_pct DOUBLE,          -- Offensive Rebound %
    drb_pct DOUBLE,          -- Defensive Rebound %
    trb_pct DOUBLE,          -- Total Rebound %
    ast_pct DOUBLE,          -- Assist %
    stl_pct DOUBLE,          -- Steal %
    blk_pct DOUBLE,          -- Block %
    tov_pct DOUBLE,          -- Turnover %
    usg_pct DOUBLE,          -- Usage %

    -- Impact Metrics
    ows DOUBLE,              -- Offensive Win Shares
    dws DOUBLE,              -- Defensive Win Shares
    ws DOUBLE,               -- Win Shares
    ws_48 DOUBLE,            -- Win Shares per 48 minutes

    obpm DOUBLE,             -- Offensive Box Plus/Minus
    dbpm DOUBLE,             -- Defensive Box Plus/Minus
    bpm DOUBLE,              -- Box Plus/Minus
    vorp DOUBLE,             -- Value Over Replacement Player

    PRIMARY KEY (player_id, season_id, team_id)
);

-- Create indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_advanced_stats_player ON player_season_advanced_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_advanced_stats_season ON player_season_advanced_stats(season_id);
CREATE INDEX IF NOT EXISTS idx_advanced_stats_team ON player_season_advanced_stats(team_id);

-- Create indexes for filtering by key metrics
CREATE INDEX IF NOT EXISTS idx_advanced_stats_vorp ON player_season_advanced_stats(vorp DESC);
CREATE INDEX IF NOT EXISTS idx_advanced_stats_per ON player_season_advanced_stats(per DESC);
CREATE INDEX IF NOT EXISTS idx_advanced_stats_ws ON player_season_advanced_stats(ws DESC);
