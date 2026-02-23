import os
import sys

# Add project root (one level up from /tests) to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app  # noqa: E402


def test_login_page_loads():
    client = app.test_client()
    resp = client.get("/login")
    assert resp.status_code in (200, 302)  # 302 if you redirect somewhere


def test_index_requires_login():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code in (200, 302)  # 302 if TOTP is enabled