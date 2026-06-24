from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.user_database.schema import create_tables

from backend.api.long_term import router as long_term_router
from backend.api.dashboard import router as dashboard_router
from backend.api.swing import router as swing_router
from backend.api.ipo import router as ipo_router
from backend.api.auth import router as auth_router
from backend.api.admin import router as admin_router
from backend.api.portfolio import router as portfolio_router
from backend.api.portfolio_analysis import router as portfolio_analysis_router

app = FastAPI()

# Static
app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="frontend/templates"
)

# Startup
@app.on_event("startup")
def startup():
    create_tables()
    print("Green Bull Rider Ready")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Health
@app.get("/")
def home():
    return {
        "app": "Green Bull Rider V6",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

# ======================
# USER UI
# ======================

@app.get("/ui/dashboard")
async def ui_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user/dashboard.html"
    )

@app.get("/ui/long-term")
async def ui_long_term(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user/long_term.html"
    )

@app.get("/ui/swing")
async def ui_swing(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user/swing.html"
    )

@app.get("/ui/ipo")
async def ui_ipo(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user/ipo.html"
    )

@app.get("/ui/portfolio")
async def ui_portfolio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user/portfolio.html"
    )

@app.get("/ui/portfolio-analysis")
async def ui_portfolio_analysis(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user/portfolio_analysis.html"
    )

@app.get("/ui/watchlists")
async def ui_watchlists(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user/watchlists.html"
    )

@app.get("/ui/market")
async def ui_market(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user/market_monitor.html"
    )

@app.get("/ui/profile")
async def ui_profile(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user/profile.html"
    )

# ======================
# ADMIN UI
# ======================

@app.get("/admin")
async def admin_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/login.html"
    )

@app.get("/admin/dashboard")
async def admin_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html"
    )

@app.get("/admin/users")
async def admin_users(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/users.html"
    )

@app.get("/admin/settings")
async def admin_settings(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/settings.html"
    )

@app.get("/admin/data-engine")
async def admin_data_engine(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/data_engine.html"
    )

# ======================
# API ROUTERS
# ======================

app.include_router(long_term_router)
app.include_router(dashboard_router)
app.include_router(swing_router)
app.include_router(ipo_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(portfolio_router)
app.include_router(portfolio_analysis_router)
