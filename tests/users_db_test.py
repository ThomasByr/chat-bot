from src.db import UsersDB


default_users = [
    {"username": "mario", "password": "mario1"},
    {"username": "peach", "password": "peach1"},
]

test_users = [
    {"username": "waluigi", "password": "waluigi1"},
    {"username": "wario", "password": "wario1"},
]

def test_read_db():
    db = UsersDB()
    for user in default_users:
        print(user)
        assert db.read_db(user["username"], user["password"])


def test_write_db():
    db = UsersDB()
    for user in test_users:
        db.write_db(user["username"], user["password"], test=True)
        assert db.read_db(user["username"], user["password"], test=True)
    db.reset_test_db()
