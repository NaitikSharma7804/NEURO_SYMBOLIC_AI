"""SQLAlchemy database connection and session management."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config.settings import settings

# Handle sqlite async url format
db_url = settings.DATABASE_URL
if db_url.startswith("sqlite:///"):
    async_db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///")
else:
    async_db_url = db_url

engine = create_async_engine(async_db_url, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
