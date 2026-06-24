from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.long_term import router as long_term_router
from backend.api.dashboard import router as dashboard_router
from backend.api.swing import router as swing_router
from backend.api.ipo import router as ipo_router
from backend.api.auth import router as auth_router
from backend.user_database.schema import create_tables
from backend.api.admin import router as admin_router
from backend.api.portfolio import router as portfolio_router
from backend.api.portfolio_analysis import router as portfolio_analysis_router

app = FastAPI(
    title="Green Bull Rider API",
    version="1.0.0"
)
@app.on_event("startup")
def startup():

    create_tables()

    print("Users DB Ready")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():

    return {
        "app": "Green Bull Rider",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }

app.include_router(long_term_router)
app.include_router(dashboard_router)
app.include_router(swing_router)
app.include_router(ipo_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(portfolio_router)
app.include_router(portfolio_analysis_router)

