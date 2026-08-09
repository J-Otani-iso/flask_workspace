from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
from pymongo import MongoClient
import base64
import gridfs
import bson

app = Flask(__name__)

# Socket.ioのセットアップ
socketio = SocketIO(app)

# MongoDBの接続先設定
mongo_uri = "mongodb+srv://otanijunya_db_user:jQk9KM57dyoAmMh6@cluster0.jgo9x46.mongodb.net/?appName=Cluster0"
client = MongoClient(mongo_uri)
db = client["SNS"]

# GridFSのセットアップ - (*1)
fs = gridfs.GridFS(db)

@app.route("/")
def index():
    return render_template("index.html")

# メッセージの読み込み
@socketio.on('load messages')
def load_messages():
    messages = db.images.find().sort('_id', -1).limit(3)
    messages = list(messages)[::-1]
    # メッセージと画像データをリストにして返す - (*2)
    messages_return = [{'message':message['message'],
                        'image_data':get_image_data(message['image_id'])}
                        for message in messages]
    
    emit('load all messages', messages_return)

# 画像IDから画像データを取得 - (*3)
def get_image_data(image_id):
    image_file = fs.get(image_id).read()
    image_base64 = base64.b64encode(image_file)
    return image_base64.decode('utf-8')

# メッセージと画像と画像の登録 - (*4)
@socketio.on('send message')
def send_message(data):
    message = data['message']
    image_data = data['image_data']
    image_name = data['image_name']

    # base64エンコードされている画像データをでコードしてGridFSに保存 - (*5)
    image_bytes = base64.b64decode(image_data.split(',')[1])
    image_id = fs.put(image_bytes, image_name = image_name)

    # MongoDBに画像を保存したGridFSのファイルIDとテキストを保存 - (*6)
    image_recode = {
        'image_name': image_name,
        'image_id': image_id,
        'message': message
    }
    db.images.insert_one(image_recode)

    # メッセージと画像をクライアントへ送信 - (*7)
    emit('load one message', {"message":message, "image_data":get_image_data(image_id)}, broadcast=True)

if __name__ == "__main__":
    # Socketioサーバの起動
    socketio.run(app, debug=True)