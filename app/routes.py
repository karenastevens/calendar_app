from ssl import ALERT_DESCRIPTION_UNKNOWN_PSK_IDENTITY
from app import app
import mysql.connector
from app.forms import AppointmentForm
import os
from flask import (Blueprint, render_template, redirect, url_for)
from datetime import (datetime, timedelta)

bp = Blueprint('main', __name__, url_prefix='/')

my_conn=mysql.connector.connect(
    user = os.environ.get("DB_USER"),
    password = os.environ.get("DB_PASS"),
    db = os.environ.get("DB_NAME"),
    host = os.environ.get("DB_HOST"),
)


@bp.route("/")
def main():
    d = datetime.now()
    return redirect(url_for(".daily", year=d.year, month=d.month, day=d.day))

@bp.route('/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
def daily(year, month, day):
    mycursor = my_conn.cursor()
    form = AppointmentForm()
    if form.validate_on_submit():
        mycursor.execute("INSERT INTO appointments(name, start_datetime, end_datetime, description, private) VALUES(%s, %s, %s, %s, %s)", (form.name.data, datetime.combine(form.start_date.data, form.start_time.data), datetime.combine(form.end_date.data, form.end_time.data), form.description.data, form.private.data))
        my_conn.commit()
        return redirect('/')

    day = datetime(year, month, day)
    next_day = (day + timedelta(days=1))
    mycursor.execute("SELECT id, name, start_datetime, end_datetime FROM appointments WHERE start_datetime BETWEEN %s AND %s ORDER BY start_datetime", (day, next_day))
    rows = mycursor.fetchall()
    return render_template('main.html', rows=rows, form=form)
