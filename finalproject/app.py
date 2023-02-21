import sqlite3, json

from sqlite3 import Error
from flask import Flask, flash, redirect, render_template, url_for, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime



from functions import login_required, db_fetch, db_modify, get_stats

app = Flask(__name__, static_folder='static')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
        
        # # Update user progress table
        db_modify(  """
                    INSERT OR REPLACE INTO user_program_progress (user_id, program_id)
                    VALUES (?, ?);
                    """, (session["user_id"], session["program_id"], ))


        # Convert rows to a list of dictionaries
        programs = db_fetch('SELECT * FROM programs')

        # Redirect user to home page
        return redirect("/current_program")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Fetch programs
        programs = db_fetch('SELECT * FROM programs')

        return render_template("programs.html", programs=programs)


@app.route("/current_program", methods=["GET", "POST"])
@login_required
def current_program():
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        
        # Extract values from the form
        kg = request.form.getlist('kg')
        reps = request.form.getlist('reps')
        exercise_sets = request.form.getlist('exercise')

        # Get userprogress
        userprogress = db_fetch('SELECT * FROM user_program_progress WHERE user_id = ?;', (session["user_id"], ))

        # Store the workout data in the database
        for i in range(len(exercise_sets)):
            exercise_set = exercise_sets[i] if exercise_sets[i] else None
            weight = int(kg[i]) if kg[i] else None
            num_reps = int(reps[i]) if reps[i] else None
            
            db_modify('INSERT INTO workouts (user_id, program_id, date, exercise_name, weight, reps) VALUES (?, ?, ?, ?, ?, ?)', 
                    (session["user_id"], session["program_id"], datetime.now(), exercise_set, weight, num_reps, ))

        # Update user progress
        db_modify(  """
                        UPDATE user_program_progress 
                        SET day = CASE
                            WHEN day < 7 THEN day + 1
                            ELSE 1
                        END,
                        week = CASE
                            WHEN day = 7 THEN week + 1
                            ELSE week
                        END
                        WHERE user_id = ?
                    """, (session["user_id"], ))


        return render_template("thank_you.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Get userprogress
        userprogress = db_fetch('SELECT * FROM user_program_progress WHERE user_id = ?;', (session["user_id"], ))
        print(userprogress)

        day = userprogress[0]["day"]
        program_id = userprogress[0]["program_id"]

        # Get exercises
        exercises = db_fetch('SELECT * FROM exercises WHERE day = ? AND program_id = ?;', (day, program_id, ))

        # # Get program_name
        programs = db_fetch('SELECT program_name FROM programs WHERE id = ?;', (program_id, ))
        program_name = programs[0]["program_name"]
 
        # In case of StrongLift 5x5 change day to Workout A and B
        if program_id == 4 and day == 1:
            day = 'A'

        elif program_id == 4 and day == 2:
            day = 'B'

        return render_template("current_program.html", exercises=exercises, day=day, program_name=program_name)

@app.route("/recipes", methods=["GET"])
@login_required
def recipes():

    # User reached route via GET (as by clicking a link or via redirect)
    
    # Fetch recipes
    recipes = db_fetch('SELECT * FROM recipes')

    return render_template("recipes.html", recipes=recipes)
    

@app.route("/statistics", methods=["GET"])
@login_required
def statistics():

    onerms = get_stats()
    

    return jsonify(onerms)

@app.route("/1rm", methods=["GET", "POST"])
@login_required
def onerepmax():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":  

        # Extract values from the form
        benchpress_kg = request.form.get('benchpress_kg')
        squat_kg = request.form.get('squat_kg')
        deadlift_kg = request.form.get('deadlift_kg')
        OHP_kg = request.form.get('OHP_kg')

        # Update user one rep max
        if benchpress_kg:
            db_modify('UPDATE user_program_progress SET benchpress1rm = ? WHERE user_id = ?', (benchpress_kg, session["user_id"], ))
        
        if squat_kg:
            db_modify('UPDATE user_program_progress SET backsquat1rm = ? WHERE user_id = ?', (squat_kg, session["user_id"], ))

        if deadlift_kg:
            db_modify('UPDATE user_program_progress SET deadlift1rm = ? WHERE user_id = ?', (deadlift_kg, session["user_id"], ))

        if OHP_kg:
            db_modify('UPDATE user_program_progress SET overheadpress1rm = ? WHERE user_id = ?', (OHP_kg, session["user_id"], ))
        
        return redirect("/1rm")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Fetch user progress
        onerepmaxs = db_fetch('SELECT * FROM user_program_progress WHERE user_id = ?', (session["user_id"], ))

        


        return render_template("onerepmax.html", onerepmaxs=onerepmaxs)

    


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

        # Ensure username exists and password is correct
        userinfo = db_fetch('SELECT * FROM users WHERE username = ?', (request.form.get("username"),))

        # If there is no row returned username doesn't exist
        if len(userinfo) != 1:
            flash("Invalid username and/or password")
            return redirect("/login")

        # Check if password is correct
        if not check_password_hash(userinfo[0]["password"], request.form.get("password")):
            flash("Invalid username and/or password")
            return redirect("/login")

        # Add to session
        session["username"] = request.form.get("username")
        session["user_id"] = userinfo[0]["user_id"]

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

        # INSERT new unique user into database
        try: db_modify('INSERT INTO users (username, password) VALUES (?, ?);', (request.form.get("username"), generate_password_hash(request.form.get("password")),))

        except sqlite3.IntegrityError as error:
            flash("Username already taken :(")
            return redirect("/register")

        # Add to session to log user in
        user = db_fetch('SELECT * FROM users WHERE username = ?', (request.form.get("username"),))
        
        # Set current session
        session["username"] = request.form.get("username")
        session["user_id"] = user[0]["user_id"]
        session["program_id"] = 1

        # Set default user_program_progress
        db_modify('INSERT INTO user_program_progress (user_id, program_id) VALUES (?, 1)', (session["user_id"], ))

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


if __name__ == '__main__':
    app.run(debug=True)
