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