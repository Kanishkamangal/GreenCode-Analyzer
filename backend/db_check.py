from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Database:", conn.execute(text("SELECT current_database()")).scalar())
    print("User:", conn.execute(text("SELECT current_user")).scalar())

    tables = conn.execute(
        text("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name
        """)
    )

    print("\nTables:")
    for row in tables:
        print(f"  {row[0]}.{row[1]}")

    print("\nRow counts:")
    for table in [
        "analysis",
        "benchmark",
        "feedback",
        "otp",
        "programming_language",
        "report",
        "users",
    ]:
        count = conn.execute(
            text(f'SELECT COUNT(*) FROM "{table}"')
        ).scalar()
        print(f"  {table}: {count}")

    print("\nAnalysis table columns:")

    columns = conn.execute(
        text("""
            SELECT
                column_name,
                data_type,
                is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'analysis'
            ORDER BY ordinal_position
        """)
    )

    for row in columns:
        print(
            f"  {row[0]} | "
            f"type={row[1]} | "
            f"nullable={row[2]}"
        )