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

# def open_db(db_file):
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except Error as e:
#         print(e)
#     return None

# def close_db(conn):
#     try:
#         conn.commit()
#         conn.close()
#     except Error as e:
#         print(e)

# Accepts a query and optionally parameters, returns the results as a list of dicts
def db_fetch(db_query, db_params=None):
    try:    
        # Open and connect DB
        conn = sqlite3.connect('permabulk.db')
        c = conn.cursor()  
        
        # Fetch from DB
        if db_params is None:
            c.execute(db_query)

        else:
            c.execute(db_query, db_params)

        rows = c.fetchall()

        # Close and commit DB
        conn.commit()
        conn.close()

        # Get the column names
        columns = [description[0] for description in c.description]

        # Convert rows to a list of dictionaries
        listofdicts = [dict(zip(columns, row)) for row in rows]

        # Returns listofdicts
        return(listofdicts)

    except Error as e:
        print(e)

# Accepts a query and optionally parameters, returns the results as a list of dicts
def db_modify(db_query, db_params=None):
    try:
        # Open and connect DB
        conn = sqlite3.connect('permabulk.db')
        c = conn.cursor()  

        # If multiple arguments
        if db_params is None:
            c.execute(db_query)
 
        else:
            c.execute(db_query, db_params)

        # Close and commit DB
        conn.commit()
        conn.close()

    except Error as e:
        print(e)

        
