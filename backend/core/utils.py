from datetime import datetime, timezone


def dt_utcnow() -> datetime:
    return datetime.now(timezone.utc)
