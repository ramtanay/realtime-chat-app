from flask_socketio import (
    emit,
    join_room,
    leave_room
)

import sqlite3

import jwt

from flask import request, session

from utils.config import (
    DATABASE_NAME,
    SECRET_KEY
)


online_users = {}

DEFAULT_ROOM = "General"


def register_socket_events(socketio):


    # =========================
    # CONNECT
    # =========================
    @socketio.on('connect')
    def handle_connect(auth):

        token = auth.get('token')

        if not token:

            print("No token provided")

            return False

        try:

            data = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=['HS256']
            )

            session['user'] = data

            print(f"{data['username']} connected")

        except jwt.InvalidTokenError:

            print("Invalid token")

            return False


    # =========================
    # DISCONNECT
    # =========================
    @socketio.on('disconnect')
    def handle_disconnect():

        socket_id = request.sid

        disconnected_user = None

        for username, sockets in online_users.items():

            if socket_id in sockets:

                sockets.remove(socket_id)

                # Remove user if no active tabs
                if len(sockets) == 0:

                    disconnected_user = username

                break

        if disconnected_user:

            del online_users[disconnected_user]

            print(f"{disconnected_user} disconnected")

        emit('online_users', {

            'users': list(online_users.keys())

        }, broadcast=True)


    # =========================
    # INITIAL JOIN
    # =========================
    @socketio.on('join')
    def handle_join():

        username = session['user']['username']

        socket_id = request.sid

        # Track online users
        if username not in online_users:

            online_users[username] = set()

        online_users[username].add(socket_id)

        # Join default room
        join_room(DEFAULT_ROOM)

        # Save current room
        session['current_room'] = DEFAULT_ROOM

        print(
            f"{username} joined room: "
            f"{DEFAULT_ROOM}"
        )

        print("Current online users:", online_users)

        emit('online_users', {

            'users': list(online_users.keys())

        }, broadcast=True)

        emit('room_joined', {

            'room': DEFAULT_ROOM

        })


    # =========================
    # ROOM SWITCHING
    # =========================
    @socketio.on('join_room')
    def handle_join_room(data):

        room = data.get('room')

        if not room:

            emit('error', {

                'message': 'Room name required'

            })

            return

        old_room = session.get(
            'current_room',
            DEFAULT_ROOM
        )

        # Leave old room
        leave_room(old_room)

        # Join new room
        join_room(room)

        # Save current room
        session['current_room'] = room

        print(
            f"{session['user']['username']} "
            f"switched from "
            f"{old_room} to {room}"
        )

        emit('room_joined', {

            'room': room

        })


    # =========================
    # SEND MESSAGE
    # =========================
    @socketio.on('send_message')
    def handle_send_message(data):

        message = data.get('message')

        if not message:

            emit('error', {

                'message': 'Invalid message'

            })

            return

        user = session.get('user')

        user_id = user['id']

        username = user['username']

        room = data.get(
            'room',
            DEFAULT_ROOM
        )

        with sqlite3.connect(DATABASE_NAME) as conn:

            cursor = conn.cursor()

            cursor.execute(
                '''
                INSERT INTO messages
                (user_id, username, message, room)
                VALUES (?, ?, ?, ?)
                ''',
                (
                    user_id,
                    username,
                    message,
                    room
                )
            )

            cursor.execute(
                '''
                SELECT timestamp
                FROM messages
                WHERE id = ?
                ''',
                (cursor.lastrowid,)
            )

            timestamp = cursor.fetchone()[0]

        emit('receive_message', {

            'user_id': user_id,

            'username': username,

            'message': message,

            'timestamp': str(timestamp),

            'room': room

        }, to=room)


    # =========================
    # TYPING INDICATOR
    # =========================
    @socketio.on('typing')
    def handle_typing(data):

        room = data.get(
            'room',
            DEFAULT_ROOM
        )

        username = session['user']['username']

        emit('user_typing', {

            'username': username,

            'room': room

        }, to=room, include_self=False)