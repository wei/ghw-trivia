"""FastAPI application initialization and configuration."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from trivia_api.config import get_settings
from trivia_api.database import Base, engine
from trivia_api.errors import TriviaAPIException
from trivia_api.api import session, question, answer, attempts, leaderboard

# Configure logging
settings = get_settings()
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Application started")

    yield

    # Shutdown
    logger.info("Application shutting down")


# Create FastAPI app instance
app = FastAPI(
    title="Trivia API",
    description="REST API for managing trivia question sessions, user answers, and leaderboard rankings",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(TriviaAPIException)
async def trivia_api_exception_handler(request: Request, exc: TriviaAPIException):
    """Handle Trivia API exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with user-friendly messages."""
    errors = exc.errors()
    message = "Validation error: " + ", ".join(
        [f"{error['loc'][-1]}: {error['msg']}" for error in errors]
    )
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": message,
        },
    )


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "trivia-api",
    }


# Include API routers
app.include_router(session.router)
app.include_router(question.router)
app.include_router(answer.router)
app.include_router(attempts.router)
app.include_router(leaderboard.router)

logger.info("FastAPI application initialized")
