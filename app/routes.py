from ssl import ALERT_DESCRIPTION_UNKNOWN_PSK_IDENTITY
from app import app
import mysql.connector
from app.forms import AppointmentForm
import os
from flask import (Blueprint, render_template, redirect)
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')

my_conn=mysql.connector.connect(
    user = os.environ.get("DB_USER"),
    password = os.environ.get("DB_PASS"),
    db = os.environ.get("DB_NAME"),
    host = os.environ.get("DB_HOST"),
)


@bp.route("/", methods=['GET', 'POST'])
def main():
    mycursor = my_conn.cursor()
    form = AppointmentForm()
    data = ()
    if form.validate_on_submit():
        mycursor.execute("INSERT INTO appointments(name, start_datetime, end_datetime, description, private) VALUES(%s, %s, %s, %s, %s)", (form.name.data, datetime.combine(form.start_date.data, form.start_time.data), datetime.combine(form.end_date.data, form.end_time.data), form.description.data, form.private.data))
        my_conn.commit()
        return redirect('/')
    mycursor.execute("SELECT id, name, start_datetime, end_datetime FROM appointments ORDER BY start_datetime")
    rows = mycursor.fetchall()
    return render_template('main.html', rows=rows, form=form)
