"""Drop all tables and enums from the public schema, then stamp alembic as base."""
import asyncio
from app.core.database import AsyncSessionFactory
from sqlalchemy import text

async def reset():
    async with AsyncSessionFactory() as session:
        # Drop all tables (cascading to drop views, etc.)
        await session.execute(text("DROP SCHEMA public CASCADE"))
        await session.execute(text("CREATE SCHEMA public"))
        await session.commit()
        print("All objects dropped and public schema recreated.")

asyncio.run(reset())
