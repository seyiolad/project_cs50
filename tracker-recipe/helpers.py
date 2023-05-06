import os
import requests

import re

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def fetch_recipe(search_query):
    try:
        # Get API_KEY environment variable
        api_key = os.environ.get("API_KEY")

        # Fetch recipes from Spoonacular API
        search_query["apiKey"] = api_key


        # Encode search query for URL
        encoded_query = "&".join([f"{k}={v}" for k,v in search_query.items()])
        url = f"https://api.spoonacular.com/recipes/complexSearch?{encoded_query}"

        response = requests.get(url)

        # Check for successful response
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response as JSON
    try:
        results = response.json()["results"]
        return results
    except (requests.exceptions.HTTPError, KeyError, TypeError):
        return None


def is_valid_email(email):
    # Strip leading/trailing whitespace from email string
    email = email.strip()
    # Split email string using comma separator and remove any whitespace around the separator
    email_list = re.split(r'\s*,\s*', email)
    # Check each email address in the resulting list
    for email_addr in email_list:
        # Validate the email address using a regular expression
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email_addr):
            return False
    return True

