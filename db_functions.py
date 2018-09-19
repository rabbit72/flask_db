import os
import sqlite3


DB_PATH = os.path.abspath("./sqlite.db")


def check_db():
    if not os.path.isfile(DB_PATH):
        create_db()


def create_db():
    create_fish = """CREATE TABLE fish
    (id INTEGER PRIMARY KEY AUTOINCREMENT, name text UNIQUE, size text);"""
    _send_request_db(create_fish)


def add_new_fish(name: str, size: str):
    add_fish = """INSERT INTO fish (name, size) VALUES (?, ?);"""
    try:
        _send_request_db(add_fish, (name, size))
    except sqlite3.IntegrityError:
        pass


def delete_fish(name: str):
    delete = "DELETE FROM fish WHERE name=?;"
    _send_request_db(delete, (name,))


def fetch_fish(name):
    select_fish = "SELECT id, name, size FROM fish WHERE name=?;"
    fish = _send_request_db(select_fish, (name,))
    try:
        fish_id, fish_name, fish_size = fish[0]
        return dict(id=fish_id, name=fish_name, size=fish_size)
    except (ValueError, IndexError):
        return dict()


def fetch_fishes():
    select_fish = "SELECT id, name, size FROM fish;"
    fishes = _send_request_db(select_fish)
    return [dict(id=_id, name=name, size=size) for _id, name, size in fishes]


def _send_request_db(sql_request, variables=tuple()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_request, variables)
        conn.commit()
    return cursor.fetchall()