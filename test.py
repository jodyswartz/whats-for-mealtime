from main import app


def test_home_page_loads():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"What's for Mealtime?" in resp.data


def test_submit_works_without_db():
    client = app.test_client()
    resp = client.post(
        "/submit",
        data={
            "name": "Test",
            "date": "2026-02-21",
            "time": "18:30",
            "servings": "2",
            "dietary": "none",
            "cuisine": "tacos",
            "budget": "medium",
            "prep_time": "30",
            "pantry": "beans, tortillas",
            "avoid": "mushrooms",
            "notes": "quick",
        },
    )
    assert resp.status_code == 200
    assert b"Mealtime Receipt" in resp.data