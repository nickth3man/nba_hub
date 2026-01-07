"""Team routes for NBA Hub"""
from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache
from typing import Optional

from web.config import TEMPLATES_DIR, CACHE_TTL
from web.utils.queries import (
    get_team_info,
    get_team_roster,
    get_team_schedule,
    get_all_teams,
    get_available_seasons
)
from web.utils.formatters import (
    format_date,
    format_season,
    format_height,
    format_weight
)

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Add custom filters
templates.env.filters['format_date'] = format_date
templates.env.filters['format_season'] = format_season
templates.env.filters['format_height'] = format_height
templates.env.filters['format_weight'] = format_weight


@router.get("", response_class=HTMLResponse)
@cache(expire=CACHE_TTL)
async def teams_list(request: Request):
    """
    Display list of all teams
    """
    teams = get_all_teams()

    return templates.TemplateResponse(
        "team/list.html",
        {
            "request": request,
            "teams": teams,
        }
    )


@router.get("/{team_id}", response_class=HTMLResponse)
@cache(expire=CACHE_TTL)
async def team_overview(request: Request, team_id: int):
    """
    Display team overview page
    """
    # Get team information
    team_info = get_team_info(team_id)
    if not team_info:
        raise HTTPException(status_code=404, detail="Team not found")

    # Get current roster
    roster = get_team_roster(team_id)

    # Get recent schedule
    schedule = get_team_schedule(team_id, limit=10)

    return templates.TemplateResponse(
        "team/overview.html",
        {
            "request": request,
            "team": team_info,
            "roster": roster,
            "schedule": schedule,
        }
    )


@router.get("/{team_id}/roster", response_class=HTMLResponse)
@cache(expire=CACHE_TTL)
async def team_roster(
    request: Request,
    team_id: int,
    season: Optional[str] = Query(None, description="Season ID")
):
    """
    Display team roster for a specific season
    """
    # Get team information
    team_info = get_team_info(team_id)
    if not team_info:
        raise HTTPException(status_code=404, detail="Team not found")

    # Get roster
    roster = get_team_roster(team_id, season)

    # Get available seasons
    available_seasons = get_available_seasons()

    return templates.TemplateResponse(
        "team/roster.html",
        {
            "request": request,
            "team": team_info,
            "roster": roster,
            "selected_season": season or (available_seasons[0] if available_seasons else None),
            "available_seasons": available_seasons,
        }
    )


@router.get("/{team_id}/schedule", response_class=HTMLResponse)
@cache(expire=CACHE_TTL)
async def team_schedule(
    request: Request,
    team_id: int,
    season: Optional[str] = Query(None, description="Season ID")
):
    """
    Display team schedule/results for a specific season
    """
    # Get team information
    team_info = get_team_info(team_id)
    if not team_info:
        raise HTTPException(status_code=404, detail="Team not found")

    # Get schedule
    schedule = get_team_schedule(team_id, season)

    # Get available seasons
    available_seasons = get_available_seasons()

    return templates.TemplateResponse(
        "team/schedule.html",
        {
            "request": request,
            "team": team_info,
            "schedule": schedule,
            "selected_season": season or (available_seasons[0] if available_seasons else None),
            "available_seasons": available_seasons,
        }
    )
