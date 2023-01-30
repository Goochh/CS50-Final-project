import sqlite3

from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from functions import login_required, open_db, close_db

app = Flask(__name__, static_folder='static')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/programs", methods=["GET"])
@login_required
def programs():
    return render_template("programs.html")


@app.route("/program", methods=["GET", "POST"])
@login_required
def program():
    
    # Open DB
    conn = open_db('permabulk.db')
    c = conn.cursor()

    # Query DB
    c.execute('SELECT exercise, reps FROM exercises WHERE day = 1;')
    rows = c.fetchall()

    # Get the column names
    columns = [description[0] for description in c.description]
    
    # Convert rows to a list of dictionaries
    exercises = [dict(zip(columns, row)) for row in rows]

    print(exercises)
    



    
    return render_template("program.html", exercises=exercises)

    


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
