from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store active users
active_users = set()

@app.route('/')
def index():
    return render_template('index.html')

# Handle new messages
@socketio.on('message')
def handle_message(data):
    print(f"Message received: {data}")
    send(data, broadcast=True)  # Broadcast the message to all users

# Handle user joining
@socketio.on('join')
def handle_join(username):
    active_users.add(username)
    emit('update_users', list(active_users), broadcast=True)

# Handle user disconnecting
@socketio.on('disconnect')
def handle_disconnect():
    print("A user has disconnected.")

if __name__ == '__main__':
    socketio.run(app, debug=True)
