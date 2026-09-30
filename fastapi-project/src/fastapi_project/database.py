from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5200/employee_hub"

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
    )

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()    