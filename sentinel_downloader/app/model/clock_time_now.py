from datetime import datetime

def get_time():
    """
    Returns the current time in the format YYYY-MM-DD HH:MM:SS.

    Args:
        None

    Returns:
        str: The current time in the format YYYY-MM-DD HH:MM:SS.

    Raises:
        None
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
