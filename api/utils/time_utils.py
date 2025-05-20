from datetime import datetime, timedelta

def get_minutes_from_week_start(timestamp: datetime) -> float:
    """
    Convert a timestamp to minutes from the start of the week (Monday 12 AM)
    """
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    
    week_start = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = week_start - timedelta(days=timestamp.weekday())
    minutes_diff = (timestamp - week_start).total_seconds() / 60
    return minutes_diff 