import os
import sys

# Add project root (one level up from /tests) to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app  # noqa: E402


def test_login_page_loads():
    client = app.test_client()
    resp = client.get("/login")
    assert resp.status_code == 200


def test_index_redirects_to_login_when_not_authed():
    client = app.test_client()
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/login" in resp.headers.get("Location", "")