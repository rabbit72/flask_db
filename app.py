import os.path
import sqlite3

from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

DB_PATH = os.path.abspath("./sqlite.db")


@app.route("/")
def post(name):
    fish = fetch_fish(name)
    if not fish:
        fish = {"error": "Fish not found"}
    return jsonify(fish)


@app.route("/api/fish/<name>")
def fish_api_fetch(name):
    fish = fetch_fish(name)
    if not fish:
        fish = {"error": "Fish not found"}
    return jsonify(fish)


@app.route("/api/fish/", methods=["GET", "POST"])
def fish_api():
    if request.method == "GET":
        return jsonify(fetch_fishes())

    elif request.method == "POST":
        name = request.form["name"]
        size = request.form["size"]
        try:
            add_new_fish(name, size)
        except sqlite3.IntegrityError:
            pass
        fish = fetch_fish(name)
        if fish:
            return jsonify(fish)
        else:
            return jsonify(error="Параметры: name, size")


def create_db():
    create_fish = """CREATE TABLE fish
    (id INTEGER PRIMARY KEY AUTOINCREMENT, name text UNIQUE, size text);"""
    _send_request_db(create_fish)


def add_new_fish(name: str, size: str):
    add_fish = """INSERT INTO fish (name, size) VALUES (?, ?);"""
    _send_request_db(add_fish, (name, size))


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


def main():
    if not os.path.isfile(DB_PATH):
        create_db()
    app.run()


if __name__ == "__main__":
    main()
