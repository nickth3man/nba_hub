"""Main FastAPI application for NBA Hub"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from web.config import (
    APP_TITLE,
    APP_DESCRIPTION,
    APP_VERSION,
    STATIC_DIR,
    TEMPLATES_DIR,
    CACHE_TTL
)
from web.routers import players, teams, leaders, games
from web.utils.queries import get_recent_games, get_league_leaders
from web.utils.formatters import format_date, format_stat


# Initialize FastAPI app
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Add custom filters to Jinja2
templates.env.filters['format_date'] = format_date
templates.env.filters['format_stat'] = format_stat


# Include routers
app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(leaders.router, prefix="/leaders", tags=["leaders"])
app.include_router(games.router, prefix="/games", tags=["games"])


@app.on_event("startup")
async def startup():
    """Initialize cache on startup"""
    FastAPICache.init(InMemoryBackend())


@app.get("/", response_class=HTMLResponse)
@cache(expire=CACHE_TTL)
async def home(request: Request):
    """
    Home page with recent games and top performers
    """
    try:
        # Get recent games
        recent_games = get_recent_games(days=7, limit=10)

        # Get top scorers
        top_scorers = get_league_leaders(stat='ppg', limit=10)

        # Get top rebounders
        top_rebounders = get_league_leaders(stat='rpg', limit=5)

        # Get top assists
        top_assists = get_league_leaders(stat='apg', limit=5)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "recent_games": recent_games,
                "top_scorers": top_scorers,
                "top_rebounders": top_rebounders,
                "top_assists": top_assists,
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(e),
                "recent_games": [],
                "top_scorers": [],
                "top_rebounders": [],
                "top_assists": [],
            }
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": APP_VERSION}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
