"""Player routes for NBA Hub"""
from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache
from typing import Optional

from web.config import TEMPLATES_DIR, CACHE_TTL
from web.utils.queries import (
    get_player_info,
    get_player_career_stats,
    get_player_season_stats,
    get_player_game_log,
    search_players,
    get_available_seasons
)
from web.utils.formatters import (
    format_stat,
    format_percentage,
    format_date,
    format_season,
    format_height,
    format_weight
)

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Add custom filters
templates.env.filters['format_stat'] = format_stat
templates.env.filters['format_percentage'] = format_percentage
templates.env.filters['format_date'] = format_date
templates.env.filters['format_season'] = format_season
templates.env.filters['format_height'] = format_height
templates.env.filters['format_weight'] = format_weight


@router.get("/{player_id}", response_class=HTMLResponse)
@cache(expire=CACHE_TTL)
async def player_profile(request: Request, player_id: int):
    """
    Display player profile page with career stats and season-by-season breakdown
    """
    # Get player information
    player_info = get_player_info(player_id)
    if not player_info:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get career stats
    career_stats = get_player_career_stats(player_id)

    # Get season-by-season stats
    season_stats = get_player_season_stats(player_id)

    # Get available seasons for this player
    available_seasons = [stat['season_id'] for stat in season_stats]

    return templates.TemplateResponse(
        "player/profile.html",
        {
            "request": request,
            "player": player_info,
            "career_stats": career_stats,
            "season_stats": season_stats,
            "available_seasons": available_seasons,
        }
    )


@router.get("/{player_id}/gamelog", response_class=HTMLResponse)
@cache(expire=CACHE_TTL)
async def player_game_log(
    request: Request,
    player_id: int,
    season: Optional[str] = Query(None, description="Season ID")
):
    """
    Display player game log for a specific season
    """
    # Get player information
    player_info = get_player_info(player_id)
    if not player_info:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get season stats to determine available seasons
    season_stats = get_player_season_stats(player_id)
    available_seasons = [stat['season_id'] for stat in season_stats]

    # Use most recent season if none specified
    if not season and available_seasons:
        season = available_seasons[0]

    # Get game log
    game_log = get_player_game_log(player_id, season)

    return templates.TemplateResponse(
        "player/game_log.html",
        {
            "request": request,
            "player": player_info,
            "game_log": game_log,
            "selected_season": season,
            "available_seasons": available_seasons,
        }
    )


@router.get("/search", response_class=HTMLResponse)
async def search_players_page(request: Request, q: Optional[str] = Query(None)):
    """
    Player search page
    """
    results = []
    if q:
        results = search_players(q, limit=50)

    return templates.TemplateResponse(
        "player/search.html",
        {
            "request": request,
            "query": q or "",
            "results": results,
        }
    )


@router.get("/api/search/players", response_class=JSONResponse)
async def api_search_players(q: str = Query(..., min_length=2)):
    """
    API endpoint for player search autocomplete
    """
    results = search_players(q, limit=10)
    return results
