import asyncio
from app.core.database import AsyncSessionFactory
from sqlalchemy import text

async def check():
    async with AsyncSessionFactory() as session:
        result = await session.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        )
        tables = result.fetchall()
        print("Tables in database:")
        for t in tables:
            print(f"  {t[0]}")
        result2 = await session.execute(
            text("SELECT typname FROM pg_type WHERE typcategory = 'E' ORDER BY typname")
        )
        enums = result2.fetchall()
        print("Enums in database:")
        for e in enums:
            print(f"  {e[0]}")

asyncio.run(check())
