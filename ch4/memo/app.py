import os

from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy


# Flaskアプリの初期化
app: Flask = Flask(__name__)

# RenderではPostgreSQL、ローカルではSQLiteを使用
database_url = os.environ.get("DATABASE_URL", "sqlite:///memo.sqlite")

# psycopgを使用する形式に変換
if database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

db: SQLAlchemy = SQLAlchemy(app)


# メモのデータベースモデル
class MemoItem(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.Text, nullable=False)
    body: str = db.Column(db.Text, nullable=False)


# テーブル作成
with app.app_context():
    db.create_all()


# メモ一覧を表示
@app.route("/", methods=["GET"])
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


# メモ編集画面を表示
@app.route("/memo/<int:id>", methods=["GET"])
def memo(id: int):

    # 新規作成の場合
    if id == 0:
        it = MemoItem(
            title="__無題__",
            body=""
        )

    else:
        it = db.session.get(MemoItem, id)

        if it is None:
            return "メモが見つかりません", 404

    return render_template("memo.html", it=it)


# 新規メモを作成
@app.route("/memo", methods=["POST"])
def create_memo():

    title = request.form.get("title", "__無題__")
    body = request.form.get("body", "")

    if title == "":
        return "タイトルは空にできません", 400

    item = MemoItem(
        title=title,
        body=body
    )

    db.session.add(item)
    db.session.commit()

    return redirect(url_for("index"))


# 既存メモを更新
@app.route("/memo/<int:id>", methods=["PATCH"])
def update_memo(id: int):

    item = db.session.get(MemoItem, id)

    if item is None:
        return jsonify({
            "message": "メモが見つかりません"
        }), 404

    data = request.get_json()

    title = data.get("title")
    body = data.get("body")

    if title is not None:

        if title == "":
            return jsonify({
                "message": "タイトルは空にできません"
            }), 400

        item.title = title

    if body is not None:
        item.body = body

    db.session.commit()

    return jsonify({
        "message": "メモを更新しました"
    }), 200


# メモを削除
@app.route("/memo/<int:id>", methods=["DELETE"])
def delete_memo(id: int):

    item = db.session.get(MemoItem, id)

    if item is None:
        return jsonify({
            "message": "メモが見つかりません"
        }), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "message": "メモを削除しました"
    }), 200


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8888
    )