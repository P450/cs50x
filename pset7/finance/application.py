"""
    This program does not prevent race conditions
        https://stackoverflow.com/questions/6477574/do-database-transactions-prevent-race-conditions

    Consider additional features:
        https://en.wikipedia.org/wiki/ACID
        https://stackoverflow.com/questions/549/the-definitive-guide-to-form-based-website-authentication/477578#477578
"""

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

@app.route("/")
@login_required
def index():
    """Display the summary of the user portfolio."""

    # declare a variable for the total asset
    assets = 0

    # update stock prices and calculate the total value of shares
    companies = db.execute("SELECT * \
                            FROM portfolio \
                            WHERE users_id = :id \
                            GROUP BY symbol", id=session["user_id"])

    # for each company in portfolio
    for company in companies:

        symbol = company["symbol"]
        shares = company["shares"]

        # calculate current and total value of shares
        stockinfo = lookup(symbol)
        shares_value = stockinfo["price"] * shares

        # add to total assets
        assets += shares_value

        # update portfolio with current price and new totals
        db.execute("UPDATE portfolio \
                    SET price = :price, total = :total \
                    WHERE users_id = :id AND symbol = :symbol", \
                    price=usd(stockinfo["price"]), total=usd(shares_value), \
                    id=session["user_id"], symbol=stockinfo["symbol"])

    # retrieve user's cash balance
    cash = db.execute("SELECT cash \
                       FROM users \
                       WHERE id=:id", id=session["user_id"])

    # add to total assets
    assets += cash[0]["cash"]

    # select portfolio columns to display
    portfolio = db.execute("SELECT * \
                            FROM portfolio \
                            WHERE users_id=:id \
                            ORDER BY symbol", id=session["user_id"])

    # render index with symbol, name, shares, cur price, total
    return render_template("index.html", portfolio=portfolio, \
                                         cash=usd(cash[0]["cash"]), \
                                         assets=usd(assets))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares  of stock."""

    # if user reached route via POST
    if request.method == "POST":

        # look up symbol
        symbol = request.form["symbol"]
        stockinfo = lookup(symbol)

        # ensure proper input for symbol
        if stockinfo == None:
            return apology("Invalid symbol")

        # ensure proper input for shares
        try:
            shares = int(request.form["shares"])

            if shares < 1:
                return apology("Invalid shares")
        except:
            return apology("Invalid shares")

        # calculate the total cost of the shares
        cost = stockinfo["price"] * shares

        # select cash from database
        balance = db.execute("SELECT cash \
                              FROM users \
                              WHERE id = :id", id=session["user_id"])
        cash = balance[0]["cash"]

        # if not enough cash
        if cost > cash:
            return apology("Not enough cash")

        # record the purchase in history
        db.execute("INSERT INTO history (users_id, symbol, name, shares, price) \
                    VALUES (:id, :symbol, :name, :shares, :price)", \
                    id=session["user_id"], symbol=stockinfo["symbol"], \
                    name=stockinfo["name"], shares=shares, price=usd(stockinfo["price"]))

        # update cash balance
        db.execute("UPDATE users \
                    SET cash = cash - :cost \
                    WHERE id = :id", \
                    cost=cost, id=session["user_id"])

        # #check if stock is already in portfolio
        portfolio = db.execute("SELECT shares \
                                FROM portfolio \
                                WHERE users_id = :id AND symbol = :symbol", \
                                id=session["user_id"], symbol=stockinfo["symbol"])

        # if stock doesn't exist in portfolio
        if not portfolio:

            # insert new stock into portfolio (did not usd() here since index will do it)
            db.execute("INSERT INTO portfolio (users_id, symbol, name, shares, price, total) \
                        VALUES (:id, :symbol, :name, :shares, :price, :total)", \
                        id=session["user_id"], symbol=stockinfo["symbol"], name=stockinfo["name"], \
                        shares=shares, price=stockinfo["price"], total=cost)

        else:
            # update shares
            shares += portfolio[0]["shares"]

            db.execute("UPDATE portfolio \
                        SET shares = :oldshares \
                        WHERE users_id = :id AND symbol = :symbol", \
                        oldshares=shares, id=session["user_id"], symbol=stockinfo["symbol"])

        # display success message
        flash("Bought!")

        # redirect to index
        return redirect(url_for("index"))

    # if user reached route via GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    history = db.execute("SELECT * \
                          FROM history \
                          WHERE users_id = :id", id=session["user_id"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # query database for username
        rows = db.execute("SELECT * \
                           FROM users \
                           WHERE username = :username", \
                           username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("Invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # if user reached route via GET
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
            return render_template("quoted.html", name=stock["name"], \
                                                  price=usd(stock["price"]), \
                                                  symbol=stock["symbol"])
    # if user reached route via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any prior user_id
    session.clear()

    if request.method == "POST":

        # ensure username was submitted
        if not request.form["username"]:
            return apology("Must provide username")

        # ensure password was submitted
        elif not request.form["password"]:
            return apology("Must provide password")

        # password confirmation failed
        elif request.form["password"] != request.form["repassword"]:
            return apology("Confirmation password does not match")

        # hash the password
        hash = pwd_context.hash(request.form["password"])

        # insert username and hashed password into database
        insertuser = db.execute("INSERT INTO users (username, hash) \
                                 VALUES(:username, :hash)", \
                                 username=request.form["username"], hash=hash)

        # if failed (username not unique so insertuser == None)
        if not insertuser:
            return apology("Try a different username")

        rows = db.execute("SELECT * \
                           FROM users \
                           WHERE username = :username", \
                           username=request.form["username"])

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect
        return redirect(url_for("index"))


    # if user reached route via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    # if user reached route via POST
    if request.method == "POST":

        # assign variable names
        symbol = request.form["symbol"]
        shares = request.form["shares"]

        # ensure proper input for symbol
        if not symbol:
            return apology("Must provide symbol")

        # ensure proper input for shares
        if not shares:
            return apology("Must provide shares")

        try:
            shares = int(shares)
            if shares < 1:
                return apology("Invalid shares")
        except:
            return apology("Invalid shares")

        # get stock info
        stockinfo = lookup(symbol)

        # select from portfolio
        symbolport = db.execute("SELECT * \
                                 FROM portfolio \
                                 WHERE users_id = :id AND symbol = :symbol", \
                                 id=session["user_id"], symbol=stockinfo["symbol"])
        # symbol does not exist
        if not symbolport:
            return apology("Doesn't exist in portfolio")

        # select shares from portfolio
        sharesport = db.execute("SELECT shares \
                                 FROM portfolio \
                                 WHERE users_id = :id AND symbol = :symbol", \
                                 id=session["user_id"], symbol=stockinfo["symbol"])

        # if not enough shares in portfolio
        if sharesport[0]["shares"] < shares:
            return apology("Not enough shares in portfolio")

        # get current info on stock and shares
        sold = stockinfo["price"] * shares

        # add to history
        db.execute("INSERT INTO history (users_id, symbol, name, shares, price) \
                    VALUES (:id, :symbol, :name, :shares, :price)",
                    id=session["user_id"], symbol=stockinfo["symbol"], name=stockinfo["name"], \
                    shares=-(shares), price=usd(stockinfo["price"]))

        # if 0 shares, delete stock from portfolio
        if sharesport[0]["shares"] - shares == 0:
            db.execute("DELETE FROM portfolio \
                        WHERE users_id = :id AND symbol = :symbol", \
                        id=session["user_id"], symbol=stockinfo["symbol"])

        # else update shares in portfolio
        else:
            db.execute("UPDATE portfolio \
                        SET shares = shares - :shares \
                        WHERE users_id = :id AND symbol = :symbol", \
                        shares=shares, id=session["user_id"], symbol=stockinfo["symbol"])

        # update cash balance
        db.execute("UPDATE users \
                    SET cash = cash + :sold \
                    WHERE id = :id", \
                    id=session["user_id"], sold=sold)

        # display success message
        flash("Sold!")

        return redirect(url_for("index"))

    # if user reached route by GET
    else:
        return render_template("sell.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    # if request.method == "GET":
    #     return render_template("account.html")

    # elif request.method == "POST":

    # ensure proper submission
    if not request.form["oldpw"] or \
       not request.form["newpw"] or \
       not request.form["confirmpw"]:
        return apology("All fields must be filled")

    if request.form["newpw"] != request.form["confirmpw"]:
        return apology("Confirmation password does not match")

    if request.form["oldpw"] == request.form["newpw"]:
        return apology("Choose a different password")

    # select hash from users table
    pwcheck = db.execute("SELECT hash \
                          FROM users \
                          WHERE id = :id", \
                          id=session["user_id"])

    # ensure username exists and password is correct
    if not pwd_context.verify(request.form["oldpw"], pwcheck[0]["hash"]):
        return apology("Invalid password")

    else:
        # update password
        db.execute("UPDATE users \
                    SET hash = :hash \
                    WHERE id = :id", \
                    hash=pwd_context.hash(request.form["newpw"]), id=session["user_id"])

    flash("Password changed!")

    return redirect(url_for("index"))

