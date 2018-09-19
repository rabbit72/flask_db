from flask import Flask, abort, render_template
from flask_restful import Resource, Api, reqparse

import db_functions as db

db.check_db()

app = Flask(__name__)
api = Api(app)

fish_parser = reqparse.RequestParser()
fish_parser.add_argument("name", type=str, required=True, help="Name for new fish")
fish_parser.add_argument("size", type=str, required=True, help="Fish size")


@api.resource("/api/fish/")
class ListFishes(Resource):
    def get(self):
        return db.fetch_fishes(), 200


@api.resource("/api/fish/add/")
class AddFish(Resource):
    def post(self):
        new_fish = fish_parser.parse_args()
        fish_name = new_fish["name"]
        fish_size = new_fish["size"]
        if not (fish_name and fish_size):
            return abort(400)
        fish_info = db.fetch_fish(fish_name)
        if fish_info:
            return fish_info, 302
        db.add_new_fish(new_fish["name"], new_fish["size"])
        fish_info = db.fetch_fish(fish_name)
        return fish_info, 201

    get = post


@api.resource("/api/fish/<string:fish_name>")
class Fish(Resource):
    def get(self, fish_name):
        fish_info = db.fetch_fish(fish_name)
        if not fish_info:
            return abort(404)
        return fish_info, 200

    def delete(self, fish_name):
        db.delete_fish(fish_name)
        fish_info = db.fetch_fish(fish_name)
        if not fish_info:
            return fish_info, 204
        else:
            return "Error db", 500


@app.route("/")
def main_page():
    return render_template("index.html", fishes=db.fetch_fishes())


# @app.route("/static/<path:path>")
# def static(path):
#     return send_from_directory("static", path)


if __name__ == "__main__":
    app.run()
