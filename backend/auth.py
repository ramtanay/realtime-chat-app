from flask import Blueprint,request,jsonify
from flask_bcrypt import Bcrypt
import sqlite3
from utils.config import SECRET_KEY
import jwt
import datetime
from utils.config import DATABASE_NAME
from utils.jwt_helper import token_required


auth = Blueprint('auth',__name__)

bcrypt = Bcrypt()


@auth.route('/signup',methods=['POST'])
def signup():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'message': "Username and Password must be provided"
        }), 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO users(username,password) VALUES(?, ?)""",(username,hashed_password))
        return jsonify({
            "message": "User Created successfully"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            'message':'Username already exists'
        }), 400
    

@auth.route('/login',methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'message':'Username and Password must be provided.'
        }), 400

    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id,password FROM users WHERE username = ?",(username,))
        user = cursor.fetchone()
    if not user:
        return jsonify({
            'message' : f'No user found with username {username}'
        }), 404
    hashed_password = user[1]
    if bcrypt.check_password_hash(hashed_password,password):
        token = jwt.encode({
            "username":username,
            "id":user[0],
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
            },SECRET_KEY,algorithm='HS256')
        return jsonify({
            'message': 'Successfully logged in.',
            'token' : token
        }), 200
    return jsonify({
        "message":" Password doesn't match."
    }), 401
    



@auth.route('/verify', methods=['GET'])
@token_required
def verify_token(data):

    with sqlite3.connect(DATABASE_NAME) as conn:

        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT id
            FROM users
            WHERE id = ?
            ''',
            (data['id'],)
        )

        user = cursor.fetchone()

    if not user:

        return jsonify({

            'message': 'User no longer exists'

        }), 401

    return jsonify({

        'message': 'Token valid'

    }), 200


