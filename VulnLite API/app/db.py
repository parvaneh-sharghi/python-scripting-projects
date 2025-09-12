# app/db.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from typing import AsyncGenerator

# Async database tools from SQLAlchemy
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from .config import DATABASE_URL

# Create async database engine using asyncpg driver
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Create async session factory (like a connection to the DB for each request)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Define the Vulnerability table using ORM style
class Vulnerability(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)   # Auto-increment primary key
    title: str                                                 # Title (required)
    severity: str = Field(default="medium", index=True)        # Severity with index
    status: str = Field(default="open", index=True)            # Status with index
    notes: Optional[str] = None                                # Optional notes
    discovered_at: datetime = Field(default_factory=datetime.utcnow, index=True)  # Auto timestamp
    archived: bool = Field(default=False, index=True)          # Archived flag

# Init function: create tables if not exist
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency to get a database session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session