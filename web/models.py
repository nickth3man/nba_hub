"""Pydantic models for NBA Hub Web Application"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date, datetime


class PlayerInfo(BaseModel):
    """Player basic information"""
    player_id: int
    display_first_last: str
    position: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    birthdate: Optional[str] = None
    from_year: Optional[int] = None
    to_year: Optional[int] = None


class PlayerCareerStats(BaseModel):
    """Player career statistics"""
    games_played: int
    points_per_game: float
    rebounds_per_game: float
    assists_per_game: float
    field_goal_pct: float
    three_point_pct: Optional[float] = None
    free_throw_pct: Optional[float] = None


class PlayerSeasonStats(BaseModel):
    """Player season statistics"""
    season_id: str
    team_abbreviation: Optional[str] = None
    games_played: int
    minutes_per_game: float
    points_per_game: float
    rebounds_per_game: float
    assists_per_game: float
    steals_per_game: float
    blocks_per_game: float
    field_goal_pct: float
    three_point_pct: Optional[float] = None
    free_throw_pct: Optional[float] = None


class GameLog(BaseModel):
    """Player game log entry"""
    game_id: str
    game_date: str
    matchup: str
    wl: Optional[str] = None
    min: Optional[float] = None
    pts: Optional[int] = None
    reb: Optional[int] = None
    ast: Optional[int] = None
    stl: Optional[int] = None
    blk: Optional[int] = None
    fgm: Optional[int] = None
    fga: Optional[int] = None
    fg_pct: Optional[float] = None
    fg3m: Optional[int] = None
    fg3a: Optional[int] = None
    fg3_pct: Optional[float] = None
    ftm: Optional[int] = None
    fta: Optional[int] = None
    ft_pct: Optional[float] = None
    plus_minus: Optional[int] = None


class TeamInfo(BaseModel):
    """Team information"""
    team_id: int
    team_name: str
    abbreviation: str
    city: Optional[str] = None
    state: Optional[str] = None
    year_founded: Optional[int] = None


class TeamPlayer(BaseModel):
    """Player on a team roster"""
    player_id: int
    player_name: str
    position: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    age: Optional[int] = None


class GameInfo(BaseModel):
    """Game information"""
    game_id: str
    game_date: str
    home_team_id: int
    home_team_name: str
    visitor_team_id: int
    visitor_team_name: str
    home_team_score: Optional[int] = None
    visitor_team_score: Optional[int] = None
    season: Optional[int] = None


class LeaderEntry(BaseModel):
    """League leader entry"""
    rank: int
    player_id: int
    player_name: str
    team_abbreviation: Optional[str] = None
    games_played: int
    stat_value: float
    stat_name: str


class SearchResult(BaseModel):
    """Search result for player/team"""
    id: int
    name: str
    type: str  # 'player' or 'team'
    description: Optional[str] = None
