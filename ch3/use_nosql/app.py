from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

# Socket.ioのセットアップ - (*1)
socketio = SocketIO(app)

# MongoDBの接続先設定 - (*2)
mongo_uri = "mongodb+srv://otanijunya_db_user:jQk9KM57dyoAmMh6@cluster0.jgo9x46.mongodb.net/?appName=Cluster0"
client = MongoClient(mongo_uri)
db = client["SNS"]
messages_collection = db["messages"]

@app.route("/")
def index():
    return render_template("index.html")

# メッセージの読み込み - (*3)
@socketio.on('load messages')
def load_messages():
    message_documents = messages_collection.find().sort('_id', -1).limit(10)
    message_documents = list(message_documents)[::-1]
    messages_texts = [document['message'] for document in message_documents]
    # メッセージをクライアントへ送信 - (*4)
    emit('load all messages', messages_texts)

# メッセージの登録 - (*5)
@socketio.on('send message')
def send_message(message_text):
    messages_collection.insert_one({'message': message_text})
    # メッセージをクライアントへ送信 - (*6)
    emit('load one message', message_text, broadcast=True)


if __name__ == "__main__":
    # Socketioサーバの起動 - (*7)
    socketio.run(app, debug=True)