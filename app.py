import db_functions as db

from flask import Flask, abort, render_template, send_from_directory
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)

fish_parser = reqparse.RequestParser()
fish_parser.add_argument("name", type=str, required=True, help="Name for new fish")
fish_parser.add_argument("size", type=str, required=True, help="Fish size")


class ListFishes(Resource):
    def get(self):
        return db.fetch_fishes(), 200

    def post(self):
        new_fish = fish_parser.parse_args()
        fish_name = new_fish["name"]
        fish_size = new_fish["size"]
        if not (fish_name and fish_size):
            return abort(400)
        db.add_new_fish(new_fish["name"], new_fish["size"])
        fish_info = db.fetch_fish(fish_name)
        if fish_info:
            return fish_info, 201
        else:
            return "Error db", 500


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


api.add_resource(ListFishes, "/api/fish/")
api.add_resource(Fish, "/api/fish/<string:fish_name>")

# @app.route("/")
# def post(name):
#     fish = fetch_fish(name)
#     if not fish:
#         fish = {"error": "Fish not found"}
#     return jsonify(fish)


def main():
    db.check_db()
    app.run()


if __name__ == "__main__":
    main()
