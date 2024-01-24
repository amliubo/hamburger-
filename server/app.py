import secrets
from bson import ObjectId
from config import Config
from datetime import timedelta
from flask_cors import CORS
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token
from pymongo import MongoClient, UpdateOne

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
jwt = JWTManager(app)

# 配置
app.config.from_object(Config)

# MongoDB 配置
client = MongoClient(app.config['MONGODB_URI'], connect=False)
mongo_db = client.get_database()

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
                                  'time': str(activity['time']),'like':activity['like'],'dislike':activity['dislike'],'comment':activity['comment']} for activity in activities]
        return jsonify(serialized_activities)
    elif request.method == 'POST':
        data = request.json
        if 'activity_id' in data:
            activity_id = data.pop('activity_id')
            mongo_db.activities.update_one({'_id': ObjectId(activity_id)}, {'$push': {'comment': data}})
            return jsonify({'message': 'secuess'})
        else:
            mongo_db.activities.insert_one(data)
            return jsonify({'message': 'secuess'})
    
@app.route('/like', methods=['POST'])
def like():
    data = request.get_json()
    _id = ObjectId(data.get('_id'))
    comment_id = data.get('comment_id')
    if comment_id is not None:
        query = {'_id': _id, 'comment.comment_id': comment_id}
        update = UpdateOne(query, {'$inc': {'comment.$.like': 1}})
    else:
        query = {'_id': _id}
        update = UpdateOne(query, {'$inc': {'like': 1}})
    mongo_db.activities.bulk_write([update])
    return jsonify({'message': 'success'})


@app.route('/dislike', methods=['POST'])
def dislike():
    data = request.get_json()
    _id = ObjectId(data.get('_id'))
    comment_id = data.get('comment_id')
    if comment_id is not None:
        query = {'_id': _id, 'comment.comment_id': comment_id}
        update = UpdateOne(query, {'$inc': {'comment.$.dislike': 1}})
    else:
        query = {'_id': _id}
        update = UpdateOne(query, {'$inc': {'dislike': 1}})
    mongo_db.activities.bulk_write([update])
    return jsonify({'message': 'success'})