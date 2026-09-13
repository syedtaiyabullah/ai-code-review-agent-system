"""FastAPI application for AI Code Review Agent."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from src.config import settings
from src.models import CodeSubmission, ReviewResult
from src.agents import ReviewOrchestrator
from src.utils.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global orchestrator instance
orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    global orchestrator
    logger.info("Starting AI Code Review Agent API...")
    orchestrator = ReviewOrchestrator()
    logger.info("Review orchestrator initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Code Review Agent API...")


# Create FastAPI app
app = FastAPI(
    title="AI Code Review Agent",
    description="Intelligent multi-agent code review system powered by LLMs",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AI Code Review Agent",
        "version": "0.1.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "health": "/health",
            "review": "/api/v1/review",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "model": settings.default_model,
        "parallel_agents": settings.enable_parallel_agents
    }


@app.post("/api/v1/review", response_model=ReviewResult)
async def review_code(submission: CodeSubmission):
    """Review code and return findings.
    
    Args:
        submission: Code submission with code, language, and review options
        
    Returns:
        ReviewResult with all issues and summary
        
    Raises:
        HTTPException: If review fails
    """
    try:
        logger.info(f"Received review request for {submission.filename} ({submission.language})")
        
        # Validate code length
        if len(submission.code) > settings.max_code_length:
            raise HTTPException(
                status_code=400,
                detail=f"Code too long. Max length: {settings.max_code_length} characters"
            )
        
        if not submission.code.strip():
            raise HTTPException(
                status_code=400,
                detail="Code cannot be empty"
            )
        
        # Execute review
        result = await orchestrator.review_code(
            code=submission.code,
            language=submission.language,
            filename=submission.filename,
            context=submission.context,
            review_types=submission.review_types
        )
        
        logger.info(f"Review completed: {result.submission_id} - {result.total_issues} issues found")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Review failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Review failed: {str(e)}"
        )


@app.get("/api/v1/supported-languages")
async def get_supported_languages():
    """Get list of supported programming languages."""
    return {
        "languages": [
            {"code": "python", "name": "Python", "extensions": [".py"]},
            {"code": "javascript", "name": "JavaScript", "extensions": [".js", ".jsx"]},
            {"code": "typescript", "name": "TypeScript", "extensions": [".ts", ".tsx"]},
            {"code": "java", "name": "Java", "extensions": [".java"]},
            {"code": "go", "name": "Go", "extensions": [".go"]},
            {"code": "rust", "name": "Rust", "extensions": [".rs"]},
            {"code": "cpp", "name": "C++", "extensions": [".cpp", ".cc", ".cxx"]},
            {"code": "c", "name": "C", "extensions": [".c", ".h"]}
        ]
    }


@app.get("/api/v1/review-types")
async def get_review_types():
    """Get available review types."""
    return {
        "review_types": [
            {
                "code": "bug",
                "name": "Bug Detection",
                "description": "Identifies potential bugs, logic errors, and edge cases"
            },
            {
                "code": "security",
                "name": "Security Analysis",
                "description": "Detects security vulnerabilities and unsafe patterns"
            },
            {
                "code": "performance",
                "name": "Performance Review",
                "description": "Suggests performance optimizations and identifies bottlenecks"
            },
            {
                "code": "quality",
                "name": "Code Quality",
                "description": "Checks code quality, best practices, and maintainability"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )
