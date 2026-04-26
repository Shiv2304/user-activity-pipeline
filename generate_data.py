#!/usr/bin/env python3
"""Generate simulated user activity event data as a CSV file."""

from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

EVENT_TYPES = ("signup", "login", "purchase")
FEATURES = (
    "homepage",
    "search",
    "checkout",
    "recommendations",
    "profile",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate simulated user activity events and save them to CSV."
    )
    parser.add_argument(
        "--num-events",
        type=int,
        default=1000,
        help="Number of events to generate (default: 1000).",
    )
    parser.add_argument(
        "--num-users",
        type=int,
        default=100,
        help="Number of unique users to simulate (default: 100).",
    )
    parser.add_argument(
        "--days-back",
        type=int,
        default=30,
        help="Generate timestamps over the past N days (default: 30).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/raw/user_activity.csv"),
        help="Output CSV path (default: data/raw/user_activity.csv).",
    )
    return parser.parse_args()


def random_timestamp(now: datetime, days_back: int) -> str:
    start = now - timedelta(days=days_back)
    delta_seconds = int((now - start).total_seconds())
    random_offset = random.randint(0, delta_seconds)
    ts = start + timedelta(seconds=random_offset)
    return ts.isoformat()


def generate_rows(num_events: int, num_users: int, days_back: int) -> list[dict[str, str]]:
    now = datetime.now(timezone.utc)
    rows: list[dict[str, str]] = []

    for _ in range(num_events):
        user_id = f"user_{random.randint(1, num_users):04d}"
        event_type = random.choices(
            EVENT_TYPES,
            weights=(0.15, 0.65, 0.2),
            k=1,
        )[0]

        rows.append(
            {
                "user_id": user_id,
                "event_type": event_type,
                "timestamp": random_timestamp(now, days_back),
                "feature": random.choice(FEATURES),
            }
        )

    rows.sort(key=lambda row: row["timestamp"])
    return rows


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["user_id", "event_type", "timestamp", "feature"]
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()

    if args.num_events <= 0:
        raise ValueError("--num-events must be a positive integer")
    if args.num_users <= 0:
        raise ValueError("--num-users must be a positive integer")
    if args.days_back <= 0:
        raise ValueError("--days-back must be a positive integer")

    rows = generate_rows(args.num_events, args.num_users, args.days_back)
    write_csv(rows, args.output)
    print(f"Generated {len(rows)} events at {args.output}")


if __name__ == "__main__":
    main()
