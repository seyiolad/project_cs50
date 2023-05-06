import os
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash

from flask_mail import Mail, Message

from helpers import apology, login_required, fetch_recipe, is_valid_email





# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_NAME"] = "session"
Session(app)

# Configure email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'Enter-Your-Email'
app.config['MAIL_PASSWORD'] = "Enter-Your-Password/App-Password"

mail = Mail(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///recipe.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 400)

        # Ensure username was submitted
        elif not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ? OR email = ?", request.form.get("username"), request.form.get("email"))


        # Ensure username or email doesn't already exist
        if len(rows) > 0:
            for row in rows:
                if row["username"] == request.form.get("username"):
                    return apology("username already exists", 400)
                elif row["email"] == request.form.get("email"):
                    return apology("email already exists", 400)

        # Insert new user into users
        db.execute("INSERT INTO users (username, email, hash) VALUES(?, ?, ?)",
               request.form.get("username"),
               request.form.get("email"),
               generate_password_hash(request.form.get("password")))

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



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


@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT * FROM my_recipes WHERE user_id = :user_id ORDER BY created_on DESC", user_id=session["user_id"])
    return render_template("index.html", rows=rows)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        # Get search query from the form data
        search_query = {
            "query": request.form.get("query"),
            "number": "50",
            "offset": "0"
        }

        # Ensure search query was submitted
        if not search_query["query"]:
            flash("Please enter a search query.")
            return redirect("/search")

        # Fetch recipes from Spoonacular API
        results = []
        while True:
            response = fetch_recipe(search_query)

            # Check for successful response
            if not response:
                flash("Unable to fetch recipes. Please try again later.")
                return redirect("/search")

            # Add fetched recipes to the results list
            results.extend(response)

            # Check if there are more recipes to fetch
            if len(response) < 100:
                break

            # Update the offset to fetch the next set of recipes
            search_query["offset"] = str(int(search_query["offset"]) + 100)

        # get session for the results
        session['search_results'] = results
        return redirect(url_for('search'))

    # Render search results template with recipes
    results = session.get('search_results')
    return render_template("search.html", results=results)




@app.route("/recipes")
@login_required
def recipes():

    # Query database for user's saved recipes
    user_id = session["user_id"]
    recipes = db.execute("SELECT * FROM my_recipes WHERE user_id = :user_id ORDER BY created_on DESC", user_id=user_id)

    # Render recipes template with saved recipes
    return render_template("recipes.html", recipes=recipes)


@app.route("/recipe/<int:result_id>")
@login_required
def recipe_details(result_id):

    # Fetch recipe details from Spoonacular API
    try:
        # Get API_KEY environment variable
        api_key = os.environ.get("API_KEY")

        # Build the URL for the recipe details endpoint
        url = f"https://api.spoonacular.com/recipes/{result_id}/information?includeNutrition=false&apiKey={api_key}"

        # Send the request to the API and get the response
        response = requests.get(url)

        # Raise an error if the response status code is not 200
        response.raise_for_status()

        # Extract the recipe details from the response JSON
        recipe_details = response.json()

        # Render the recipe details template with the recipe details
        return render_template("recipe_details.html", recipe=recipe_details)

    except requests.RequestException:
        # If there was an error with the request, apologize to the user
        return apology("Unable to fetch recipe details. Please try again later.")



@app.route("/add_recipe/<int:recipe_id>", methods=["POST", "GET"])
@login_required
def add_recipe(recipe_id):
    if request.method == "POST":
        # Get recipe details from form
        title = request.form.get("title")
        image = request.form.get("image")
        sourceUrl = request.form.get("sourceUrl")
        servings = request.form.get("servings")
        instructions = request.form.get("instructions")
        ingredients = request.form.get("ingredients")

        # Check if the recipe_id already exists in the user's recipe book
        user_id = session["user_id"]
        recipe_exists = db.execute("SELECT * FROM my_recipes WHERE user_id = :user_id AND recipe_id = :recipe_id", user_id=user_id, recipe_id=recipe_id)
        if recipe_exists:
            flash("You already have this recipe in your profile.")
            return redirect(url_for('recipe_details',result_id=recipe_id))

        # Insert recipe into the user's recipe table
        try:
            db.execute("""
                INSERT INTO my_recipes (user_id, title, image, recipe_id, sourceUrl, servings, instructions, ingredients)
                VALUES (:user_id, :title, :image, :recipe_id, :sourceUrl, :servings, :instructions, :ingredients)
            """, user_id=user_id, title=title, image=image, recipe_id=recipe_id, sourceUrl=sourceUrl, servings=servings, instructions=instructions, ingredients=ingredients)

            flash("Recipe successfully added!", "success")
            # Redirect to the recipe details page
            return redirect(url_for('recipe_details',result_id=recipe_id))

        except:
            flash("An error occurred while adding the recipe.")
            return redirect(url_for('recipe_details',result_id=recipe_id))



@app.route("/profile")
@login_required
def profile():
    # Render profile template
    return render_template("profile.html")



@app.route("/add_myrecipe", methods=["GET","POST"])
@login_required
def add_myrecipe():
    if request.method == "POST":
        # Get recipe details from form
        title = request.form.get("title")
        recipe_id = request.form.get("recipe_id")
        image = request.form.get("image")
        sourceUrl = request.form.get("sourceUrl")
        servings = request.form.get("servings")
        instructions = request.form.get("instructions")
        ingredients = request.form.get("ingredients")

        # Check if the recipe_id already exists in the user's recipe book
        user_id = session["user_id"]
        recipe_exists = db.execute("SELECT * FROM recipes WHERE user_id = :user_id AND recipe_id = :recipe_id", user_id=user_id, recipe_id=recipe_id)
        if recipe_exists:
            flash("You already have this recipe in your profile.")
            return redirect(url_for('add_myrecipe'))

        # Insert recipe into the user's recipe table
        try:
            db.execute("""
                INSERT INTO recipes (user_id, title, image, recipe_id, sourceUrl, servings, instructions, ingredients)
                VALUES (:user_id, :title, :image, :recipe_id, :sourceUrl, :servings, :instructions, :ingredients)
            """, user_id=user_id, title=title, image=image, recipe_id=recipe_id, sourceUrl=sourceUrl, servings=servings, instructions=instructions, ingredients=ingredients)

            flash("Recipe successfully added!", "success")
            # Redirect to the recipe details page
            return redirect(url_for('add_myrecipe'))

        except:

            flash("An error occurred while adding the recipe.")
            return redirect(url_for('add_myrecipe'))
    return render_template("/add_myrecipe.html")




@app.route("/view_myrecipes")
@login_required
def view_myrecipes():

    # Query database for user's saved recipes
    user_id = session["user_id"]
    recipes = db.execute("SELECT * FROM recipes WHERE user_id = :user_id ORDER BY created_on DESC", user_id=user_id)


    # Render recipes template with saved recipes
    return render_template("view_myrecipes.html", recipes=recipes)



@app.route("/view_all_recipes")
@login_required
def view_all_recipes():

    # Query database for user's saved recipes
    user_id=session["user_id"]
    recipes = db.execute('''
    SELECT r.title, r.recipe_id, r.created_on, r.ingredients, r.instructions, r.image, r.sourceUrl
    FROM recipes r
    JOIN my_recipes mr ON r.user_id = ?
    UNION
    SELECT mr.title, mr.recipe_id, mr.created_on, mr.ingredients, mr.instructions, mr.image, mr.sourceUrl
    FROM recipes r
    JOIN my_recipes mr ON mr.user_id = ?
    ORDER BY r.created_on DESC, mr.created_on DESC; ''', user_id, user_id)


    # Render recipes template with saved recipes
    return render_template("view_all_recipes.html", recipes=recipes)



@app.route('/edit_recipe', methods=['GET', 'POST'])
@login_required
def edit_recipe():
    recipe = None
    table = None

    if request.method == 'POST':
        recipe_id = int(request.form.get("recipe_id"))

        # Query database for recipes
        recipe1 = db.execute("SELECT * FROM recipes WHERE recipe_id = :recipe_id AND user_id = :user_id", recipe_id=recipe_id, user_id=session["user_id"])

        # Query database for my_recipes
        recipe2 = db.execute("SELECT * FROM my_recipes WHERE recipe_id = :recipe_id AND user_id = :user_id", recipe_id=recipe_id, user_id=session["user_id"])

        if recipe1 is None and recipe2 is None:
            flash("Recipe not found.")
            return redirect("/edit_recipe")

        if recipe1:
            recipe = recipe1[0]
            table = "recipes"
        elif recipe2:
            recipe = recipe2[0]
            table = "my_recipes"

        if recipe:
            return render_template('edit_recipe.html', recipe=recipe,table=table)
        else:
            flash('Recipe not found')
            return redirect('/edit_recipe')

    return render_template('edit_recipe.html')



@app.route('/update_recipe/<table>', methods=['POST'])
@login_required
def update_recipe(table):
  # handle recipe update

    try:
        # Update recipe in database
        db.execute(f"""UPDATE {table} SET title = :title, image = :image, sourceUrl = :sourceUrl, ingredients = :ingredients,
            instructions = :instructions, servings = :servings WHERE recipe_id = :recipe_id""",
            title=request.form['title'], image=request.form['image'], sourceUrl=request.form['sourceUrl'],
            ingredients=request.form['ingredients'], instructions=request.form['instructions'],
            servings=request.form['servings'], recipe_id=int(request.form["recipe_id"]))

        flash('Recipe updated successfully')
        return redirect('/edit_recipe')

    except Exception:
        flash('Recipe update failed')
        return redirect('/edit_recipe')


@app.route("/delete_recipe", methods=["GET","POST"])
@login_required
def delete_recipe():
    recipe = None
    table = None

    if request.method == 'POST':
        recipe_id = int(request.form.get("recipe_id"))

        # Query database for recipes
        recipe1 = db.execute("SELECT * FROM recipes WHERE recipe_id = :recipe_id AND user_id = :user_id", recipe_id=recipe_id, user_id=session["user_id"])

        # Query database for my_recipes
        recipe2 = db.execute("SELECT * FROM my_recipes WHERE recipe_id = :recipe_id AND user_id = :user_id", recipe_id=recipe_id, user_id=session["user_id"])

        if recipe1 is None and recipe2 is None:
            flash("Recipe not found.")
            return redirect("/delete_recipe")

        if recipe1:
            recipe = recipe1[0]
            table = "recipes"
        elif recipe2:
            recipe = recipe2[0]
            table = "my_recipes"

        if recipe:
            return render_template('delete_recipe.html', recipe=recipe,table=table)
        else:
            flash('Recipe not found')
            return redirect('/delete_recipe')

    return render_template('delete_recipe.html')




@app.route('/update_delete_recipe/<table>/<recipe_id>', methods=['POST'])
@login_required
def update_delete_recipe(table, recipe_id):
    try:
        # Delete recipe from database
        db.execute(f"DELETE FROM {table} WHERE recipe_id = :recipe_id AND user_id = :user_id", recipe_id=recipe_id, user_id=session["user_id"])
        if table == "recipes":
            flash("Recipe deleted successfully.")
            return redirect("/view_myrecipes")
        else:
            flash("Recipe deleted successfully.")
            return redirect("/recipes")
    except Exception:
        flash("Delete failed!")
    return redirect("/delete_recipe")



@app.route('/recipe_share', methods=['GET', 'POST'])
@login_required
def recipe_share():
    recipe = None
    table = None

    if request.method == 'POST':
        recipe_id = int(request.form.get("recipe_id"))

        # Query database for recipes
        recipe1 = db.execute("SELECT * FROM recipes WHERE recipe_id = :recipe_id AND user_id = :user_id", recipe_id=recipe_id, user_id=session["user_id"])

        # Query database for my_recipes
        recipe2 = db.execute("SELECT * FROM my_recipes WHERE recipe_id = :recipe_id AND user_id = :user_id", recipe_id=recipe_id, user_id=session["user_id"])

        if recipe1 is None and recipe2 is None:
            flash("Recipe not found.")
            return redirect("/recipe_share")

        if recipe1:
            recipe = recipe1[0]
            table = "recipes"
        elif recipe2:
            recipe = recipe2[0]
            table = "my_recipes"

        if recipe:
            return render_template('recipe_share.html', recipe=recipe, table=table)
        else:
            flash('Recipe not found')
            return redirect('/recipe_share')

    return render_template('recipe_share.html')



@app.route('/share_with_friends/<int:recipe_id><table>', methods=['POST', 'GET'])
@login_required
def share_with_friends(recipe_id, table):
    if request.method == 'POST':
        # Get recipe information from the database
        recipe = db.execute(f"SELECT * FROM {table} WHERE recipe_id = :recipe_id AND user_id = :user_id", recipe_id=recipe_id, user_id=session["user_id"])

        recipe = recipe[0]

        title = recipe["title"]
        ingredients = recipe["ingredients"]
        instructions = recipe["instructions"]

        if not recipe:
            flash("Recipe not found!")
            return redirect(url_for("recipe_share"))


        # Get form data
        if request.form.get('emails'):
            emails = request.form.get('emails')

            email_list = emails.split(',')
            message = request.form.get('message')

            # send mail to each recipient
            for email in email_list:

                # check if email is valid
                if not is_valid_email(email):
                    flash(f'Invalid email address: {email}')
                    return redirect(url_for('share_with_friends', recipe_id=recipe_id, table=table))

                msg = Message('Test Email',
                            sender='Enter-Your-Email',
                            recipients=[email.strip()])
                msg.body = f"Hi,\n\n{message}\n\nHere's a recipe I wanted to share with you:\n\nTitle: {title}\n\nIngredients: {ingredients}\n\nInstructions: {instructions}\n\nEnjoy cooking!\n\n\n"
                mail.send(msg)

            flash("Email sent successfully!")
            return redirect(url_for('share_with_friends', recipe_id=recipe_id, table=table))
        else:
            emails = []
            return render_template('share_with_friends.html', recipe_id=recipe_id, table=table)

    return render_template('share_with_friends.html', recipe_id=recipe_id, table=table)


@app.route('/shopping_list', methods=['GET', 'POST'])
@login_required
def shopping_list():
    # Query database for user's saved recipes
    user_id=session["user_id"]
    recipes = db.execute('''
    SELECT r.title, r.recipe_id, r.created_on, r.ingredients, r.instructions, r.image, r.sourceUrl
    FROM recipes r
    JOIN my_recipes mr ON r.user_id = ?
    UNION
    SELECT mr.title, mr.recipe_id, mr.created_on, mr.ingredients, mr.instructions, mr.image, mr.sourceUrl
    FROM recipes r
    JOIN my_recipes mr ON mr.user_id = ?
    ORDER BY r.created_on DESC, mr.created_on DESC; ''', user_id, user_id)

    # Render recipes template with saved recipes
    return render_template('shopping_list.html', recipes=recipes)



@app.route('/shopping_list/ingredients', methods=['POST'])
def shopping_list_ingredients():
    recipe_ids = request.form.getlist('recipe_ids')

    if recipe_ids == []:
        flash("Please Check/Select at least a recipe! ")
        return redirect("/shopping_list")

    recipes = []
    for recipe_id in recipe_ids:
        # Query database for recipes
        recipe1 = db.execute("SELECT * FROM recipes WHERE recipe_id = :recipe_id AND user_id = :user_id", recipe_id=recipe_id, user_id=session["user_id"])

        # Query database for my_recipes
        recipe2 = db.execute("SELECT * FROM my_recipes WHERE recipe_id = :recipe_id AND user_id = :user_id", recipe_id=recipe_id, user_id=session["user_id"])

        if recipe1 is None and recipe2 is None:
            flash("Recipes not checked/selected.")
            return redirect("/shopping_list")

        if recipe1:
            recipe = recipe1[0]

        elif recipe2:
            recipe = recipe2[0]

        recipes.append(recipe)


    return render_template('shopping_list_ingredients.html', recipes=recipes)


