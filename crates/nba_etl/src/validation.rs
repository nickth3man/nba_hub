use std::path::{Path, PathBuf};

use anyhow::{Context, Result};
use duckdb::Connection;
use log::{info, warn};

const EPSILON: f64 = 0.0001;

pub fn run_validations(db_path: &str, csv_dir: &str) -> Result<()> {
    let conn = Connection::open(db_path)
        .with_context(|| format!("Failed to open DuckDB at {db_path}"))?;
    let csv_dir = PathBuf::from(csv_dir);

    ensure_csv_table(&conn, "player_statistics", &csv_dir.join("PlayerStatistics.csv"))?;
    ensure_csv_table(&conn, "team_statistics", &csv_dir.join("TeamStatistics.csv"))?;
    ensure_csv_table(&conn, "games", &csv_dir.join("Games.csv"))?;
    ensure_csv_table(&conn, "player_per_game", &csv_dir.join("Player Per Game.csv"))?;
    ensure_csv_table(&conn, "player_totals", &csv_dir.join("Player Totals.csv"))?;
    ensure_csv_table(&conn, "per_36_minutes", &csv_dir.join("Per 36 Minutes.csv"))?;
    ensure_csv_table(&conn, "per_100_poss", &csv_dir.join("Per 100 Poss.csv"))?;
    ensure_csv_table(&conn, "advanced_csv", &csv_dir.join("Advanced.csv"))?;
    ensure_table_from_csv_if_missing(
        &conn,
        "player_season_advanced",
        &csv_dir.join("Advanced.csv"),
    )?;

    let v001 = r#"
        WITH player_points AS (
            SELECT gameId,
                   playerteamCity AS team_city,
                   playerteamName AS team_name,
                   SUM(points) AS player_points
            FROM player_statistics
            GROUP BY gameId, team_city, team_name
        ),
        team_points AS (
            SELECT gameId,
                   teamCity AS team_city,
                   teamName AS team_name,
                   teamScore
            FROM team_statistics
        )
        SELECT COUNT(*)
        FROM (
            SELECT p.gameId, p.team_city, p.team_name, p.player_points, t.teamScore
            FROM player_points p
            JOIN team_points t USING (gameId, team_city, team_name)
            WHERE COALESCE(p.player_points, 0) <> COALESCE(t.teamScore, 0)
        ) mismatches;
    "#;

    let v002 = r#"
        WITH game_seasons AS (
            SELECT gameId,
                   CASE
                       WHEN CAST(substr(gameDateTimeEst, 6, 2) AS INTEGER) >= 7
                           THEN CAST(substr(gameDateTimeEst, 1, 4) AS INTEGER) + 1
                       ELSE CAST(substr(gameDateTimeEst, 1, 4) AS INTEGER)
                   END AS season_year
            FROM games
        ),
        player_totals AS (
            SELECT ps.personId AS player_id,
                   gs.season_year,
                   COUNT(*) AS games,
                   SUM(ps.numMinutes) AS minutes_total,
                   SUM(ps.fieldGoalsMade) AS fgm,
                   SUM(ps.fieldGoalsAttempted) AS fga,
                   SUM(ps.threePointersMade) AS fg3m,
                   SUM(ps.threePointersAttempted) AS fg3a,
                   SUM(ps.freeThrowsMade) AS ftm,
                   SUM(ps.freeThrowsAttempted) AS fta,
                   SUM(ps.reboundsOffensive) AS orb,
                   SUM(ps.reboundsDefensive) AS drb,
                   SUM(ps.reboundsTotal) AS trb,
                   SUM(ps.assists) AS ast,
                   SUM(ps.steals) AS stl,
                   SUM(ps.blocks) AS blk,
                   SUM(ps.turnovers) AS tov,
                   SUM(ps.foulsPersonal) AS pf,
                   SUM(ps.points) AS pts
            FROM player_statistics ps
            JOIN game_seasons gs ON ps.gameId = gs.gameId
            GROUP BY player_id, season_year
        ),
        player_stats_calc AS (
            SELECT player_id,
                   season_year,
                   minutes_total / NULLIF(games, 0) AS minutes_pg,
                   fgm / NULLIF(games, 0) AS fgm_pg,
                   fga / NULLIF(games, 0) AS fga_pg,
                   fg3m / NULLIF(games, 0) AS fg3m_pg,
                   fg3a / NULLIF(games, 0) AS fg3a_pg,
                   ftm / NULLIF(games, 0) AS ftm_pg,
                   fta / NULLIF(games, 0) AS fta_pg,
                   orb / NULLIF(games, 0) AS orb_pg,
                   drb / NULLIF(games, 0) AS drb_pg,
                   trb / NULLIF(games, 0) AS trb_pg,
                   ast / NULLIF(games, 0) AS ast_pg,
                   stl / NULLIF(games, 0) AS stl_pg,
                   blk / NULLIF(games, 0) AS blk_pg,
                   tov / NULLIF(games, 0) AS tov_pg,
                   pf / NULLIF(games, 0) AS pf_pg,
                   pts / NULLIF(games, 0) AS pts_pg
            FROM player_totals
        ),
        player_per_game_agg AS (
            SELECT player_id,
                   season,
                   SUM(g) AS games,
                   SUM(mp_per_game * g) AS minutes_total,
                   SUM(fg_per_game * g) AS fgm,
                   SUM(fga_per_game * g) AS fga,
                   SUM(x3p_per_game * g) AS fg3m,
                   SUM(x3pa_per_game * g) AS fg3a,
                   SUM(ft_per_game * g) AS ftm,
                   SUM(fta_per_game * g) AS fta,
                   SUM(orb_per_game * g) AS orb,
                   SUM(drb_per_game * g) AS drb,
                   SUM(trb_per_game * g) AS trb,
                   SUM(ast_per_game * g) AS ast,
                   SUM(stl_per_game * g) AS stl,
                   SUM(blk_per_game * g) AS blk,
                   SUM(tov_per_game * g) AS tov,
                   SUM(pf_per_game * g) AS pf,
                   SUM(pts_per_game * g) AS pts
            FROM player_per_game
            GROUP BY player_id, season
        ),
        player_per_game_calc AS (
            SELECT player_id,
                   season,
                   minutes_total / NULLIF(games, 0) AS minutes_pg,
                   fgm / NULLIF(games, 0) AS fgm_pg,
                   fga / NULLIF(games, 0) AS fga_pg,
                   fg3m / NULLIF(games, 0) AS fg3m_pg,
                   fg3a / NULLIF(games, 0) AS fg3a_pg,
                   ftm / NULLIF(games, 0) AS ftm_pg,
                   fta / NULLIF(games, 0) AS fta_pg,
                   orb / NULLIF(games, 0) AS orb_pg,
                   drb / NULLIF(games, 0) AS drb_pg,
                   trb / NULLIF(games, 0) AS trb_pg,
                   ast / NULLIF(games, 0) AS ast_pg,
                   stl / NULLIF(games, 0) AS stl_pg,
                   blk / NULLIF(games, 0) AS blk_pg,
                   tov / NULLIF(games, 0) AS tov_pg,
                   pf / NULLIF(games, 0) AS pf_pg,
                   pts / NULLIF(games, 0) AS pts_pg
            FROM player_per_game_agg
        )
        SELECT COUNT(*)
        FROM (
            SELECT COALESCE(ps.player_id, pg.player_id) AS player_id,
                   COALESCE(ps.season_year, pg.season) AS season_year,
                   ps.minutes_pg AS stats_minutes_pg,
                   pg.minutes_pg AS ppg_minutes_pg,
                   ps.fgm_pg AS stats_fgm_pg,
                   pg.fgm_pg AS ppg_fgm_pg,
                   ps.fga_pg AS stats_fga_pg,
                   pg.fga_pg AS ppg_fga_pg,
                   ps.fg3m_pg AS stats_fg3m_pg,
                   pg.fg3m_pg AS ppg_fg3m_pg,
                   ps.fg3a_pg AS stats_fg3a_pg,
                   pg.fg3a_pg AS ppg_fg3a_pg,
                   ps.ftm_pg AS stats_ftm_pg,
                   pg.ftm_pg AS ppg_ftm_pg,
                   ps.fta_pg AS stats_fta_pg,
                   pg.fta_pg AS ppg_fta_pg,
                   ps.orb_pg AS stats_orb_pg,
                   pg.orb_pg AS ppg_orb_pg,
                   ps.drb_pg AS stats_drb_pg,
                   pg.drb_pg AS ppg_drb_pg,
                   ps.trb_pg AS stats_trb_pg,
                   pg.trb_pg AS ppg_trb_pg,
                   ps.ast_pg AS stats_ast_pg,
                   pg.ast_pg AS ppg_ast_pg,
                   ps.stl_pg AS stats_stl_pg,
                   pg.stl_pg AS ppg_stl_pg,
                   ps.blk_pg AS stats_blk_pg,
                   pg.blk_pg AS ppg_blk_pg,
                   ps.tov_pg AS stats_tov_pg,
                   pg.tov_pg AS ppg_tov_pg,
                   ps.pf_pg AS stats_pf_pg,
                   pg.pf_pg AS ppg_pf_pg,
                   ps.pts_pg AS stats_pts_pg,
                   pg.pts_pg AS ppg_pts_pg
            FROM player_stats_calc ps
            FULL OUTER JOIN player_per_game_calc pg
                ON ps.player_id = pg.player_id
               AND ps.season_year = pg.season
            WHERE ps.player_id IS NULL
               OR pg.player_id IS NULL
               OR ABS(COALESCE(ps.minutes_pg, 0) - COALESCE(pg.minutes_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.fgm_pg, 0) - COALESCE(pg.fgm_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.fga_pg, 0) - COALESCE(pg.fga_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.fg3m_pg, 0) - COALESCE(pg.fg3m_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.fg3a_pg, 0) - COALESCE(pg.fg3a_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.ftm_pg, 0) - COALESCE(pg.ftm_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.fta_pg, 0) - COALESCE(pg.fta_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.orb_pg, 0) - COALESCE(pg.orb_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.drb_pg, 0) - COALESCE(pg.drb_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.trb_pg, 0) - COALESCE(pg.trb_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.ast_pg, 0) - COALESCE(pg.ast_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.stl_pg, 0) - COALESCE(pg.stl_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.blk_pg, 0) - COALESCE(pg.blk_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.tov_pg, 0) - COALESCE(pg.tov_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.pf_pg, 0) - COALESCE(pg.pf_pg, 0)) > {eps}
               OR ABS(COALESCE(ps.pts_pg, 0) - COALESCE(pg.pts_pg, 0)) > {eps}
        ) mismatches;
    "#;

    let v003 = r#"
        WITH totals AS (
            SELECT player_id,
                   season,
                   SUM(mp) AS minutes,
                   SUM(fg) AS fgm,
                   SUM(fga) AS fga,
                   SUM(x3p) AS fg3m,
                   SUM(x3pa) AS fg3a,
                   SUM(ft) AS ftm,
                   SUM(fta) AS fta,
                   SUM(orb) AS orb,
                   SUM(drb) AS drb,
                   SUM(trb) AS trb,
                   SUM(ast) AS ast,
                   SUM(stl) AS stl,
                   SUM(blk) AS blk,
                   SUM(tov) AS tov,
                   SUM(pf) AS pf,
                   SUM(pts) AS pts
            FROM player_totals
            GROUP BY player_id, season
        ),
        totals_calc AS (
            SELECT player_id,
                   season,
                   fgm * 36 / NULLIF(minutes, 0) AS fgm_36,
                   fga * 36 / NULLIF(minutes, 0) AS fga_36,
                   fg3m * 36 / NULLIF(minutes, 0) AS fg3m_36,
                   fg3a * 36 / NULLIF(minutes, 0) AS fg3a_36,
                   ftm * 36 / NULLIF(minutes, 0) AS ftm_36,
                   fta * 36 / NULLIF(minutes, 0) AS fta_36,
                   orb * 36 / NULLIF(minutes, 0) AS orb_36,
                   drb * 36 / NULLIF(minutes, 0) AS drb_36,
                   trb * 36 / NULLIF(minutes, 0) AS trb_36,
                   ast * 36 / NULLIF(minutes, 0) AS ast_36,
                   stl * 36 / NULLIF(minutes, 0) AS stl_36,
                   blk * 36 / NULLIF(minutes, 0) AS blk_36,
                   tov * 36 / NULLIF(minutes, 0) AS tov_36,
                   pf * 36 / NULLIF(minutes, 0) AS pf_36,
                   pts * 36 / NULLIF(minutes, 0) AS pts_36
            FROM totals
        ),
        per36_agg AS (
            SELECT player_id,
                   season,
                   SUM(mp) AS minutes,
                   SUM(fg_per_36_min * mp) AS fgm,
                   SUM(fga_per_36_min * mp) AS fga,
                   SUM(x3p_per_36_min * mp) AS fg3m,
                   SUM(x3pa_per_36_min * mp) AS fg3a,
                   SUM(ft_per_36_min * mp) AS ftm,
                   SUM(fta_per_36_min * mp) AS fta,
                   SUM(orb_per_36_min * mp) AS orb,
                   SUM(drb_per_36_min * mp) AS drb,
                   SUM(trb_per_36_min * mp) AS trb,
                   SUM(ast_per_36_min * mp) AS ast,
                   SUM(stl_per_36_min * mp) AS stl,
                   SUM(blk_per_36_min * mp) AS blk,
                   SUM(tov_per_36_min * mp) AS tov,
                   SUM(pf_per_36_min * mp) AS pf,
                   SUM(pts_per_36_min * mp) AS pts
            FROM per_36_minutes
            GROUP BY player_id, season
        ),
        per36_calc AS (
            SELECT player_id,
                   season,
                   fgm * 36 / NULLIF(minutes, 0) AS fgm_36,
                   fga * 36 / NULLIF(minutes, 0) AS fga_36,
                   fg3m * 36 / NULLIF(minutes, 0) AS fg3m_36,
                   fg3a * 36 / NULLIF(minutes, 0) AS fg3a_36,
                   ftm * 36 / NULLIF(minutes, 0) AS ftm_36,
                   fta * 36 / NULLIF(minutes, 0) AS fta_36,
                   orb * 36 / NULLIF(minutes, 0) AS orb_36,
                   drb * 36 / NULLIF(minutes, 0) AS drb_36,
                   trb * 36 / NULLIF(minutes, 0) AS trb_36,
                   ast * 36 / NULLIF(minutes, 0) AS ast_36,
                   stl * 36 / NULLIF(minutes, 0) AS stl_36,
                   blk * 36 / NULLIF(minutes, 0) AS blk_36,
                   tov * 36 / NULLIF(minutes, 0) AS tov_36,
                   pf * 36 / NULLIF(minutes, 0) AS pf_36,
                   pts * 36 / NULLIF(minutes, 0) AS pts_36
            FROM per36_agg
        )
        SELECT COUNT(*)
        FROM (
            SELECT COALESCE(t.player_id, p.player_id) AS player_id,
                   COALESCE(t.season, p.season) AS season
            FROM totals_calc t
            FULL OUTER JOIN per36_calc p
                ON t.player_id = p.player_id
               AND t.season = p.season
            WHERE t.player_id IS NULL
               OR p.player_id IS NULL
               OR ABS(COALESCE(t.fgm_36, 0) - COALESCE(p.fgm_36, 0)) > {eps}
               OR ABS(COALESCE(t.fga_36, 0) - COALESCE(p.fga_36, 0)) > {eps}
               OR ABS(COALESCE(t.fg3m_36, 0) - COALESCE(p.fg3m_36, 0)) > {eps}
               OR ABS(COALESCE(t.fg3a_36, 0) - COALESCE(p.fg3a_36, 0)) > {eps}
               OR ABS(COALESCE(t.ftm_36, 0) - COALESCE(p.ftm_36, 0)) > {eps}
               OR ABS(COALESCE(t.fta_36, 0) - COALESCE(p.fta_36, 0)) > {eps}
               OR ABS(COALESCE(t.orb_36, 0) - COALESCE(p.orb_36, 0)) > {eps}
               OR ABS(COALESCE(t.drb_36, 0) - COALESCE(p.drb_36, 0)) > {eps}
               OR ABS(COALESCE(t.trb_36, 0) - COALESCE(p.trb_36, 0)) > {eps}
               OR ABS(COALESCE(t.ast_36, 0) - COALESCE(p.ast_36, 0)) > {eps}
               OR ABS(COALESCE(t.stl_36, 0) - COALESCE(p.stl_36, 0)) > {eps}
               OR ABS(COALESCE(t.blk_36, 0) - COALESCE(p.blk_36, 0)) > {eps}
               OR ABS(COALESCE(t.tov_36, 0) - COALESCE(p.tov_36, 0)) > {eps}
               OR ABS(COALESCE(t.pf_36, 0) - COALESCE(p.pf_36, 0)) > {eps}
               OR ABS(COALESCE(t.pts_36, 0) - COALESCE(p.pts_36, 0)) > {eps}
        ) mismatches;
    "#;

    let v004 = r#"
        WITH team_base AS (
            SELECT gameId,
                   teamId,
                   opponentTeamId,
                   numMinutes AS team_minutes,
                   fieldGoalsAttempted AS fga,
                   fieldGoalsMade AS fgm,
                   freeThrowsAttempted AS fta,
                   reboundsOffensive AS orb,
                   reboundsDefensive AS drb,
                   turnovers AS tov
            FROM team_statistics
        ),
        team_poss AS (
            SELECT t.gameId,
                   t.teamId,
                   t.opponentTeamId,
                   t.team_minutes,
                   t.fga,
                   t.fgm,
                   t.fta,
                   t.orb,
                   t.drb,
                   t.tov,
                   opp.drb AS opp_drb,
                   (t.fga + 0.4 * t.fta - 1.07 * (t.orb / NULLIF(t.orb + opp.drb, 0)) * (t.fga - t.fgm) + t.tov) AS team_poss,
                   (opp.fga + 0.4 * opp.fta - 1.07 * (opp.orb / NULLIF(opp.orb + t.drb, 0)) * (opp.fga - opp.fgm) + opp.tov) AS opp_poss
            FROM team_base t
            JOIN team_base opp
              ON t.gameId = opp.gameId
             AND t.opponentTeamId = opp.teamId
        ),
        game_poss AS (
            SELECT *,
                   0.5 * (team_poss + opp_poss) AS game_poss
            FROM team_poss
        ),
        player_games AS (
            SELECT ps.personId AS player_id,
                   CASE
                       WHEN CAST(substr(ps.gameDateTimeEst, 6, 2) AS INTEGER) >= 7
                           THEN CAST(substr(ps.gameDateTimeEst, 1, 4) AS INTEGER) + 1
                       ELSE CAST(substr(ps.gameDateTimeEst, 1, 4) AS INTEGER)
                   END AS season_year,
                   ps.numMinutes AS player_minutes,
                   ps.points AS points,
                   ps.assists AS assists,
                   ps.reboundsTotal AS trb,
                   ps.steals AS stl,
                   ps.blocks AS blk,
                   ps.turnovers AS tov,
                   ps.foulsPersonal AS pf,
                   ps.fieldGoalsMade AS fgm,
                   ps.fieldGoalsAttempted AS fga,
                   ps.threePointersMade AS fg3m,
                   ps.threePointersAttempted AS fg3a,
                   ps.freeThrowsMade AS ftm,
                   ps.freeThrowsAttempted AS fta,
                   ps.reboundsOffensive AS orb,
                   ps.reboundsDefensive AS drb,
                   gp.team_minutes AS team_minutes,
                   gp.game_poss AS game_poss
            FROM player_statistics ps
            JOIN team_statistics ts
              ON ps.gameId = ts.gameId
             AND ps.playerteamCity = ts.teamCity
             AND ps.playerteamName = ts.teamName
            JOIN game_poss gp
              ON ts.gameId = gp.gameId
             AND ts.teamId = gp.teamId
        ),
        player_poss AS (
            SELECT *,
                   game_poss * (player_minutes / NULLIF(team_minutes, 0)) AS player_poss
            FROM player_games
        ),
        player_season AS (
            SELECT player_id,
                   season_year,
                   SUM(player_poss) AS poss,
                   SUM(points) AS points,
                   SUM(assists) AS assists,
                   SUM(trb) AS trb,
                   SUM(stl) AS stl,
                   SUM(blk) AS blk,
                   SUM(tov) AS tov,
                   SUM(pf) AS pf,
                   SUM(fgm) AS fgm,
                   SUM(fga) AS fga,
                   SUM(fg3m) AS fg3m,
                   SUM(fg3a) AS fg3a,
                   SUM(ftm) AS ftm,
                   SUM(fta) AS fta,
                   SUM(orb) AS orb,
                   SUM(drb) AS drb
            FROM player_poss
            GROUP BY player_id, season_year
        ),
        per100_calc AS (
            SELECT player_id,
                   season_year,
                   points * 100 / NULLIF(poss, 0) AS pts_100,
                   assists * 100 / NULLIF(poss, 0) AS ast_100,
                   trb * 100 / NULLIF(poss, 0) AS trb_100,
                   stl * 100 / NULLIF(poss, 0) AS stl_100,
                   blk * 100 / NULLIF(poss, 0) AS blk_100,
                   tov * 100 / NULLIF(poss, 0) AS tov_100,
                   pf * 100 / NULLIF(poss, 0) AS pf_100,
                   fgm * 100 / NULLIF(poss, 0) AS fg_100,
                   fga * 100 / NULLIF(poss, 0) AS fga_100,
                   fg3m * 100 / NULLIF(poss, 0) AS fg3_100,
                   fg3a * 100 / NULLIF(poss, 0) AS fg3a_100,
                   ftm * 100 / NULLIF(poss, 0) AS ft_100,
                   fta * 100 / NULLIF(poss, 0) AS fta_100,
                   orb * 100 / NULLIF(poss, 0) AS orb_100,
                   drb * 100 / NULLIF(poss, 0) AS drb_100
            FROM player_season
        ),
        per100_csv_agg AS (
            SELECT player_id,
                   season,
                   SUM(mp) AS minutes,
                   SUM(fg_per_100_poss * mp) AS fg_100,
                   SUM(fga_per_100_poss * mp) AS fga_100,
                   SUM(x3p_per_100_poss * mp) AS fg3_100,
                   SUM(x3pa_per_100_poss * mp) AS fg3a_100,
                   SUM(ft_per_100_poss * mp) AS ft_100,
                   SUM(fta_per_100_poss * mp) AS fta_100,
                   SUM(orb_per_100_poss * mp) AS orb_100,
                   SUM(drb_per_100_poss * mp) AS drb_100,
                   SUM(trb_per_100_poss * mp) AS trb_100,
                   SUM(ast_per_100_poss * mp) AS ast_100,
                   SUM(stl_per_100_poss * mp) AS stl_100,
                   SUM(blk_per_100_poss * mp) AS blk_100,
                   SUM(tov_per_100_poss * mp) AS tov_100,
                   SUM(pf_per_100_poss * mp) AS pf_100,
                   SUM(pts_per_100_poss * mp) AS pts_100
            FROM per_100_poss
            GROUP BY player_id, season
        ),
        per100_csv_calc AS (
            SELECT player_id,
                   season,
                   fg_100 / NULLIF(minutes, 0) AS fg_100,
                   fga_100 / NULLIF(minutes, 0) AS fga_100,
                   fg3_100 / NULLIF(minutes, 0) AS fg3_100,
                   fg3a_100 / NULLIF(minutes, 0) AS fg3a_100,
                   ft_100 / NULLIF(minutes, 0) AS ft_100,
                   fta_100 / NULLIF(minutes, 0) AS fta_100,
                   orb_100 / NULLIF(minutes, 0) AS orb_100,
                   drb_100 / NULLIF(minutes, 0) AS drb_100,
                   trb_100 / NULLIF(minutes, 0) AS trb_100,
                   ast_100 / NULLIF(minutes, 0) AS ast_100,
                   stl_100 / NULLIF(minutes, 0) AS stl_100,
                   blk_100 / NULLIF(minutes, 0) AS blk_100,
                   tov_100 / NULLIF(minutes, 0) AS tov_100,
                   pf_100 / NULLIF(minutes, 0) AS pf_100,
                   pts_100 / NULLIF(minutes, 0) AS pts_100
            FROM per100_csv_agg
        )
        SELECT COUNT(*)
        FROM (
            SELECT COALESCE(p.player_id, c.player_id) AS player_id,
                   COALESCE(p.season_year, c.season) AS season
            FROM per100_calc p
            FULL OUTER JOIN per100_csv_calc c
                ON p.player_id = c.player_id
               AND p.season_year = c.season
            WHERE p.player_id IS NULL
               OR c.player_id IS NULL
               OR ABS(COALESCE(p.fg_100, 0) - COALESCE(c.fg_100, 0)) > {eps}
               OR ABS(COALESCE(p.fga_100, 0) - COALESCE(c.fga_100, 0)) > {eps}
               OR ABS(COALESCE(p.fg3_100, 0) - COALESCE(c.fg3_100, 0)) > {eps}
               OR ABS(COALESCE(p.fg3a_100, 0) - COALESCE(c.fg3a_100, 0)) > {eps}
               OR ABS(COALESCE(p.ft_100, 0) - COALESCE(c.ft_100, 0)) > {eps}
               OR ABS(COALESCE(p.fta_100, 0) - COALESCE(c.fta_100, 0)) > {eps}
               OR ABS(COALESCE(p.orb_100, 0) - COALESCE(c.orb_100, 0)) > {eps}
               OR ABS(COALESCE(p.drb_100, 0) - COALESCE(c.drb_100, 0)) > {eps}
               OR ABS(COALESCE(p.trb_100, 0) - COALESCE(c.trb_100, 0)) > {eps}
               OR ABS(COALESCE(p.ast_100, 0) - COALESCE(c.ast_100, 0)) > {eps}
               OR ABS(COALESCE(p.stl_100, 0) - COALESCE(c.stl_100, 0)) > {eps}
               OR ABS(COALESCE(p.blk_100, 0) - COALESCE(c.blk_100, 0)) > {eps}
               OR ABS(COALESCE(p.tov_100, 0) - COALESCE(c.tov_100, 0)) > {eps}
               OR ABS(COALESCE(p.pf_100, 0) - COALESCE(c.pf_100, 0)) > {eps}
               OR ABS(COALESCE(p.pts_100, 0) - COALESCE(c.pts_100, 0)) > {eps}
        ) mismatches;
    "#;

    let v005 = r#"
        WITH advanced AS (
            SELECT season AS season_year,
                   player_id AS player_bref_id,
                   team AS team_abbrev,
                   mp AS minutes,
                   per,
                   ts_percent,
                   usg_percent,
                   ows,
                   dws,
                   ws,
                   bpm,
                   vorp
            FROM advanced_csv
        ),
        stored AS (
            SELECT season_year,
                   player_bref_id,
                   team_abbrev,
                   minutes,
                   per,
                   ts_percent,
                   usg_percent,
                   ows,
                   dws,
                   ws,
                   bpm,
                   vorp
            FROM player_season_advanced
        )
        SELECT COUNT(*)
        FROM (
            SELECT COALESCE(a.player_bref_id, s.player_bref_id) AS player_bref_id,
                   COALESCE(a.season_year, s.season_year) AS season_year,
                   COALESCE(a.team_abbrev, s.team_abbrev) AS team_abbrev
            FROM advanced a
            FULL OUTER JOIN stored s
              ON a.player_bref_id = s.player_bref_id
             AND a.season_year = s.season_year
             AND a.team_abbrev = s.team_abbrev
            WHERE a.player_bref_id IS NULL
               OR s.player_bref_id IS NULL
               OR ABS(COALESCE(a.minutes, 0) - COALESCE(s.minutes, 0)) > {eps}
               OR ABS(COALESCE(a.per, 0) - COALESCE(s.per, 0)) > {eps}
               OR ABS(COALESCE(a.ts_percent, 0) - COALESCE(s.ts_percent, 0)) > {eps}
               OR ABS(COALESCE(a.usg_percent, 0) - COALESCE(s.usg_percent, 0)) > {eps}
               OR ABS(COALESCE(a.ows, 0) - COALESCE(s.ows, 0)) > {eps}
               OR ABS(COALESCE(a.dws, 0) - COALESCE(s.dws, 0)) > {eps}
               OR ABS(COALESCE(a.ws, 0) - COALESCE(s.ws, 0)) > {eps}
               OR ABS(COALESCE(a.bpm, 0) - COALESCE(s.bpm, 0)) > {eps}
               OR ABS(COALESCE(a.vorp, 0) - COALESCE(s.vorp, 0)) > {eps}
        ) mismatches;
    "#;

    let eps = EPSILON.to_string();
    let v002 = v002.replace("{eps}", &eps);
    let v003 = v003.replace("{eps}", &eps);
    let v004 = v004.replace("{eps}", &eps);
    let v005 = v005.replace("{eps}", &eps);

    let checks = vec![
        ("V-001", "Player points match team totals", v001.to_string()),
        ("V-002", "Per-game stats parity", v002),
        ("V-003", "Per-36 stats parity", v003),
        ("V-004", "Per-100 possessions parity", v004),
        ("V-005", "Advanced parity", v005),
    ];

    let mut failures = Vec::new();
    info!("Validation summary:");
    for (id, label, sql) in checks {
        let mismatches = count_mismatches(&conn, &sql)
            .with_context(|| format!("Failed validation query for {}", id))?;
        info!("{} ({}) mismatches: {}", id, label, mismatches);
        if mismatches > 0 {
            failures.push(id);
        }
    }

    if !failures.is_empty() {
        return Err(anyhow::anyhow!(
            "Validation failed: {}",
            failures.join(", ")
        ));
    }

    Ok(())
}

