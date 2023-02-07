import sqlite3

from sqlite3 import Error
from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from functions import login_required, open_db, close_db

app = Flask(__name__, static_folder='static')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

conn = open_db('permabulk.db')
c = conn.cursor

c.execute("""CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE IF NOT EXISTS 'programs' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
'program_name' TEXT NOT NULL,
'description' TEXT NOT NULL, image);
CREATE TABLE Workouts (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  program_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  date DATE NOT NULL,
  exercise_name TEXT NOT NULL,
  sets INTEGER NOT NULL,
  reps INTEGER NOT NULL,
  weight REAL NOT NULL,
  FOREIGN KEY (program_id) REFERENCES Programs(id),
  FOREIGN KEY (user_id) REFERENCES Users(id)
);
CREATE TABLE user_program_progress (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  program_id INTEGER NOT NULL,
  week INTEGER NOT NULL DEFAULT 1, day INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (program_id) REFERENCES programs (id)
);
CREATE TABLE exercises (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  program_id INTEGER NOT NULL,
  exercise TEXT NOT NULL, day INTEGER, reps TEXT, sets INTEGER NOT NULL DEFAULT 0, weight REAL,
  FOREIGN KEY (program_id) REFERENCES programs (id)
);
CREATE UNIQUE INDEX user_id_unique_index ON user_program_progress (user_id);""")

close_db(conn)


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/programs", methods=["GET", "POST"])
@login_required
def programs():

    
    # # Open DB
    # conn = open_db('permabulk.db')
    # c = conn.cursor()

    # # User already picked program
    # c.execute("SELECT * FROM user_program_progress WHERE user_id = ?", (session["user_id"], ))
    # rows = c.fetchall()

    # # Close DB
    # close_db(conn)

    # # If there is a row returned user started program
    # if len(rows) == 1:
    #     flash("Already picked program")
    #     return redirect("/current_program")
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Fetch chosen program
        session["program_id"] = request.form.get("program_id")
        
        # Open DB
        conn = open_db('permabulk.db')
        c = conn.cursor()

        # Update user progress table
        try:
            c.execute('INSERT INTO user_program_progress (user_id, program_id) VALUES (?, ?);', (session["user_id"], session["program_id"], ))
        
        except Error as e:
            c.execute('UPDATE user_program_progress SET program_id = ? WHERE user_id = ?;', (session["program_id"], session["user_id"], ))

        # Query DB
        c.execute('SELECT * FROM programs')
        rows = c.fetchall()

        # Get the column names
        columns = [description[0] for description in c.description]
        
        # Convert rows to a list of dictionaries
        programs = [dict(zip(columns, row)) for row in rows]

        # Close DB
        close_db(conn)

        # Redirect user to home page
        return redirect("/current_program")


    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Open DB
        conn = open_db('permabulk.db')
        c = conn.cursor()

        # Query DB
        c.execute('SELECT * FROM programs')
        rows = c.fetchall()

        # Get the column names
        columns = [description[0] for description in c.description]
        
        # Convert rows to a list of dictionaries
        programs = [dict(zip(columns, row)) for row in rows]

        return render_template("programs.html", programs=programs)


@app.route("/current_program", methods=["GET", "POST"])
@login_required
def current_program():
    
    # Open DB
    conn = open_db('permabulk.db')
    c = conn.cursor()

    # Fetch user progress from DB
    c.execute('SELECT * FROM user_program_progress WHERE user_id = ?;', (session["user_id"], ))
    rows = c.fetchall()

    # Get the column names
    columns = [description[0] for description in c.description]
    
    # Convert rows to a list of dictionaries
    userprogress = [dict(zip(columns, row)) for row in rows]

    day = userprogress[0].get('day')
    program_id = userprogress[0].get('program_id')

    # Query DB
    c.execute('SELECT * FROM exercises WHERE day = ? AND program_id = ?;', (day, program_id, ))
    rows = c.fetchall()

    # Get the column names
    columns = [description[0] for description in c.description]
    
    # Convert rows to a list of dictionaries
    exercises = [dict(zip(columns, row)) for row in rows]

    # Close and commit DB
    close_db(conn)

    # In case of StrongLift 5x5 change day to Workout A and B
    if program_id == 4 and day == 1:
        day = 'A'

    elif program_id == 4 and day == 2:
        day = 'B'

    return render_template("current_program.html", exercises=exercises, day=day)

    exc
@app.route("/diet", methods=["GET"])
@login_required
def diet():
    return render_template("diet.html")


@app.route("/statistics", methods=["GET"])
@login_required
def statistics():
    return render_template("statistics.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect("/login")

        # Open database
        conn = open_db('permabulk.db')
        c = conn.cursor()

        # Ensure username exists and password is correct
        c.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = c.fetchall()

        # If there is no row returned username doesn't exist
        if len(rows) != 1:
            flash("Invalid username and/or password")
            return redirect("/login")

        # Get the column names
        columns = [description[0] for description in c.description]
        
        # Convert rows to a list of dictionaries
        rows = [dict(zip(columns, row)) for row in rows]

        # Check if password is correct
        if not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Invalid username and/or password")
            return redirect("/login")

        # Add to session
        session["username"] = request.form.get("username")
        session["user_id"] = rows[0]["user_id"]

        # Close database
        close_db(conn)

        # Succesful login
        flash("You were successfully logged in!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

        
@app.route("/register", methods=["GET", "POST"])
def register():
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return flash("Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):

            flash("Must provide password :|")
            return redirect("/register")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation") == request.form.get("password"):
            flash("Passwords don't match :(")
            return redirect("/register")

        # Open database
        conn = open_db('permabulk.db')
        c = conn.cursor()

        # INSERT new unique user into database
        try: c.execute("INSERT INTO users (username, password) VALUES(?, ?)", (request.form.get("username"), generate_password_hash(request.form.get("password")),))

        except sqlite3.IntegrityError as error:
            flash("Username already taken :(")
            return redirect("/register")

        # Add to session to log user in
        c.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = c.fetchall()

        # Set current session
        session["username"] = request.form.get("username")
        session["user_id"] = rows[0][0]

        # Close database
        close_db(conn)

        # Flash message for succesfull registration
        flash("Registration successfull!")
       
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():

    #Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/test")
def test():

    return render_template("calculator.html")


if __name__ == '__main__':
    app.run(debug=True)
