from fastapi import FastAPI

from app.database.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
# Import all models so SQLAlchemy can register them on the metadata
from app.models.user import User
from app.models.benchmark import Benchmark
from app.models.programming_language import ProgrammingLanguage
from app.models.analysis import Analysis
from app.models.report import Report
from app.routers import history_router
from app.routers.comparison_router import router as comparison_router
from app.routers import otp_router
from app.models.feedback import Feedback
# Import routers
from app.routers import (
    user_router,
    benchmark_router,
    programming_language_router,
    analysis_router,
    report_router,
    feedback_router,
)

app = FastAPI(
    title="GreenCode Analyzer API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers on the FastAPI app
app.include_router(user_router.router)
app.include_router(benchmark_router.router)
app.include_router(programming_language_router.router)
app.include_router(analysis_router.router)
app.include_router(
    history_router.router
)
app.include_router(report_router.router)
app.include_router(comparison_router)
app.include_router(otp_router.router)
app.include_router(feedback_router.router)

# Create all database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "GreenCode Analyzer Backend Running"}