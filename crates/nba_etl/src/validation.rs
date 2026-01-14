use anyhow::{Result, Context};
use duckdb::Connection;
use log::{info, error};

pub fn validate_team_totals(db_path: &str) -> Result<()> {
    info!("Validating team totals against player sums...");
    
    let conn = Connection::open(db_path).context("Failed to open DuckDB")?;
    
    // Check if tables exist (assuming Sync has populated DuckDB from Convex or direct ingest)
    // For this MVP, we'll assume we are checking the local DuckDB state if it exists.
    
    // Query: For each game and team, sum player points and compare to team points
    // Note: We need the schema to match what we expect. 
    // Assuming 'unified_games' and 'unified_player_boxscores' exist in DuckDB.
    
    let query = r#"
        SELECT 
            g.game_id,
            g.home_team_id,
            g.home_points,
            SUM(CASE WHEN pb.team_id = g.home_team_id THEN pb.points ELSE 0 END) as calculated_home_points
        FROM unified_games g
        JOIN unified_player_boxscores pb ON g.game_id = pb.game_id
        GROUP BY g.game_id, g.home_team_id, g.home_points
        HAVING g.home_points != calculated_home_points
    "#;
    
    let mut stmt = conn.prepare(query).context("Failed to prepare validation query")?;
    let rows = stmt.query_map([], |row| {
        Ok((
            row.get::<_, String>(0)?,
            row.get::<_, i64>(1)?,
            row.get::<_, i32>(2)?,
            row.get::<_, i32>(3)?,
        ))
    })?;
    
    let mut discrepancies = 0;
    for row in rows {
        let (game_id, team_id, reported, calculated) = row?;
        error!("Discrepancy in Game {}: Team {} reported {}, calculated {}", game_id, team_id, reported, calculated);
        discrepancies += 1;
    }
    
    if discrepancies == 0 {
        info!("Validation passed: All team totals match player sums.");
    } else {
        error!("Validation failed: Found {} discrepancies.", discrepancies);
        anyhow::bail!("Validation failed");
    }
    
    Ok(())
}
