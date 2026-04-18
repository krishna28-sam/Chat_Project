from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from pymongo import MongoClient
from datetime import datetime
import bcrypt
import os
from dotenv import load_dotenv
import logging

logging.getLogger('werkzeug').setLevel(logging.ERROR)
logging.getLogger('socketio').setLevel(logging.ERROR)

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET', 'secret_key')

CORS(app)
JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=False, engineio_logger=False)

mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/chat_app')
db = MongoClient(mongo_uri)['chat_app']
users = db['users']
messages = db['messages']


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'message': 'Server is running'}), 200


@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'message': 'All fields required'}), 400
    
    existing_user = users.find_one({'$or': [{'username': username}, {'email': email}]})
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
    
    result = users.insert_one({
        'username': username,
        'email': email,
        'password': hashed
    })
    
    user_id = str(result.inserted_id)
    token = create_access_token(identity=user_id)
    
    return jsonify({
        'token': token,
        'user': {'id': user_id, 'username': username, 'email': email}
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400
    
    user = users.find_one({'username': username})
    
    if not user:
        return jsonify({'message': 'User not found'}), 401
    
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'message': 'Wrong password'}), 401
    
    user_id = str(user['_id'])
    token = create_access_token(identity=user_id)
    
    return jsonify({
        'token': token,
        'user': {'id': user_id, 'username': user['username'], 'email': user['email']}
    }), 200


@socketio.on('join_room')
def on_join_room(data):
    room = data['room']
    username = data['username']
    join_room(room)
    
    emit('user_joined', {
        'message': username + ' joined'
    }, to=room)


@socketio.on('send_message')
def on_send_message(data):
    room = data['room']
    message = data['message']
    username = data['username']
    user_id = data['userId']
    
    messages.insert_one({
        'user_id': user_id,
        'username': username,
        'room': room,
        'message': message,
        'time': datetime.utcnow()
    })
    
    emit('receive_message', {
        'username': username,
        'message': message
    }, to=room)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print('Server running on port ' + str(port))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
