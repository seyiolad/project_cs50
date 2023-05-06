# # Implements a registration form using a select menu

# from flask import Flask, render_template, request

# app = Flask(__name__)

# SPORTS = [
#     "Basketball",
#     "Soccer",
#     "Ultimate Frisbee"
# ]


# @app.route("/")
# def index():
#     return render_template("index.html", sports=SPORTS)


# @app.route("/register", methods=["POST"])
# def register():

#     # Validate submission
#     if not request.form.get("name") or request.form.get("sport") not in SPORTS:
#         return render_template("failure.html")

#     # Confirm registration
#     return render_template("success.html")
# .............................................................................................

# # Implements a registration form, storing registrants in a dictionary, with error messages

# from flask import Flask, redirect, render_template, request

# app = Flask(__name__)

# REGISTRANTS = {}

# SPORTS = [
#     "Basketball",
#     "Soccer",
#     "Ultimate Frisbee"
# ]


# @app.route("/")
# def index():
#     return render_template("index.html", sports=SPORTS)


# @app.route("/register", methods=["POST"])
# def register():

#     # Validate name
#     name = request.form.get("name")
#     if not name:
#         return render_template("error.html", message="Missing name")

#     # Validate sport
#     sport = request.form.get("sport")
#     if not sport:
#         return render_template("error.html", message="Missing sport")
#     if sport not in SPORTS:
#         return render_template("error.html", message="Invalid sport")

#     # Remember registrant
#     REGISTRANTS[name] = sport

#     # Confirm registration
#     return redirect("/registrants")


# @app.route("/registrants")
# def registrants():
#     return render_template("registrants.html", registrants=REGISTRANTS)
# ...............................................................................................

# Flask with SQL

# Implements a registration form, storing registrants in a SQLite database, with support for deregistration

from cs50 import SQL
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///froshims.db")

SPORTS = [
    "Basketball",
    "Soccer",
    "Ultimate Frisbee"
]


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/deregister", methods=["POST"])
def deregister():

    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    return redirect("/registrants")


@app.route("/register", methods=["POST"])
def register():

    # Validate submission
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")

    # Remember registrant
    db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", name, sport)

    # Confirm registration
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    registrants = db.execute("SELECT * FROM registrants")
    return render_template("registrants.html", registrants=registrants)
