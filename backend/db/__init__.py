from .session import AsyncSessionLocal, engine
from .base import Base

async def init_db():
    from .models import User,Task
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

