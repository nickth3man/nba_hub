import duckdb
import pandas as pd
from src.core.database import get_db_connection


def get_seasons():
    con = get_db_connection()
    df = con.execute(
        "SELECT * FROM unified_seasons ORDER BY season_year DESC"
    ).fetchdf()
    con.close()
    return df


def get_teams(season_year=None):
    con = get_db_connection()
    if season_year:
        # This requires joining with team history or standings to see active teams for that season
        # For now, just return all teams
        query = """
            SELECT t.team_id, th.city, th.nickname, th.abbreviation 
            FROM unified_teams t
            JOIN unified_team_history th ON t.team_id = th.team_id
            WHERE th.is_active = TRUE
            ORDER BY th.city
        """
    else:
        query = """
            SELECT t.team_id, th.city, th.nickname, th.abbreviation 
            FROM unified_teams t
            JOIN unified_team_history th ON t.team_id = th.team_id
            WHERE th.is_active = TRUE
            ORDER BY th.city
        """
    df = con.execute(query).fetchdf()
    con.close()
    return df


def get_player_search(name_query):
    con = get_db_connection()
    query = f"""
        SELECT player_id, display_name, from_year, to_year 
        FROM unified_players 
        WHERE LOWER(display_name) LIKE '%{name_query.lower()}%'
        LIMIT 20
    """
    df = con.execute(query).fetchdf()
    con.close()
    return df


def get_player_profile(player_id):
    con = get_db_connection()
    # Basic info
    info = con.execute(
        f"SELECT * FROM unified_players WHERE player_id = {player_id}"
    ).fetchdf()

    # Season Stats (Totals)
    # We need to aggregate boxscores if we don't have a pre-calculated totals table
    # But we have unified_player_season_advanced.
    # Let's aggregate boxscores for basic stats.
    stats_query = f"""
        SELECT 
            s.season_year,
            t.abbreviation as team,
            COUNT(DISTINCT pb.game_id) as g,
            SUM(pb.minutes) as mp,
            SUM(pb.points) as pts,
            SUM(pb.rebounds_total) as trb,
            SUM(pb.assists) as ast,
            SUM(pb.steals) as stl,
            SUM(pb.blocks) as blk,
            SUM(pb.fgm) as fg,
            SUM(pb.fga) as fga,
            CASE WHEN SUM(pb.fga) > 0 THEN CAST(SUM(pb.fgm) AS DOUBLE) / SUM(pb.fga) ELSE 0 END as fg_pct
        FROM unified_player_boxscores pb
        JOIN unified_games g ON pb.game_id = g.game_id
        JOIN unified_seasons s ON g.season_id = s.season_id
        JOIN unified_team_history t ON pb.team_id = t.team_id
        WHERE pb.player_id = {player_id}
        GROUP BY s.season_year, t.abbreviation
        ORDER BY s.season_year DESC
    """
    stats = con.execute(stats_query).fetchdf()

    con.close()
    return info, stats


def get_standings(season_year):
    # Calculate standings from game results
    con = get_db_connection()

    # This is complex. We need to sum wins/losses for each team in the given season.
    # Simplified version:
    query = f"""
        WITH team_games AS (
            SELECT 
                home_team_id as team_id,
                CASE WHEN home_points > away_points THEN 1 ELSE 0 END as win,
                1 as game
            FROM unified_games g
            JOIN unified_seasons s ON g.season_id = s.season_id
            WHERE s.season_year = {season_year} AND g.season_type = 'REG'
            
            UNION ALL
            
            SELECT 
                away_team_id as team_id,
                CASE WHEN away_points > home_points THEN 1 ELSE 0 END as win,
                1 as game
            FROM unified_games g
            JOIN unified_seasons s ON g.season_id = s.season_id
            WHERE s.season_year = {season_year} AND g.season_type = 'REG'
        )
        SELECT 
            th.city || ' ' || th.nickname as team_name,
            SUM(tg.win) as w,
            SUM(tg.game) - SUM(tg.win) as l,
            CAST(SUM(tg.win) AS DOUBLE) / SUM(tg.game) as pct
        FROM team_games tg
        JOIN unified_team_history th ON tg.team_id = th.team_id
        GROUP BY th.city, th.nickname
        ORDER BY pct DESC
    """
    df = con.execute(query).fetchdf()
    con.close()
    return df
