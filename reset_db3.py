"""Reset database: drop public schema and recreate."""
import asyncio
from app.core.database import AsyncSessionFactory
from sqlalchemy import text

async def reset():
    async with AsyncSessionFactory() as session:
        await session.execute(text("DROP SCHEMA public CASCADE"))
        await session.execute(text("CREATE SCHEMA public"))
        await session.commit()
        print("Database reset complete.")

asyncio.run(reset())
