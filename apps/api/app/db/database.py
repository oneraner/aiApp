# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os
import ssl

# Load .env early to ensure DATABASE_URL is available
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/aiapp")

# Check if using external database that requires SSL
# Covers: Render, Supabase, Neon, GCP Cloud SQL, or explicit production environment
is_external_db = (
    any(host in DATABASE_URL for host in ["render.com", "neon.tech", "supabase", "cloudsql", "pooler.supabase.com"])
    or os.getenv("ENVIRONMENT") == "production"
)

# SSL configuration for external databases
connect_args = {}
if is_external_db:
    # Create SSL context for secure connection
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connect_args["ssl"] = ssl_context

# Supabase connection pooler (Supavisor) doesn't support prepared statements
# asyncpg uses prepared statements by default, which causes errors through poolers
is_pooler = "pooler.supabase.com" in DATABASE_URL
if is_pooler:
    connect_args["prepared_statement_cache_size"] = 0
    connect_args["statement_cache_size"] = 0

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("ENVIRONMENT") == "development",  # Only echo in development
    future=True,
    connect_args=connect_args,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base class for models
Base = declarative_base()


async def get_db():
    """
    Dependency for FastAPI to get database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database tables
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
