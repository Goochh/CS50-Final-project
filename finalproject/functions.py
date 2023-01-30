import sqlite3

from sqlite3 import Error
from functools import wraps
from flask import request, redirect, url_for, session



def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def open_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def close_db(conn):
    try:
        conn.close()
    except Error as e:
        print(e)