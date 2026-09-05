import os

from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

# Flaskアプリの初期化
app: Flask = Flask(__name__)

# データベース接続先を取得
# RenderではDATABASE_URLを使用し、
# ローカルではSQLiteを使用する
database_url = os.environ.get("DATABASE_URL", "sqlite:///memo.sqlite")

# RenderのPostgreSQL URLをpsycopg用に変換
if database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

db: SQLAlchemy = SQLAlchemy(app)


# メモのデータベースモデルを定義
class MemoItem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.Text, nullable=False)
    body: str = db.Column(db.Text, nullable=False)


# データベースの初期化
with app.app_context():
    db.create_all()


# メモ一覧を表示する
@app.route("/")
def index():
    items = MemoItem.query.order_by(MemoItem.title).all()

    items.insert(
        0,
        {
            "id": 0,
            "title": "🖌新規作成",
            "body": ""
        }
    )

    return render_template("list.html", items=items)


# メモの編集画面を出す
@app.route("/memo/<int:id>", methods=["GET", "POST"])
def memo(id: int):

    # メモを取得
    it = db.session.get(MemoItem, id)

    if id == 0 or it is None:
        # 新規メモ
        it = MemoItem(
            title="__無題__",
            body=""
        )

    # POSTの場合はデータを保存
    if request.method == "POST":

        it.title = request.form.get(
            "title",
            "__無題__"
        )

        it.body = request.form.get(
            "body",
            ""
        )

        if it.title == "":
            return "タイトルは空にできません"

        if id == 0:
            db.session.add(it)

        db.session.commit()

        return redirect(
            url_for("index")
        )

    # メモの編集画面を表示
    return render_template(
        "memo.html",
        it=it
    )


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8888
    )