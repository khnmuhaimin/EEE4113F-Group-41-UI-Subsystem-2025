from datetime import datetime, timezone
import ipaddress


def utc_timestamp(offset: int = 0) -> int:
    """
    Returns the current UTC timestamp as an integer, adjusted by an optional offset.

    Args:
        offset (int, optional): The number of seconds to adjust the UTC timestamp. Default is 0.

    Returns:
        int: The current UTC time in seconds since the Unix epoch, adjusted by the provided offset.
    """
    return round(datetime.now(tz=timezone.utc).timestamp()) + offset


def is_ip_address(ip_string: str) -> bool:
    """
    Check if the provided string is a valid IP address.

    Args:
        ip_string (str): The string to validate.

    Returns:
        bool: True if the string is a valid IPv4 or IPv6 address, False otherwise.
    """
    try:
        ipaddress.ip_address(ip_string)
        return True
    except:
        return False
    
