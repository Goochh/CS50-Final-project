import sqlite3

from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from functions import login_required

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

@app.route("/program", methods=["GET"])
@login_required
def program():
    return render_template("program.html")

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

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")

        # # Query database for username
        # rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # # Ensure username exists and password is correct
        # if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #     return flash("invalid username and/or password", 403)

        # # Remember which user has logged in
        # session["user_id"] = rows[0]["id"]

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
            return flash("Must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):

            flash("Must provide password :|", 400)
            return redirect("/register")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation") == request.form.get("password"):
            flash("Passwords don't match :(", 400)
            return redirect("/register")

        # Open database
        conn = sqlite3.connect('permabulk.db', check_same_thread=False)
        c = conn.cursor()

        try: c.execute("INSERT INTO users (username, password) VALUES(?, ?)", (request.form.get("username"), generate_password_hash(request.form.get("password")),))

        except sqlite3.IntegrityError as error:
            flash("Username already taken :(")
            return redirect("/register")

    
        # Add to session to log user in
        session["username"] = request.form.get("username")

        c.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = c.fetchall()
        
        session["user_id"] = rows[0][0]
 
        # Close database
        conn.commit()
        conn.close()


        # Flash message for succesfull transaction
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
    return redirect("/")

@app.route("/test")
def test():

    return render_template("test.html")


if __name__ == '__main__':
    app.run(debug=True)
