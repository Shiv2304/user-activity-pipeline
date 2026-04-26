import os
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine


def build_database_url() -> str:
    """Build a PostgreSQL SQLAlchemy URL from environment variables."""
    # Prefer a fully-specified connection string when provided.
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    required_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise RuntimeError(
            "Missing environment variables for PostgreSQL connection: "
            + ", ".join(missing)
        )

    user = os.environ["DB_USER"]
    password = quote_plus(os.environ["DB_PASSWORD"])
    host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]
    db_name = os.environ["DB_NAME"]

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"


def main() -> None:
    csv_path = "data/raw/events.csv"
    table_name = "events_raw"

    df = pd.read_csv(csv_path)

    engine = create_engine(build_database_url())
    with engine.begin() as connection:
        df.to_sql(table_name, connection, if_exists="append", index=False)

    print(f"Loaded {len(df)} rows from {csv_path} into {table_name}.")


if __name__ == "__main__":
    main()
