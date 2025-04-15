from datetime import datetime, timezone


def utc_timestamp() -> int:
    """
    Returns the current UTC timestamp as an integer.

    Returns:
        int: The current UTC time in seconds since the Unix epoch.
    """
    return round(datetime.now(tz=timezone.utc).timestamp())