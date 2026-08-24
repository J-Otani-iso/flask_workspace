import os, json, calendar, re
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for

# 予定イベントの保存先
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(SCRIPT_DIR, "calendar_events.json")
# イベントデータをファイルから読む
events = {}
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        events = json.load(f)

# Flaskのアプリを起動
app: Flask = Flask(__name__)
# ルートへGETアクセスしたとき
@app.route("/", methods=["GET"])
def index_get():
    # パラメーターを取得し、デフォルト値を今月とする
    now = datetime.now()
    year = int(request.args.get("year", now.year))
    month = int(request.args.get("month", now.month))
    # 月曜始まりのカレンダーを作成
    cal = calendar.Calendar(calendar.MONDAY)