fn count_mismatches(conn: &Connection, sql: &str) -> Result<i64> {
    let count: i64 = conn.query_row(sql, [], |row| row.get(0))?;
    Ok(count)
}

fn ensure_csv_table(conn: &Connection, table_name: &str, csv_path: &Path) -> Result<()> {
    if !csv_path.exists() {
        return Err(anyhow::anyhow!(
            "Required CSV missing: {}",
            csv_path.display()
        ));
    }
    if table_exists(conn, table_name)? {
        return Ok(());
    }
    create_temp_table(conn, table_name, csv_path)
        .with_context(|| format!("Failed to create temp table {table_name}"))?;
    Ok(())
}

fn ensure_table_from_csv_if_missing(
    conn: &Connection,
    table_name: &str,
    csv_path: &Path,
) -> Result<()> {
    if table_exists(conn, table_name)? {
        return Ok(());
    }
    warn!(
        "Table {} missing; creating temp table from {}",
        table_name,
        csv_path.display()
    );
    create_temp_table(conn, table_name, csv_path)
        .with_context(|| format!("Failed to create temp table {table_name}"))?;
    Ok(())
}

fn table_exists(conn: &Connection, table_name: &str) -> Result<bool> {
    let count: i64 = conn.query_row(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = ?",
        [table_name],
        |row| row.get(0),
    )?;
    Ok(count > 0)
}

fn create_temp_table(conn: &Connection, table_name: &str, csv_path: &Path) -> Result<()> {
    let path = csv_path
        .to_string_lossy()
        .replace('\'', "''");
    let sql = format!(
        "CREATE TEMP TABLE {table_name} AS SELECT * FROM read_csv_auto('{path}', HEADER=TRUE)"
    );
    conn.execute(&sql, [])?;
    Ok(())
}
