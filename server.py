from flask import Flask, render_template
from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return "TCP Group Chat Server is running!"

@socketio.on('message')
def handle_message(msg):
    print("Message received: " + msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 if PORT is not set
    socketio.run(app, host="0.0.0.0", port=port)
