# import requests
# import json
# import os
# import urllib.parse


# url = "https://api.spoonacular.com/recipes/complexSearch"

# querystring = {
#     "apiKey": "8f3b7ee66ba444d98b356507a72a7777",
#     "query": "pasta",
#     "number": "5"
# }

# response = requests.request("GET", url, params=querystring) # Or response = requests.get(url, params=querystring)


# # Convert the response to a dictionary
# response_dict = json.loads(response.text)

# # for index, (key, value) in enumerate(response_dict.items()):
# #     print(index, key, value)

# list_dict = response_dict["results"]
# for each_dict in list_dict:
#     print(each_dict)
# ............................................................................

# # def lookup(symbol):
# #     """Look up quote for symbol."""

#     # Contact API
# try:
#     api_key = os.environ.get("API_KEY")
#     querystring = {
#         "apiKey": api_key,
#         "query": "pasta",
#         "number": "5"
#     }
#     url = "https://api.spoonacular.com/recipes/complexSearch"
#     response = requests.get(url, params=querystring)
#     response.raise_for_status()
# except requests.RequestException as e:
#     print("Our errror is:", e)

# # Parse response
# try:

#     # Convert the response to a dictionary
#     response_dict = json.loads(response.text)

#      # quote = response.json()
#     list_dict = response_dict["results"]
#     for each_dict in list_dict:
#         print(each_dict)
# except (KeyError, TypeError, ValueError) as e:
#         print("Our second error:", e)

# .............................................................................

# def fetch_recipe(search_query):
# import requests
# import json
# import os
# import urllib.parse

# try:
#     # Fetch recipes from Spoonacular API
#     api_key = os.environ.get("API_KEY")

#     search_query = querystring = {
#         "apiKey": api_key,
#         "query": "pasta",
#         "number": "5"
#     }

#     # Encode search query for URL
#     json_query = json.dumps(search_query)
#     encoded_query = urllib.parse.quote(json_query.encode("utf-8"))


#     url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query={encoded_query}"

#     response = requests.get(url)

#     # Check for successful response
#     response.raise_for_status()
# except requests.RequestException as e:
#     print("Our error is:", e)

# # Prse response as JSON
# try:
#     results = response.json()["results"]
#     print(results)
# except (requests.exceptions.HTTPError, KeyError, TypeError) as e:
#     print("Our second error:", e)
# .........................................................................

import requests
import os

try:
    # Fetch recipes from Spoonacular API
    api_key = os.environ.get("API_KEY")

    search_query = {
        "apiKey": api_key,
        "query": "pasta",
        "number": "5"
    }

    # Encode search query for URL
    encoded_query = "&".join([f"{k}={v}" for k,v in search_query.items()])
    url = f"https://api.spoonacular.com/recipes/complexSearch?{encoded_query}"

    response = requests.get(url)

    # Check for successful response
    response.raise_for_status()
except requests.RequestException as e:
    print("Our error is:", e)

# Parse response as JSON
try:
    results = response.json()["results"]
    print(results)
except (requests.exceptions.HTTPError, KeyError, TypeError) as e:
    print("Our second error:", e)
