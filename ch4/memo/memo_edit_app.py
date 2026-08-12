from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import escape

# Flaskとデータベースの初期化 -(*1)
app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memo_edit.sqlite"
db:SQLAlchemy = SQLAlchemy(app)
# メモのデータベースモデルを定義 -(*2)
class MemoItem(db.Model):
    id: int = db.Column(db.Interger, primary_key = True)
    title: str = db.Column(db.Text, nullable = False)
    body: str = db.Column(db.Text, nullable = False)
# データベースの初期化
with app.app_context():
    db.create_all()

# 各種HTMLを定義 -(*3)
CSS = "https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css"
HTML_HEADER = f"""
    <!DOCTYPE html><html><head><meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="{CSS}">
    </head><body class="p-3">
    <h1 class="has-background-info p-3 mb-3">Memo</h1>
"""
HTML_EDITOR_FORM = """
    <div class="card p-3"><form method="POST">
        <label class="label">タイトル：</label>
        <input type="text" name="title" value="{title}" class="input">
"""