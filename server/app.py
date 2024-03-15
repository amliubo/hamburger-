from bson import ObjectId
from config import Config
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from pymongo import MongoClient, UpdateOne

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)
jwt = JWTManager(app)

# MongoDB Configuration
client = MongoClient(app.config["MONGODB_URI"], connect=False)
mongo_db = client.get_database()


# Routes
@app.route("/posts", methods=["GET", "POST"])
def handle_posts():
    if request.method == "GET":
        return get_posts()
    elif request.method == "POST":
        return create_post()


@app.route("/like", methods=["POST"])
def handle_like():
    data = request.get_json()
    return like_post(data)


@app.route("/dislike", methods=["POST"])
def handle_dislike():
    data = request.get_json()
    return dislike_post(data)


@app.route("/activities", methods=["POST"])
def create_activity():
    data = request.json
    mongo_db.activities.insert_one(data)
    return jsonify({"message": "Activity created successfully"}), 201


@app.route("/activities", methods=["GET"])
def read_activities():
    activities = mongo_db.activities.find({}, {"_id": False})
    return jsonify(list(activities))


def get_posts():
    posts = mongo_db.posts.find({}).sort("time", -1)
    serialized_posts = []
    for post in posts:
        serialized_post = {
            "_id": str(post["_id"]),
            "author": str(post["author"]),
            "description": str(post["description"]),
            "time": str(post["time"]),
            "like": post["like"],
            "dislike": post["dislike"],
            "city": str(post["city"]),
        }
        serialized_posts.append(serialized_post)
    return jsonify(serialized_posts)


def create_post():
    data = request.json
    mongo_db.posts.insert_one(data)
    return jsonify({"message": "success"})


def like_post(data):
    _id = ObjectId(data.get("_id"))
    query = {"_id": _id}
    update = UpdateOne(query, {"$inc": {"like": 1}})
    mongo_db.posts.bulk_write([update])
    return jsonify({"message": "success"})


def dislike_post(data):
    _id = ObjectId(data.get("_id"))
    query = {"_id": _id}
    update = UpdateOne(query, {"$inc": {"dislike": 1}})
    mongo_db.posts.bulk_write([update])
    return jsonify({"message": "success"})


if __name__ == "__main__":
    app.run(host="10.10.20.24", port=8000, debug=True)
