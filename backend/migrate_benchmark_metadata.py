from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")


engine = create_engine(DATABASE_URL)


def migrate():
    with engine.begin() as conn:
        print("Checking analysis table...")

        column_exists = conn.execute(
            text("""
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name = 'analysis'
                      AND column_name = 'benchmark_metadata'
                )
            """)
        ).scalar()

        if column_exists:
            print("benchmark_metadata column already exists.")
            print("No migration required.")
            return

        print("Adding benchmark_metadata column...")

        conn.execute(
            text("""
                ALTER TABLE public.analysis
                ADD COLUMN benchmark_metadata JSON NULL
            """)
        )

        print("Migration completed successfully.")
        print("Added: analysis.benchmark_metadata JSON NULL")


if __name__ == "__main__":
    migrate()