# app/db/migration.py
"""
Database migration utilities for automatic deployment
Runs Alembic migrations programmatically
"""
import os
from pathlib import Path
from alembic import command
from alembic.config import Config
import logging

logger = logging.getLogger(__name__)


def get_alembic_config() -> Config:
    """
    Get Alembic configuration object
    """
    # Get the project root directory (where alembic.ini is located)
    current_file = Path(__file__).resolve()
    api_root = current_file.parent.parent.parent  # Go up to /apps/api
    alembic_ini_path = api_root / "alembic.ini"
    
    if not alembic_ini_path.exists():
        raise FileNotFoundError(f"alembic.ini not found at {alembic_ini_path}")
    
    # Create Alembic config
    alembic_cfg = Config(str(alembic_ini_path))
    
    # Set the script location (where migrations are stored)
    alembic_cfg.set_main_option("script_location", str(api_root / "alembic"))
    
    # Override database URL from environment variable
    database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/aiapp")
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)
    
    return alembic_cfg


async def run_migrations():
    """
    Run all pending Alembic migrations
    This function is called during application startup
    """
    try:
        logger.info("🔄 Starting database migrations...")
        alembic_cfg = get_alembic_config()
        
        # Run migrations synchronously (Alembic is not async)
        # We run it in the default event loop to avoid blocking
        import asyncio
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, command.upgrade, alembic_cfg, "head")
        
        logger.info("✓ Database migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Database migration failed: {e}")
        # Don't raise the exception - let the app start anyway
        # The health check endpoint will catch database issues
        return False

