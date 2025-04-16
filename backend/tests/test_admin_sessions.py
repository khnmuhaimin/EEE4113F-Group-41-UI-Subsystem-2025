from dotenv import load_dotenv
load_dotenv()
import os
import re
from urllib.parse import urljoin
import requests

BASE_URL = f"http://0.0.0.0:{os.environ["PORT"]}"

def test_admin_login():
    admin_email = os.environ["ADMIN_EMAIL"]
    admin_password = os.environ["ADMIN_PASSWORD"]

    # testing the good path
    headers = {
    "Content-Type": "application/json"
    }
    body = {
        "email": admin_email,
        "password": admin_password
    }
    response = requests.request("POST", urljoin(BASE_URL, "/admins/login"), headers=headers, json=body)
    assert response.status_code == 204  # test http status code
    assert (set_cookie_header := response.headers.get("Set-Cookie")) is not None  # test that a Set-Cookie header is present
    assert re.match(r"session_id=[^;]+", set_cookie_header) is not None  # test that something was returned as the session id
    assert "HttpOnly" in set_cookie_header
    assert "Secure" in set_cookie_header

    # testing for missing credentials
    bodies = [
        {
        },
        {
            "email": admin_email
        },
        {
            "password": admin_password
        }
    ]
    for body in bodies:
        response = requests.request("POST", urljoin(BASE_URL, "/admins/login"), headers=headers, json=body)
        assert response.status_code == 400  # test http status code
        assert response.headers.get("Set-Cookie") is None  # test that a Set-Cookie header is not present
        assert response.json()["message"] == "Request body is missing login credentials."

    # testing for invalid credentials
        bodies = [
        {
            "email": admin_email,
            "password": "this is the wrong password"
        },
        {
            "email": "this is the wrong email",
            "password": admin_password
        },
        {
            "email": "this is the wrong email",
            "password": "and the password is wrong too"
        }
    ]
    for body in bodies:
        response = requests.request("POST", urljoin(BASE_URL, "/admins/login"), headers=headers, json=body)
        assert response.status_code == 401  # test http status code
        assert response.headers.get("Set-Cookie") is None  # test that a Set-Cookie header is not present
        assert response.json()["message"] == "Unauthorized."
        




