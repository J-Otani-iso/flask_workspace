from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
# SQLAlchemyをインポート
from flask_sqlalchemy import SQLAlchemy


app: Flask = Flask(__name__)
login_user_name: str = "osamu"


# Databaseの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# メッセージのデータベースモデル
class Message(db.Model):
    id = db.Column(db.Interger, primary_key=True)