from pyexpat.errors import messages
from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from utils.jwt_helper import token_required
from database import create_tables
from auth import auth 
from utils.socket_events import register_socket_events
from messages import messages

# Creat Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(messages, url_prefix='/api')




# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins='*')
register_socket_events(socketio)

@app.route('/',methods=['GET'])
def home():
    return jsonify({
        "message" : 'Chat server Running...'
    })

@app.route('/protected',methods=['GET'])
@token_required
def protected(data):
    return jsonify({
        "message":"This is a protected route",
        "username": data['username'],
        'user_id': data['user_id']
    })
create_tables()

if __name__ == '__main__':
    socketio.run(app,debug=True)





