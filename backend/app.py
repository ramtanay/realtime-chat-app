from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO

import os

from utils.jwt_helper import token_required
from utils.config import DATABASE_NAME, DB_PASSWORD

from database import create_tables

from auth import auth

from messages import messages

from utils.socket_events import register_socket_events


# =========================
# CREATE APP
# =========================
app = Flask(__name__)

CORS(app, supports_credentials=True)

app.register_blueprint(
    auth,
    url_prefix='/auth'
)

app.register_blueprint(
    messages,
    url_prefix='/api'
)


# =========================
# SOCKET.IO
# =========================
socketio = SocketIO(

    app,

    cors_allowed_origins='*'
)

register_socket_events(socketio)


# =========================
# HOME ROUTE
# =========================
@app.route('/', methods=['GET'])
def home():

    return jsonify({

        "message": "Chat server running..."
    })


# =========================
# PROTECTED ROUTE
# =========================
@app.route('/protected', methods=['GET'])
@token_required
def protected(data):

    return jsonify({

        "message": "This is a protected route",

        "username": data['username'],

        "user_id": data['id']
    })


# =========================
# RESET DATABASE (FOR TESTING PURPOSES ONLY)
# =========================
@app.route(
    "/reset-db",
    methods=["POST"]
)
def reset_db():

    data = request.get_json()

    password = data.get("password")

    if (
        os.path.exists(DATABASE_NAME)
        and password == DB_PASSWORD
    ):

        os.remove(DATABASE_NAME)

        create_tables()

        return {

            "message":
            "Database reset successful"
        }

    return {

        "message":
        "Invalid password or database does not exist"

    }, 400


@app.route('/health')
def health():
    return jsonify({
        "status": "healthy"})


# =========================
# CREATE TABLES
# =========================
create_tables()


# =========================
# RUN APP
# =========================
if __name__ == "__main__":

    port = int(

        os.environ.get("PORT", 5000)
    )

    socketio.run(

        app,

        host="0.0.0.0",

        port=port
    )