import pytest
from fastapi.testclient import TestClient
from db import SessionLocal, Base, engine, ChatData
from main import app

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    test_entries = [
        ("How to change password", "Complete detail to change password.. Steps are here 1...  2...."),
        ("How to logout", "Complete detail to logout.. Steps are here 1...  2...."),
        ("How to delete data", "Complete detail to delete data.. Steps are here 1...  2...."),
        ("reset password", "Follow these steps to reset your password: 1) ... 2) ..."),
    ]

    problems = [t[0] for t in test_entries]
    # Remove any existing test rows to avoid duplicates
    try:
        db.query(ChatData).filter(ChatData.problem.in_(problems)).delete(synchronize_session=False)
        for p, s in test_entries:
            db.add(ChatData(problem=p, solution=s))
        db.commit()
    finally:
        db.close()

    yield

    # Cleanup after tests
    db = SessionLocal()
    try:
        db.query(ChatData).filter(ChatData.problem.in_(problems)).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()


def test_known_question_change_password():
    resp = client.get("/chatbot/", params={"query": "How to change password"})
    assert resp.status_code == 200
    data = resp.json()
    assert "Complete detail to change password" in data["solution"]


def test_known_question_logout():
    resp = client.get("/chatbot/", params={"query": "How to logout"})
    assert resp.status_code == 200
    data = resp.json()
    assert "Complete detail to logout" in data["solution"]


def test_reset_password():
    resp = client.get("/chatbot/", params={"query": "reset password"})
    assert resp.status_code == 200
    data = resp.json()
    assert "reset your password" in data["solution"] or data["solution"].startswith("Follow these steps")


def test_unknown_question():
    resp = client.get("/chatbot/", params={"query": "some unknown question"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["solution"].lower().startswith("sorry")
