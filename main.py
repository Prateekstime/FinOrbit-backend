from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, Text
from database.database import Base

from config import settings
from database.database import get_db, init_db, close_db, test_db_connection, Base, engine

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting up FinOrbit Backend...")

    # Check Supabase configuration with proper error handling
    try:
        if hasattr(settings, 'is_supabase_configured'):
            is_configured = settings.is_supabase_configured
        else:
            # Fallback check
            is_configured = all([
                getattr(settings, 'SUPABASE_URL', ''),
                getattr(settings, 'SUPABASE_KEY', ''),
                getattr(settings, 'SUPABASE_DB_URL', '')
            ])

        if not is_configured:
            logger.warning("⚠️ Supabase is not properly configured. Check your .env file.")
        else:
            logger.info("✅ Supabase configuration loaded successfully")
    except Exception as e:
        logger.error(f"Error checking Supabase configuration: {str(e)}")

    # Initialize database
    try:
        await init_db()
        logger.info("✅ Database initialized")

        # Test connection
        if await test_db_connection():
            logger.info("✅ Database connection successful")
        else:
            logger.warning("⚠️ Database connection failed - check your configuration")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {str(e)}")

    yield

    # Shutdown
    logger.info("Shutting down FinOrbit Backend...")
    try:
        await close_db()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Error closing database: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title="FinOrbit - Loan Management System",
    version="1.0.0",
    description="FinOrbit Backend API for Loan Management",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# SIMPLE MODELS (for demo purposes)
# ============================================
#


class Branch(Base):
    """Simple Branch model for testing"""
    __tablename__ = "branches"
    __table_args__ = {"schema": "public"}  # Use public schema for testing

    branch_id = Column(Integer, primary_key=True, autoincrement=True)
    branch_code = Column(String(20), unique=True, nullable=False)
    branch_name = Column(String(100), nullable=False)
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100), default="India")
    pincode = Column(String(10))
    phone = Column(String(15))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ============================================
# API ENDPOINTS
# ============================================

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Welcome to FinOrbit Backend API",
        "version": "1.0.0",
        "status": "running",
        "supabase_configured": settings.is_supabase_configured if hasattr(settings,
                                                                          'is_supabase_configured') else "unknown"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    db_status = await test_db_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "supabase_configured": settings.is_supabase_configured if hasattr(settings,                                         'is_supabase_configured') else False,
        "debug": settings.DEBUG if hasattr(settings, 'DEBUG') else False
    }


@app.get("/config-check")
async def check_config():
    """
    Check configuration
    """
    return {
        "supabase_url": settings.SUPABASE_URL[:20] + "..." if settings.SUPABASE_URL else "Not configured",
        "supabase_key": "Configured" if settings.SUPABASE_KEY else "Not configured",
        "db_url": "Configured" if settings.SUPABASE_DB_URL else "Not configured",
        "debug": settings.DEBUG if hasattr(settings, 'DEBUG') else False,
        "is_configured": settings.is_supabase_configured if hasattr(settings, 'is_supabase_configured') else False
    }


@app.get("/branches")
async def get_branches(db: AsyncSession = Depends(get_db)):
    """
    Get all branches
    """
    from sqlalchemy import select
    try:
        result = await db.execute(select(Branch))
        branches = result.scalars().all()
        return [
            {
                "branch_id": b.branch_id,
                "branch_code": b.branch_code,
                "branch_name": b.branch_name,
                "city": b.city,
                "state": b.state,
                "country": b.country,
                "is_active": b.is_active
            }
            for b in branches
        ]
    except Exception as e:
        logger.error(f"Error fetching branches: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/branches")
async def create_branch(
        branch_code: str,
        branch_name: str,
        city: str = None,
        state: str = None,
        db: AsyncSession = Depends(get_db)
):
    """
    Create a new branch
    """
    try:
        branch = Branch(
            branch_code=branch_code,
            branch_name=branch_name,
            city=city,
            state=state
        )
        db.add(branch)
        await db.commit()
        await db.refresh(branch)
        return {
            "message": "Branch created successfully",
            "branch": {
                "branch_id": branch.branch_id,
                "branch_code": branch.branch_code,
                "branch_name": branch.branch_name,
                "city": branch.city,
                "state": branch.state
            }
        }
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating branch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# RUN THE APPLICATION
# ============================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG if hasattr(settings, 'DEBUG') else True
    )