from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = "postgresql+asyncpg://postgres.mlxhpsnpjjxfoyzgumfs:PRjkKJc85se1nWWz@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
