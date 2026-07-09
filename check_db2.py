"""Check database state."""
import asyncio
from app.core.database import AsyncSessionFactory
from sqlalchemy import text

async def check():
    async with AsyncSessionFactory() as session:
        # Check alembic_version
        result = await session.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        )
        tables = result.fetchall()
        print("Tables:", [t[0] for t in tables])

        result2 = await session.execute(text("SELECT typname FROM pg_type WHERE typcategory = 'E' ORDER BY typname"))
        enums = result2.fetchall()
        print("Enums:", [e[0] for e in enums])

        if "alembic_version" in [t[0] for t in tables]:
            result3 = await session.execute(text("SELECT * FROM alembic_version"))
            print("Alembic version:", result3.fetchall())

asyncio.run(check())
