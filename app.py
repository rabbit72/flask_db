import os.path
import sqlite3
import click

from flask import Flask
from flask import request, jsonify


def main(DB_PATH):
    def create_db(db_path):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """CREATE TABLE fish
                (id INTEGER PRIMARY KEY AUTOINCREMENT, name text UNIQUE, size text);"""
            )
            conn.commit()
        conn.close()

    def insert_new_fish(db_path, name: str, size: str):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO fish (name, size)
                VALUES (?, ?);""",
                (name, size),
            )
            conn.commit()
        return

    def fetch_fish(db_path, name):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, size FROM fish WHERE name=?;", (name,))
            try:
                fish_id, fish_name, fish_size = cursor.fetchall()[0]
                return dict(id=fish_id, name=fish_name, size=fish_size)
            except (ValueError, IndexError):
                return dict()

    def fetch_fishes(db_path):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, size FROM fish;")
            fishes = cursor.fetchall()
        return [dict(id=_id, name=name, size=size) for _id, name, size in fishes]

    app = Flask(__name__)

    @app.route("/api/fish/<name>")
    def fish_api_fetch(name):
        fish = fetch_fish(DB_PATH, name)
        if not fish:
            fish = {"error": "Fish not found"}
        return jsonify(fish)

    @app.route("/api/fish/", methods=["GET", "POST"])
    def fish_api():
        if request.method == "GET":
            return jsonify(fetch_fishes(DB_PATH))

        elif request.method == "POST":
            name = request.form["name"]
            size = request.form["size"]
            try:
                insert_new_fish(DB_PATH, name, size)
            except sqlite3.IntegrityError:
                pass
            fish = fetch_fish(DB_PATH, name)
            if fish:
                return jsonify(fish)
            else:
                return jsonify(error="Параметры: name, size")

    DB_PATH = os.path.abspath(DB_PATH)
    if not os.path.isfile(DB_PATH):
        create_db(DB_PATH)
    app.run()


@click.command()
@click.option("--db_name", "-n", default="sqlite")
def enter_point(db_name):
    DB_PATH = os.path.join("./", db_name + ".db")
    main(DB_PATH)


if __name__ == "__main__":
    enter_point()
