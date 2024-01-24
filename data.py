import json


def open_data(filename) -> dict:
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return dict()


def save_data(users_data: dict):
    with open('users_data.json', "w") as f:
        json.dump(users_data, f)
