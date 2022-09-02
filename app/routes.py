from ssl import ALERT_DESCRIPTION_UNKNOWN_PSK_IDENTITY
from app import app
import mysql.connector

import os

from flask import (Blueprint, render_template)

bp = Blueprint('main', __name__, url_prefix='/')

my_conn=mysql.connector.connect(
    user = os.environ.get("DB_USER"),
    password = os.environ.get("DB_PASS"),
    db = os.environ.get("DB_NAME"),
    host = os.environ.get("DB_HOST"),
)

@bp.route("/")
def main():
    mycursor = my_conn.cursor()
    mycursor.execute("SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime")
    rows = mycursor.fetchall()
    return render_template('main.html', rows=rows)
