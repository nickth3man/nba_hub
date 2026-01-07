"""SQL query helpers for NBA Hub"""
from typing import Optional, List, Dict, Any
from web.database import execute_query, execute_query_one


def get_player_info(player_id: int) -> Optional[Dict[str, Any]]:
    """Get player basic information"""
    query = """
    SELECT
        person_id as player_id,
        display_first_last,
        position,
        height,
        weight,
        birthdate,
        from_year,
        to_year
    FROM common_player_info
    WHERE person_id = ?
    """
    return execute_query_one(query, {"1": player_id})


def get_player_career_stats(player_id: int) -> Optional[Dict[str, Any]]:
    """Get player career statistics"""
    query = """
    SELECT
        COUNT(DISTINCT game_id) as games_played,
        ROUND(AVG(pts), 1) as points_per_game,
        ROUND(AVG(reb), 1) as rebounds_per_game,
        ROUND(AVG(ast), 1) as assists_per_game,
        ROUND(AVG(CASE WHEN fga > 0 THEN CAST(fgm AS FLOAT) / fga * 100 ELSE 0 END), 1) as field_goal_pct,
        ROUND(AVG(CASE WHEN fg3a > 0 THEN CAST(fg3m AS FLOAT) / fg3a * 100 ELSE 0 END), 1) as three_point_pct,
        ROUND(AVG(CASE WHEN fta > 0 THEN CAST(ftm AS FLOAT) / fta * 100 ELSE 0 END), 1) as free_throw_pct
    FROM player_game_stats_silver
    WHERE player_id = ?
    """
    return execute_query_one(query, {"1": player_id})


def get_player_season_stats(player_id: int) -> List[Dict[str, Any]]:
    """Get player season-by-season statistics"""
    query = """
    SELECT
        season_id,
        MAX(team_abbreviation) as team_abbreviation,
        COUNT(DISTINCT game_id) as games_played,
        ROUND(AVG(min), 1) as minutes_per_game,
        ROUND(AVG(pts), 1) as points_per_game,
        ROUND(AVG(reb), 1) as rebounds_per_game,
        ROUND(AVG(ast), 1) as assists_per_game,
        ROUND(AVG(stl), 1) as steals_per_game,
        ROUND(AVG(blk), 1) as blocks_per_game,
        ROUND(AVG(CASE WHEN fga > 0 THEN CAST(fgm AS FLOAT) / fga * 100 ELSE 0 END), 1) as field_goal_pct,
        ROUND(AVG(CASE WHEN fg3a > 0 THEN CAST(fg3m AS FLOAT) / fg3a * 100 ELSE 0 END), 1) as three_point_pct,
        ROUND(AVG(CASE WHEN fta > 0 THEN CAST(ftm AS FLOAT) / fta * 100 ELSE 0 END), 1) as free_throw_pct
    FROM player_game_stats_silver
    WHERE player_id = ?
    GROUP BY season_id
    ORDER BY season_id DESC
    """
    return execute_query(query, {"1": player_id})


