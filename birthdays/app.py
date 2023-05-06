import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from datetime import timedelta




# Configure application
app = Flask(__name__)

# Ensure flash messages disappears after some seconds
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5)

# Set the secret key for the application
app.secret_key = '1234'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Check if any of the fields are empty
        if not name or not month or not day:
            flash("Please provide a complete entry.")
            return redirect("/")

        # Check if the name already exists in the database
        if db.execute("SELECT * FROM birthdays WHERE LOWER(name) = LOWER(?) AND month = ? AND day = ?", name, month, day):
            flash("This birthday already exists.")
            return redirect("/")

        # Insert the new entry into the database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)
        flash("Birthday added!")
        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)



@app.route('/delete/<int:birthday_id>')
def delete_birthday(birthday_id):
    db.execute('DELETE FROM birthdays WHERE id = ?', birthday_id)
    flash('Birthday deleted!')
    return redirect('/')


