from flask.testing import FlaskClient


def get_cookie(client: FlaskClient, key: str) -> str | None:
    """
    Retrieve the value of a cookie by its key from the Flask test client.

    Args:
        client (FlaskClient): The Flask test client.
        key (str): The name of the cookie.

    Returns:
        str | None: The value of the cookie if it exists, otherwise None.
    """
    for cookie in client.cookie_jar:
        if cookie.name == key:
            return cookie.value
    return None