def get_player_game_log(
    player_id: int,
    season_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get player game log with optional season filter"""
    if season_id:
        query = """
        SELECT
            game_id,
            game_date,
            matchup,
            wl,
            min,
            pts,
            reb,
            ast,
            stl,
            blk,
            fgm,
            fga,
            ROUND(CASE WHEN fga > 0 THEN CAST(fgm AS FLOAT) / fga * 100 ELSE 0 END, 1) as fg_pct,
            fg3m,
            fg3a,
            ROUND(CASE WHEN fg3a > 0 THEN CAST(fg3m AS FLOAT) / fg3a * 100 ELSE 0 END, 1) as fg3_pct,
            ftm,
            fta,
            ROUND(CASE WHEN fta > 0 THEN CAST(ftm AS FLOAT) / fta * 100 ELSE 0 END, 1) as ft_pct,
            plus_minus
        FROM player_game_stats_silver
        WHERE player_id = ? AND season_id = ?
        ORDER BY game_date DESC
        """
        return execute_query(query, {"1": player_id, "2": season_id})
    else:
        query = """
        SELECT
            game_id,
            game_date,
            matchup,
            wl,
            min,
            pts,
            reb,
            ast,
            stl,
            blk,
            fgm,
            fga,
            ROUND(CASE WHEN fga > 0 THEN CAST(fgm AS FLOAT) / fga * 100 ELSE 0 END, 1) as fg_pct,
            fg3m,
            fg3a,
            ROUND(CASE WHEN fg3a > 0 THEN CAST(fg3m AS FLOAT) / fg3a * 100 ELSE 0 END, 1) as fg3_pct,
            ftm,
            fta,
            ROUND(CASE WHEN fta > 0 THEN CAST(ftm AS FLOAT) / fta * 100 ELSE 0 END, 1) as ft_pct,
            plus_minus
        FROM player_game_stats_silver
        WHERE player_id = ?
        ORDER BY game_date DESC
        LIMIT 100
        """
        return execute_query(query, {"1": player_id})


def get_team_info(team_id: int) -> Optional[Dict[str, Any]]:
    """Get team information"""
    query = """
    SELECT DISTINCT
        team_id,
        full_name as team_name,
        abbreviation,
        city,
        state,
        year_founded
    FROM teams
    WHERE team_id = ?
    """
    return execute_query_one(query, {"1": team_id})


def get_team_roster(
    team_id: int,
    season_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get team roster with optional season filter"""
    if season_id:
        query = """
        SELECT DISTINCT
            p.player_id,
            p.player_name,
            cpi.position,
            cpi.height,
            cpi.weight,
            CAST(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM CAST(cpi.birthdate AS DATE)) AS INTEGER) as age
        FROM player_game_stats_silver p
        LEFT JOIN common_player_info cpi ON p.player_id = cpi.person_id
        WHERE p.team_id = ? AND p.season_id = ?
        ORDER BY p.player_name
        """
        return execute_query(query, {"1": team_id, "2": season_id})
    else:
        # Get most recent season
        query = """
        WITH latest_season AS (
            SELECT MAX(season_id) as season_id
            FROM player_game_stats_silver
            WHERE team_id = ?
        )
        SELECT DISTINCT
            p.player_id,
            p.player_name,
            cpi.position,
            cpi.height,
            cpi.weight,
            CAST(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM CAST(cpi.birthdate AS DATE)) AS INTEGER) as age
        FROM player_game_stats_silver p
        LEFT JOIN common_player_info cpi ON p.player_id = cpi.person_id
        WHERE p.team_id = ? AND p.season_id = (SELECT season_id FROM latest_season)
        ORDER BY p.player_name
        """
        return execute_query(query, {"1": team_id, "2": team_id})


def get_team_schedule(
    team_id: int,
    season_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get team schedule/results"""
    if season_id:
        query = """
        SELECT
            game_id,
            game_date,
            home_team_id,
            visitor_team_id,
            season
        FROM games
        WHERE (home_team_id = ? OR visitor_team_id = ?)
          AND CAST(season AS TEXT) = ?
        ORDER BY game_date DESC
        """
        return execute_query(query, {"1": team_id, "2": team_id, "3": season_id})
    else:
        query = """
        SELECT
            game_id,
            game_date,
            home_team_id,
            visitor_team_id,
            season
        FROM games
        WHERE home_team_id = ? OR visitor_team_id = ?
        ORDER BY game_date DESC
        LIMIT 100
        """
        return execute_query(query, {"1": team_id, "2": team_id})


def get_league_leaders(
    stat: str = 'pts',
    season_id: Optional[str] = None,
    min_games: int = 20,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """Get league leaders for a specific stat"""
    # Map stat names to SQL columns
    stat_mapping = {
        'ppg': 'pts',
        'rpg': 'reb',
        'apg': 'ast',
        'spg': 'stl',
        'bpg': 'blk',
        'fg_pct': 'fg_pct',
        'fg3_pct': 'fg3_pct',
        'ft_pct': 'ft_pct'
    }

    stat_column = stat_mapping.get(stat, 'pts')

    if season_id:
        query = f"""
        WITH player_stats AS (
            SELECT
                player_id,
                player_name,
                MAX(team_abbreviation) as team_abbreviation,
                COUNT(DISTINCT game_id) as games_played,
                ROUND(AVG({stat_column}), 1) as stat_value
            FROM player_game_stats_silver
            WHERE season_id = ?
            GROUP BY player_id, player_name
            HAVING COUNT(DISTINCT game_id) >= ?
        )
        SELECT
            ROW_NUMBER() OVER (ORDER BY stat_value DESC) as rank,
            player_id,
            player_name,
            team_abbreviation,
            games_played,
            stat_value
        FROM player_stats
        ORDER BY stat_value DESC
        LIMIT ?
        """
        return execute_query(query, {"1": season_id, "2": min_games, "3": limit})
    else:
        # Get most recent season
        query = f"""
        WITH latest_season AS (
            SELECT MAX(season_id) as season_id
            FROM player_game_stats_silver
        ),
        player_stats AS (
            SELECT
                p.player_id,
                p.player_name,
                MAX(p.team_abbreviation) as team_abbreviation,
                COUNT(DISTINCT p.game_id) as games_played,
                ROUND(AVG(p.{stat_column}), 1) as stat_value
            FROM player_game_stats_silver p
            CROSS JOIN latest_season ls
            WHERE p.season_id = ls.season_id
            GROUP BY p.player_id, p.player_name
            HAVING COUNT(DISTINCT p.game_id) >= ?
        )
        SELECT
            ROW_NUMBER() OVER (ORDER BY stat_value DESC) as rank,
            player_id,
            player_name,
            team_abbreviation,
            games_played,
            stat_value
        FROM player_stats
        ORDER BY stat_value DESC
        LIMIT ?
        """
        return execute_query(query, {"1": min_games, "2": limit})


def get_recent_games(days: int = 7, limit: int = 20) -> List[Dict[str, Any]]:
    """Get recent games"""
    query = """
    SELECT
        game_id,
        game_date,
        home_team_id,
        visitor_team_id,
        season
    FROM games
    WHERE game_date >= CURRENT_DATE - INTERVAL ? DAY
    ORDER BY game_date DESC
    LIMIT ?
    """
    return execute_query(query, {"1": days, "2": limit})


def search_players(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search for players by name"""
    search_query = """
    SELECT
        person_id as player_id,
        display_first_last as player_name,
        position,
        from_year,
        to_year
    FROM common_player_info
    WHERE LOWER(display_first_last) LIKE LOWER(?)
    ORDER BY
        CASE
            WHEN LOWER(display_first_last) = LOWER(?) THEN 0
            WHEN LOWER(display_first_last) LIKE LOWER(?) THEN 1
            ELSE 2
        END,
        display_first_last
    LIMIT ?
    """
    search_pattern = f"%{query}%"
    exact_pattern = f"{query}%"
    return execute_query(
        search_query,
        {"1": search_pattern, "2": query, "3": exact_pattern, "4": limit}
    )


def get_all_teams() -> List[Dict[str, Any]]:
    """Get all teams"""
    query = """
    SELECT DISTINCT
        team_id,
        full_name as team_name,
        abbreviation,
        city
    FROM teams
    WHERE team_id IS NOT NULL
    ORDER BY full_name
    """
    return execute_query(query)


def get_available_seasons() -> List[str]:
    """Get list of available seasons"""
    query = """
    SELECT DISTINCT season_id
    FROM player_game_stats_silver
    WHERE season_id IS NOT NULL
    ORDER BY season_id DESC
    """
    results = execute_query(query)
    return [r['season_id'] for r in results]
