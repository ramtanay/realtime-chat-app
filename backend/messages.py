from flask import (
    Blueprint,
    jsonify,
    request
)

import sqlite3

from utils.config import DATABASE_NAME

from utils.jwt_helper import token_required


messages = Blueprint(
    'messages',
    __name__
)


@messages.route(
    '/messages',
    methods=['GET']
)
@token_required
def get_messages(data):

    room = request.args.get(
        'room',
        'General'
    )

    with sqlite3.connect(DATABASE_NAME) as conn:

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                username,
                room,
                message,
                timestamp

            FROM messages

            WHERE room = ?

            ORDER BY timestamp ASC
            """,
            (room,)
        )

        rows = cursor.fetchall()

    all_messages = []

    for row in rows:

        all_messages.append({

            'username': row['username'],

            'room': row['room'],

            'message': row['message'],

            'timestamp': row['timestamp']
        })

    return jsonify(all_messages), 200