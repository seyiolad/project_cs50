import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup
from helpers import usd

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
    # Get user's current cash balance
    user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]

    # Get user's stocks holdings
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])

    # Calculate the current price and total value of each holding
    total_value = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total_value"] = stock["total_shares"] * stock["price"]
        total_value += stock["total_value"]

    # Calculate grand total (i.e., stocks’ total value plus cash)
    grand_total = user_cash + total_value

    return render_template("index.html", stocks=stocks, user_cash=user_cash, total_value=total_value, grand_total=grand_total, usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")
        if not shares:
            return apology("must provide shares")
        if not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be a positive integer")

        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol")

        name = quote["name"]

        price = quote["price"]
        total_cost = price * int(shares)

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash = rows[0]["cash"]

        if total_cost > cash:
            return apology("can't afford")

        db.execute("UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
                total_cost=total_cost, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, type, symbol, name, shares, price) VALUES (:user_id, :type, :symbol, :name, :shares, :price)",
                   user_id=session["user_id"], type="buy", symbol=symbol, name=name, shares=shares, price=price)

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = :user_id ORDER BY timestamp DESC", user_id=session["user_id"])

    # Render history template with transaction data
    return render_template("history.html", rows=rows)


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

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("quote.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        symbol = request.form.get("symbol")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Look up stock symbol
        quote = lookup(symbol)

        # Ensure symbol is valid
        if not quote:
            return apology("invalid symbol", 400)

        # Render quoted template with stock symbol and price
        return render_template("quoted.html", name=quote["name"], symbol=quote["symbol"], price=usd(quote["price"]))


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

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username doesn't already exist
        if len(rows) == 1:
            return apology("username already exists", 400)

        # Insert new user into users
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                   request.form.get("username"),
                   generate_password_hash(request.form.get("password")))

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # ensure stock and number of shares are submitted
        if not request.form.get("symbol"):
            return apology("must select stock", 400)
        elif not request.form.get("shares"):
            return apology("must provide number of shares", 400)

        # get the number of shares to sell
        shares = int(request.form.get("shares"))

        # look up the stock and get its current price
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        if not stock:
            return apology("invalid stock symbol", 400)

        price = stock["price"]
        name = stock["name"]

        # check if the user owns enough shares to sell
        rows = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol",
                         user_id=session["user_id"], symbol=symbol)
        total_shares = rows[0]["total_shares"]
        if not total_shares or total_shares < shares:
            return apology("you don't own enough shares to sell", 400)

        # calculate the total sale price and update user's cash balance
        sale_price = price * shares
        db.execute("UPDATE users SET cash = cash + :sale_price WHERE id = :user_id",
                   sale_price=sale_price, user_id=session["user_id"])

        # add transaction to transactions table
        db.execute("INSERT INTO transactions (user_id, symbol, name, type, shares, price) VALUES (:user_id, :symbol, :name, :type, :shares, :price)",
                   user_id=session["user_id"], symbol=symbol, name=name, type="Sell", shares=-shares, price=price)

        flash("Sold !")
        return redirect("/")

    else:
        # get the user's stocks and their total values
        rows = db.execute("""
            SELECT symbol, SUM(shares) as total_shares, price
            FROM transactions
            WHERE user_id = :user_id
            GROUP BY symbol
            HAVING total_shares > 0
            """, user_id=session["user_id"])

        stocks = []
        for row in rows:
            stock = lookup(row["symbol"])
            stocks.append({
                "symbol": row["symbol"],
                "name": stock["name"],
                "shares": row["total_shares"],
                "price": stock["price"],
                "total": row["total_shares"] * stock["price"]
            })

        # get the user's current cash balance
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash = rows[0]["cash"]

        return render_template("sell.html", stocks=stocks, cash=cash)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change user password"""
    if request.method == "POST":
        # Get current password and new password from form
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")

        # Verify current password
        user_hash = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["hash"]
        if not check_password_hash(user_hash, current_password):
            flash("Current password is incorrect", "danger")
            return redirect("/change_password")

        # Update password in database
        hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", hash=hash, user_id=session["user_id"])


        flash("Password changed successfully", "success")
        return redirect("/")

    return render_template("change_password.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to user account"""
    if request.method == "POST":
       # Get amount from form
        amount = float(request.form.get("amount"))

        # Get and Update user's cash balance in database
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]
        cash += amount
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=cash, user_id=session["user_id"])

        flash("Cash added successfully", "success")
        return redirect("/")

    return render_template("add_cash.html")

