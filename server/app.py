import secrets
from bson import ObjectId
from config import Config
from datetime import timedelta
from dataclasses import dataclass
from flask_cors import CORS
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token
from pymongo import MongoClient


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
jwt = JWTManager(app)

# 配置
app.config.from_object(Config)

# MongoDB 配置
client = MongoClient(app.config['MONGODB_URI'], connect=False)
mongo_db = client.get_database()

# 模型
@dataclass
class User:
    username: str
    password: str

@dataclass
class Action:
    author: str
    email: str
    description: str
    time: str
    like: int
    dislike: int

# 路由
@app.route('/token', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = mongo_db.user.find_one({'username': username})
    if user and password == user.get('password', ''):
        access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=30))
        return jsonify({'user': username, 'access_token': access_token })
    return make_response(jsonify({'error': 'Invalid username or password'}), 401)

@app.route('/post', methods=['GET', 'POST'])
def activities():
    if request.method == 'GET':
        activities = mongo_db.activities.find({}).sort('time', -1)
        serialized_activities = [{'_id': str(activity['_id']), 'author': str(activity['author']),'email': str(activity['email']),'description': str(activity['description']),
                                  'time': str(activity['time']),'like':activity['like'],'dislike':activity['dislike']} for activity in activities]
        return jsonify(serialized_activities)
    elif request.method == 'POST':
        data = request.json
        mongo_db.activities.insert_one(data)
        return jsonify({'message': 'Activity created successfully'}), 201
    
@app.route('/like', methods=['POST'])
def like():
    _id = request.get_json().get('_id')
    mongo_db.activities.update_one({'_id': ObjectId(_id)}, {'$inc': {'like': 1}})
    return jsonify({'message': 'Like successful'})


@app.route('/dislike', methods=['POST'])
def dislike():
    _id = request.get_json().get('_id')
    mongo_db.activities.update_one({'_id': ObjectId(_id)}, {'$inc': {'dislike': 1}})
    return jsonify({'message': 'Dislike successful'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
