from datetime import datetime, timezone


def utc_timestamp(offset: int = 0) -> int:
    """
    Returns the current UTC timestamp as an integer, adjusted by an optional offset.

    Args:
        offset (int, optional): The number of seconds to adjust the UTC timestamp. Default is 0.

    Returns:
        int: The current UTC time in seconds since the Unix epoch, adjusted by the provided offset.
    """
    return round(datetime.now(tz=timezone.utc).timestamp()) + offset