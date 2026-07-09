"""Drop all types (enums) in the public schema manually."""
import asyncio
from app.core.database import AsyncSessionFactory
from sqlalchemy import text

async def reset():
    async with AsyncSessionFactory() as session:
        # First drop all tables
        result = await session.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        ))
        tables = result.fetchall()
        print(f"Tables found: {[t[0] for t in tables]}")

        # Drop all types (enums)
        result2 = await session.execute(text(
            "SELECT typname FROM pg_type WHERE typcategory = 'E' ORDER BY typname"
        ))
        enums = result2.fetchall()
        print(f"Enums found: {[e[0] for e in enums]}")

        # Drop cascade all tables
        for t in tables:
            await session.execute(text(f"DROP TABLE IF EXISTS public.\"{t[0]}\" CASCADE"))
            print(f"  Dropped table: {t[0]}")

        # Drop all enums
        for e in enums:
            await session.execute(text(f"DROP TYPE IF EXISTS public.\"{e[0]}\" CASCADE"))
            print(f"  Dropped type: {e[0]}")

        await session.commit()
        print("Done.")

asyncio.run(reset())
