from datetime import datetime, timezone


def calculate_minutes_from_now(arrival_time: str) -> str:
    """
    Calculate the minutes from now to the given arrival time.

    Args:
        arrival_time (str): ISO 8601 formatted arrival time.

    Returns:
        str: The number of minutes from now or "Arriving" if less than 1 minute.
    """
    try:
        arrival = datetime.fromisoformat(arrival_time)
        now = datetime.now(timezone.utc)

        minutes_diff = int((arrival - now).total_seconds() // 60)

        if minutes_diff <= 0:
            return "Arriving"
        if minutes_diff == 1:
            return "1 min"
        return f"{minutes_diff} mins"
    except ValueError:
        return "Unknown"
