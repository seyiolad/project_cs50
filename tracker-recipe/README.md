# Tracker Recipe
#### Video Demo:  <(https://youtu.be/dW88cBNHQ_E)>
#### Description:
The Tracker Recipe is a web application designed to help users search, save, and share their favorite recipes. It is built using Flask, a Python web framework, and utilizes the Spoonacular API for recipe search functionality. The application also includes user authentication and authorization features, allowing users to create accounts, save their favorite recipes, and share them with friends and family.

## Installation

To run the Tracker Recipe application, you will need to have Python 3.x installed on your machine. Once you have Python installed, you can clone the repository and install the required dependencies by running the following commands in your terminal:

```
git clone https://github.com/code50/99031388/tree/main/tracker-recipe.git
cd tracker-recipe
pip install -r requirements.txt
```

Once all the dependencies have been installed, you can run the Flask application using the following command:

```
export API_KEY=<your_spoonacular_api_key>
python app.py
```

Note that you need to replace `<your_spoonacular_api_key>` with your own Spoonacular API key. You can get your API key by signing up for a free account at the [Spoonacular API website](https://spoonacular.com/food-api/).

## File Structure

The Tracker Recipe application includes the following files and directories:
```
.
├── README.md
├── app.py
├── helpers.py
├── requirements.txt
├── recipe.db
├── templates
│   ├── add_myrecipes.html
│   ├── add_recipe.html
│   ├── apology.html
│   ├── change_password.html
│   ├── delete_recipe.html
│   ├── edit_recipe.html
|   ├── index.html
|   ├── layout.html
|   ├── login.html
|   ├── profile.html
│   ├── recipe_details.html
|   ├── recipe_share.html
|   ├── recipes.html
│   ├── register.html
|   ├── search.html
│   ├── Share_with_friends.html
│   ├── share.html
│   ├── shopping_list_ingredients.html
│   ├── shopping_list.html
│   ├── view_all_recipes.html
│   └── view_myrecipes.html
└── static
    ├── styles.css
    ├── profile-back.jpg
    └── welcome.jpg
```

- `README.md`:  The readme file that contains the documentation for the project.
- `app.py`: The main Flask application file containing the routes and logic for the application.
- `helpers.py`: A helper file containing functions for querying the Spoonacular API and interacting with the SQLite database.
- `requirements.txt`: A list of Python dependencies required by the application.
- `recipe.db`: An SQLite database containing tables for users, my_recipes, and recipes.
- `templates/`: A directory containing HTML templates for the application.
- `static/`: A directory containing static files (e.g. CSS and image files) for the application.

## Usage

The Home page of the Recipe App displays a `Recipe Search` button and a `Show Me More` button. The `Recipe Search` button when clicked presents a serach bar where users can enter one or more ingredients to search for recipes using the Spoonacular API. Users can also select their dietary requirements, such as vegetarian, vegan, gluten-free, and more. Once the search query is submitted, the application returns a list of recipes that match the search criteria.

Once you have found a recipe that you like, you can click on the recipe card to view more details about the recipe. From the recipe details page, you can choose to add the recipe to your list of favorite recipes or go back to search result to choose another recipe card.

To add a recipe to your list of favorite recipes, you will need to create an account and log in. Once you are logged in, you can access your list of favorite recipes by clicking on the `Recipes` link in the navigation bar. From there, you can add, edit, share and delete your favorite recipes.

The `Add Recipe` sub menu under `Recipe` link in the navigation bar allows users to add their own special and customized recipe and their details. Once added, it can be viewed by clicking on `My Recipes` under the  `View` menu.  The `View` menu also allows users to check their added online recipes gotten from Spoonacular site by clicking on `My Online Recipes`. Both the users special recipes and the online ones can be viewed together by  clicking on `All Recipes`.

If you would like to share a recipe with friends and family, you can do so by clicking on the `Share` button. This will take you to a page where you can enter the email addresses of the people you would like to share the recipe with. You will be asked to enter the recipe ID to bring up the recipe. The application will then send an email to the recipients you choose.

The Tracker Recipe application also includes a shopping list feature, which allows you to generate a list of ingredients for one or more recipes. To use this feature, simply click on the `Shopping List` button on the navigation bar. You can then access your shopping list by clicking on the `Getting Ingredients` button after checking/selecting the recipe(s) you want to want a shopping list for.

The Recipe App uses a SQLite database to store user information and saved recipes. The database consists of three tables: `users`, `my_recipes`, and `recipes`. The `users` table stores user information such as email, password, and username. The `my_recipes` table stores the recipes that users have saved to their account. The `recipes` table stores information about all the recipes that are available in the application.

Overall, the Tracker Recipe application provides a user-friendly interface for searching, saving, and sharing recipes. Its integration with the Spoonacular API and use of a SQLite database make it a robust and versatile tool for home cooks and food enthusiasts alike. With this app, users can easily find and save their favorite recipes, share them with friends and family, and even generate shopping lists based on the ingredients needed for their selected recipes.

As the application is built using Flask, Python, html, JavaScript and CSS it can be easily customized and extended to fit the specific needs of each user. Additionally, the use of Flask makes it easy to deploy the application on various platforms and servers, making it accessible to a wide range of users.

To get started with the Tracker Recipe application, users can download the repository and install the required dependencies using the `requirements.txt` file. Once installed, they can run the `app.py` file to launch the application on their local machine.
So why wait? Download the Tracker Recipe app today and start exploring all the amazing recipes and cooking tips that it has to offer. Whether you're looking to impress your friends and family with a delicious home-cooked meal or just want to try out some new recipes, this app has everything you need to make your culinary dreams a reality. So why not give it a try today? We can't wait to see what delicious creations you come up with!


