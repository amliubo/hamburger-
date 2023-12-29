import secrets
from datetime import timedelta
from dataclasses import dataclass
from flask_cors import CORS
from pymongo import MongoClient
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
jwt = JWTManager(app)

# 配置
class Config:
    MONGODB_URI = "mongodb://root:123456@127.0.0.1:27017/treehole?authSource=admin&retryWrites=true&w=majority"
    DEBUG = True

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
        activities = mongo_db.activities.find({}, {'_id': False}).sort('time', -1)
        return jsonify(list(activities))
    elif request.method == 'POST':
        data = request.json
        mongo_db.activities.insert_one(data)
        return jsonify({'message': 'Activity created successfully'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
