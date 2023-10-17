import os
import hashlib

import yaml as yml


__all__ = ["UsersDB"]


class UsersDB:
    CACHE_FOLDER = "cache"

    def __init__(self):
        ...

    def read_db(self, user_name: str, password: str, test: bool = False) -> bool:
        users: dict[str, str] = {}
        filename = "test_users.yml" if test else "users.yml"
        with open(os.path.join(self.CACHE_FOLDER, "default_users.yml"), "r") as f:
            for user in yml.safe_load(f)["users"]:
                users[user["username"]] = user["password"]
        try:
            with open(os.path.join(self.CACHE_FOLDER, filename), "r") as f:
                for user in yml.safe_load(f)["users"]:
                    users[user["username"]] = user["password"]
        except FileNotFoundError:
            pass
        except TypeError:
            pass

        if user_name in users:
            if users[user_name] == hashlib.md5(password.encode()).hexdigest():
                return True
        return False

    def write_db(self, user_name: str, password: str, test: bool = False):
        password = hashlib.md5(password.encode()).hexdigest()
        filename = "test_users.yml" if test else "users.yml"
        if not os.path.exists(self.CACHE_FOLDER):
            os.makedirs(self.CACHE_FOLDER)
        users = []
        try:
            with open(os.path.join(self.CACHE_FOLDER, filename), "r") as f:
                users = yml.safe_load(f)["users"]
        except FileNotFoundError:
            pass
        except TypeError:
            pass
        users.append({"username": user_name, "password": password})
        with open(os.path.join(self.CACHE_FOLDER, filename), "w") as f:
            yml.dump({"users": users}, f)

    def reset_test_db(self):
        if os.path.exists(self.CACHE_FOLDER):
            os.remove(os.path.join(self.CACHE_FOLDER, "test_users.yml"))
