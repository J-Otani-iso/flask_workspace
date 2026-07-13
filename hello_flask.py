# Flaskのインポート
from flask import Flask

# インスタンス作成
app: Flask = Flask(__name__)

# ルーティング
@app.route("/")
def hello_world():
    return "<h1>あなたの年齢は" + age + "歳です。</h1>"

# アプリの実行
if __name__ == "__main__":
    app.run(debug=True)