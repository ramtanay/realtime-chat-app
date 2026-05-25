import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("Connected to server")

    sio.emit('send_message', {
        'user_id': 1,
        'username': 'Ram',
        'message': 'Hello from client'
    })


@sio.on('receive_message')
def receive_message(data):
    print("Received:", data)


sio.connect('http://127.0.0.1:5000')

sio.wait()