import os
import sys
import time

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Welcome message
    username = session.get("username")

    if username:
        greeting = f"Welcome back, {username}!"

    else:
        greeting = "Welcome to C$50 Finance!"

    # Load list of dicts
    stocks = db.execute("SELECT stock_symbol, shares FROM portfolio WHERE user_id = ?", session["user_id"])

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    totalcash = cash[0]["cash"]
    cash = cash[0]["cash"]

    count = 0
    # for each stock check current price
    for stock in stocks:
        prix = lookup(stock["stock_symbol"])
        stock["current_price"] = prix["price"]

        total = prix["price"] * stocks[count]["shares"]
        totalcash = totalcash + total

        # Add "total_value" to purchases list of dictionaries and put the value of stock into it
        stocks[count]["total_value"] = total
        count = count + 1

    return render_template("index.html", stocks=stocks, cash=cash, totalcash=totalcash, greeting=greeting)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure symbol exists
        if lookup(request.form.get("symbol")) == None:
            return apology("symbol doesn't exist", 400)

        # Ensure amount of shares bought is positive & an integer
        try:
            if not int(request.form.get("shares")) > 0:
                return apology("must buy a positive amount of shares", 400)

        except ValueError as e:
            return apology("whole numbers please", 400)

        # Load stock dictionary in stock
        stock = lookup(request.form.get("symbol"))

        # Calculate amount of shares * current stock price
        price = float(stock.get("price")) * float(request.form.get("shares"))

        # Check amount of cash of user
        guap = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Funds too low check and add purchase
        if price > guap[0]["cash"]:
            return apology("Not enough funds")

        else:

            # Update cash value
            guap[0]["cash"] = guap[0]["cash"] - price
            db.execute("UPDATE users SET cash = ? WHERE id = ?", guap[0]["cash"], session["user_id"])

        # Add to portfolio
        stockcheck = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND stock_symbol = ?", [session["user_id"]],
                                request.form.get("symbol"))

        if stockcheck:
            db.execute("UPDATE portfolio SET shares = shares + ? WHERE user_id = ? AND stock_symbol = ?",
                       request.form.get("shares"), session["user_id"], request.form.get("symbol"))

        else:
            db.execute("INSERT INTO portfolio (user_id, stock_symbol, shares) VALUES (?, ?, ?)",
                       session["user_id"], request.form.get("symbol"), request.form.get("shares"))

        # Log purchase
        db.execute("INSERT INTO purchases (user_id, stock_symbol, amount, price, date, transaction_type) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], request.form.get("symbol"), request.form.get("shares"), price, datetime.now(), "bought")

        # Bought successfully
        flash(f'Bought {request.form.get("shares")} share(s) of {request.form.get("symbol")} successfully!')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    purchases = db.execute("SELECT * FROM purchases WHERE user_id = ?", session["user_id"])

    # for each stock check current price
    for purchase in purchases:
        prix = lookup(purchase["stock_symbol"])
        purchase["current_price"] = prix["price"]

        # Add "current_price" to purchases list of dictionaries and put the value of stock into it
        purchases[0]["current_price"] = purchase["current_price"]

    return render_template("history.html", purchases=purchases)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Succesful login
        flash("You were successfully logged in!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not lookup(request.form.get("symbol")) == None:
            quoted = lookup(request.form.get("symbol"))
            return render_template("quoted.html", quoted=quoted)

        else:
            return apology("Not a symbol", 400)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("passwords don't match", 400)

        # Add user into database & Avoid duplicate username
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))

        except ValueError as error:
            return apology("username already exists", 400)

        # Add to session to log user in
        session["username"] = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Flash message for succesfull transaction
        flash("Registration successfull!")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure symbol exists
        if lookup(request.form.get("symbol")) == None:
            return apology("symbol doesn't exist", 400)

        # Ensure amount of shares bought is positive & an integer
        try:
            if not int(request.form.get("shares")) > 0:
                return apology("must buy a positive amount of shares", 400)

        except ValueError as e:
            return apology("whole numbers please", 400)

        # Look up current stock price
        stockprice = lookup(request.form.get("symbol"))

        # Calculate amount of shares * current stock price for the value
        price = stockprice.get("price") * float(request.form.get("shares"))

        # Check if user has that many shares of the stock
        shares = db.execute("SELECT shares FROM portfolio WHERE user_id = ? AND stock_symbol = ?",
                            session["user_id"], request.form.get("symbol"))

        # Load cash
        guap = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Check if enough shares sell and add funds
        if int(request.form.get("shares")) > shares[0]["shares"]:
            return apology("Not enough shares")

        else:

            # Update cash value
            guap[0]["cash"] = guap[0]["cash"] + price
            db.execute("UPDATE users SET cash = ? WHERE id = ?", guap[0]["cash"], session["user_id"])

        # Remove portfolio
        db.execute("UPDATE portfolio SET shares = shares - ? WHERE user_id = ? AND stock_symbol = ?", request.form.get("shares"),
                   session["user_id"], request.form.get("symbol"))

        # Log purchase
        db.execute("INSERT INTO purchases (user_id, stock_symbol, amount, price, date, transaction_type) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], request.form.get("symbol"), request.form.get("shares"), price, datetime.now(), "sold")

        # Flash message for succesfull transaction
        flash(f'Sold {request.form.get("shares")} share(s) of {request.form.get("symbol")} successfully!')

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Load stocks for the select menu
        stocks = db.execute("SELECT stock_symbol, shares FROM portfolio WHERE user_id = ?", session["user_id"])

        return render_template("sell.html", stocks=stocks)


@app.route("/add_funds", methods=["GET", "POST"])
@login_required
def add_funds():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure amount of shares bought is positive & an integer
        try:
            if not int(request.form.get("funds")) > 0:
                return apology("must buy a positive amount of funds", 400)

        except ValueError as e:
            return apology("whole numbers please", 400)

        # Check amount of cash of user
        guap = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        # Funds
        funds = float(request.form.get("funds"))

        # Update guap
        db.execute("UPDATE users SET cash = ? WHERE id = ?", guap[0]["cash"] + funds, session["user_id"])

        # Flash message for succesfull transaction
        flash(f'Added {usd(funds)} successfully!')

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add_funds.html")


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)