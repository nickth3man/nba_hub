"""Data formatting utilities for NBA Hub"""
from typing import Optional, Any
from datetime import datetime


def format_stat(value: Optional[float], decimal_places: int = 1) -> str:
    """Format a stat value with specified decimal places"""
    if value is None:
        return "-"
    return f"{value:.{decimal_places}f}"


def format_percentage(value: Optional[float]) -> str:
    """Format a percentage value"""
    if value is None or value == 0:
        return "-"
    return f"{value:.1f}%"


def format_height(height: Optional[str]) -> str:
    """Format height string"""
    if not height:
        return "-"
    return height


def format_weight(weight: Optional[str]) -> str:
    """Format weight string"""
    if not weight:
        return "-"
    return f"{weight} lbs" if weight.isdigit() else weight


def format_date(date_str: Optional[str]) -> str:
    """Format date string to readable format"""
    if not date_str:
        return "-"

    try:
        # Try parsing ISO format
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%b %d, %Y")
    except:
        try:
            # Try parsing common date formats
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%b %d, %Y")
        except:
            return date_str


def format_season(season_id: Optional[str]) -> str:
    """Format season ID to readable format (e.g., '22023' -> '2023-24')"""
    if not season_id:
        return "-"

    try:
        # Season ID format is typically '2YYYY' where YYYY is the starting year
        year_str = season_id.lstrip('2')
        if len(year_str) == 4:
            year = int(year_str)
            return f"{year}-{str(year + 1)[-2:]}"
        return season_id
    except:
        return season_id


def format_minutes(minutes: Optional[float]) -> str:
    """Format minutes played"""
    if minutes is None:
        return "-"

    total_minutes = int(minutes)
    seconds = int((minutes - total_minutes) * 60)
    return f"{total_minutes}:{seconds:02d}"


def format_plus_minus(value: Optional[int]) -> str:
    """Format plus/minus stat"""
    if value is None:
        return "-"

    if value > 0:
        return f"+{value}"
    return str(value)


def format_record(wins: int, losses: int) -> str:
    """Format win-loss record"""
    return f"{wins}-{losses}"


def format_team_name(team_name: Optional[str], abbreviation: Optional[str] = None) -> str:
    """Format team name with optional abbreviation"""
    if not team_name:
        return "-"

    if abbreviation:
        return f"{team_name} ({abbreviation})"
    return team_name


def format_player_name(first_name: str, last_name: str) -> str:
    """Format player name"""
    return f"{first_name} {last_name}"


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_rank(rank: int) -> str:
    """Format rank with proper suffix (1st, 2nd, 3rd, etc.)"""
    if 10 <= rank % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(rank % 10, 'th')

    return f"{rank}{suffix}"
