from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")



##################################################



@app.route("/")
@login_required
def index():
    return apology("TODO index")






@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares  of stock."""

    # if user reached route via POST
    if request.method == "POST":

        symbol = request.form["symbol"]

        # look up symbol
        stock = lookup(symbol)

        # ensure proper symbol input
        if stock == None:
            return apology("Invalid symbol")

         # ensure proper input for shares
        try:
            shares = int(request.form["shares"])
        except:
            return apology("Invalid shares")

        if shares < 0:
            return apology("Invalid shares")

        # if proper stock and shares
        else:

            # calculate price of the stock
            price = stock["price"] * shares

            # retrieve cash from user
            cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

            # if enough cash to buy
            if cash > price:
                bought = db.execute("INSERT INTO portfolio (user_id, symbol, name, shares, price) VALUES (:user_id, :symbol, :name, :shares, :price)", user_id=session["user_id"], symbol=stock["symbol"], name=stock["name"], shares=stock["shares"], price=stock["price"])

                if not bought:
                    return apology("Unable to buy")

            # apology if can't buy
            else:
                return apology("Not enough cash")

            # update cash (in users table)
            db.execute("UPDATE users SET cash = cash - :price WHERE id = :id", price=price, id=session["user_id"])

            # redirect to index
            return redirect(url_for("index"))

    # if user reached route via GET
    else:
        return render_template("buy.html")








@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    return apology("TODO history")





@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # if user reached route via POST
    if request.method == "POST":

        # retrieve and look up the symbol
        symbol = request.form["symbol"]
        stock = lookup(symbol)

        # check if valid stock symbol
        if stock == None:
            return apology("Invalid symbol")

        # display the quote
        else:
            return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])

    # if user reached route via GET
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # password confirmation failed
        elif request.form["password"] != request.form["repassword"]:
            return apology("password must match confirmation password")

        # insert password hash and username in database
        hash = pwd_context.hash(request.form["password"])

        # insert username and hashed password into database
        insertuser = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form["username"], hash=hash)

        # if failed (username not unique so insertuser == None)
        if not insertuser:
            return apology("try a different username")

        else:
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

            # remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # redirect
            return redirect(url_for("index"))


    # if user reached route via GET (clicking a link or redirect)
    else:
        return render_template("register.html")








@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    return apology("TODO sell")
