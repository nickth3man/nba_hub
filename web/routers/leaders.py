"""League leaders routes for NBA Hub"""
from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache
from typing import Optional

from web.config import TEMPLATES_DIR, CACHE_TTL, MIN_GAMES_PLAYED
from web.utils.queries import get_league_leaders, get_available_seasons
from web.utils.formatters import format_stat, format_season

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Add custom filters
templates.env.filters['format_stat'] = format_stat
templates.env.filters['format_season'] = format_season


@router.get("", response_class=HTMLResponse)
@cache(expire=CACHE_TTL)
async def league_leaders(
    request: Request,
    stat: str = Query('ppg', description="Stat category"),
    season: Optional[str] = Query(None, description="Season ID"),
    min_games: int = Query(MIN_GAMES_PLAYED, description="Minimum games played")
):
    """
    Display league leaders page
    """
    # Get available seasons
    available_seasons = get_available_seasons()

    # Use most recent season if none specified
    if not season and available_seasons:
        season = available_seasons[0]

    # Get leaders for the specified stat
    leaders = get_league_leaders(
        stat=stat,
        season_id=season,
        min_games=min_games,
        limit=50
    )

    # Define available stat categories
    stat_categories = {
        'ppg': 'Points Per Game',
        'rpg': 'Rebounds Per Game',
        'apg': 'Assists Per Game',
        'spg': 'Steals Per Game',
        'bpg': 'Blocks Per Game',
        'fg_pct': 'Field Goal Percentage',
        'fg3_pct': '3-Point Percentage',
        'ft_pct': 'Free Throw Percentage',
    }

    return templates.TemplateResponse(
        "leaders/season.html",
        {
            "request": request,
            "leaders": leaders,
            "stat": stat,
            "stat_name": stat_categories.get(stat, stat.upper()),
            "selected_season": season,
            "available_seasons": available_seasons,
            "min_games": min_games,
            "stat_categories": stat_categories,
        }
    )
