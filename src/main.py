"""
Application entry point
"""
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api import router
from config.settings import settings
from config.logging_config import setup_logging
from monitoring.metrics import setup_metrics

# Setup logging
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    yield
    # Shutdown
    print("Shutting down gracefully...")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Setup Prometheus metrics
setup_metrics(app)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
