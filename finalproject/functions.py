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


def get_stats():
    # Fetch workout data  
    workouts_data = db_fetch('SELECT exercise_name, reps, weight, date FROM workouts WHERE user_id = ? AND exercise_name IN (?, ?, ?, ?)',
                         (session["user_id"], 'Bench Press (Barbell)-set-4', 'Squat (Barbell)-set-4', 'Overhead Press (Barbell)-set-4', 'Deadlift (Barbell)-set-0'))


    # Calculate one rep max for each exercise. weight * (1 + reps/30) = ekley formula
    exercise_1rm_dict = {}

    # For the amount of results
    for i in range(len(workouts_data)):
        exercise_name = workouts_data[i]["exercise_name"]
        exercise_name = exercise_name[:-6]
        date = workouts_data[i]["date"]

        # Apply ekley formula to fetched data
        exercise_1rm = round(workouts_data[i]["weight"] * (1 + workouts_data[i]["reps"]/30), 2)

        # If exercise not yet in list of dicts
        if exercise_name not in exercise_1rm_dict:
            exercise_1rm_dict[exercise_name] = []    

        # Add date and calculated 1rm to certain exercise
        exercise_1rm_dict[exercise_name].append({"date": date[:-7], "onerm": exercise_1rm})

    return exercise_1rm_dict

        
