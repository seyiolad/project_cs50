# # Prints all favorites in CSV using csv.reader

# import csv

# # Open CSV file
# with open("favorites.csv", "r") as file:

#     # Create reader
#     reader = csv.reader(file)

#     # Skip header row
#     next(reader)

#     # Iterate over CSV file, printing each favorite
#     for row in reader:
#         print(row[1])


# # Prints all favorites in CSV using csv.DictReader
# # Python also allows you to index by the keys of a list. Modify your code as follows:

# import csv

# # Open CSV file
# with open("favorites.csv", "r") as file:

#     # Create DictReader
#     reader = csv.DictReader(file)

#     # Iterate over CSV file, printing each favorite
#     for row in reader:
#         print(row["language"])



# # To count the number of favorite languages expressed in the csv file, we can do the following:
# # Counts favorites using variables

# import csv

# # Open CSV file
# with open("favorites.csv", "r") as file:

#     # Create DictReader
#     reader = csv.DictReader(file)

#     # Counts
#     javascript,java, c, python = 0, 0, 0, 0

#     # Iterate over CSV file, counting favorites
#     for row in reader:
#         favorite = row["language"]
#         if favorite == "JavaScript":
#             javascript += 1
#         elif favorite == "C++":
#             c += 1
#         elif favorite == "Java":
#             java += 1
#         elif favorite == "Python":
#             python += 1

# # Print counts
# print(f"JavaScript: {javascript}")
# print(f"C++: {c}")
# print(f"Java: {java}")
# print(f"Python: {python}")


# # Python allows us to use a dictionary to count the counts
# # of each language. Consider the following improvement upon our code:


# # Counts favorites using dictionary

# import csv

# # Open CSV file
# with open("favorites.csv", "r") as file:

#     # Create DictReader
#     reader = csv.DictReader(file)

#     # Counts
#     counts = {}

#     # Iterate over CSV file, counting favorites
#     for row in reader:
#         favorite = row["language"]
#         if favorite in counts:
#             counts[favorite] += 1
#         else:
#             counts[favorite] = 1

# # Print counts
# for favorite in counts:
#     print(f"{favorite}: {counts[favorite]}")


# # Python also allows sorting counts. Improve your code as follows:
# # Sorts favorites by key

# import csv

# # Open CSV file
# with open("favorites.csv", "r") as file:

#     # Create DictReader
#     reader = csv.DictReader(file)

#     # Counts
#     counts = {}

#     # Iterate over CSV file, counting favorites
#     for row in reader:
#         favorite = row["language"]
#         if favorite in counts:
#             counts[favorite] += 1
#         else:
#             counts[favorite] = 1

# # Print counts
# for favorite in sorted(counts):
#     print(f"{favorite}: {counts[favorite]}")


# # Sorts favorites by value

# import csv

# # Open CSV file
# with open("favorites.csv", "r") as file:

#     # Create DictReader
#     reader = csv.DictReader(file)

#     # Counts
#     counts = {}

#     # Iterate over CSV file, counting favorites
#     for row in reader:
#         favorite = row["language"]
#         if favorite in counts:
#             counts[favorite] += 1
#         else:
#             counts[favorite] = 1

# def get_value(language):
#     return counts[language]

# # Print counts
# for favorite in sorted(counts, key=get_value, reverse=True):
#     print(f"{favorite}: {counts[favorite]}")


# # Python has a unique ability that we have not seen to date: It allows for
# # the utilization of anonymous or lambda functions. These functions can be
# # utilized when you want to not bother creating an entirely different function.
# # Notice the following modification:



# # Sorts favorites by value using lambda function

# import csv

# # Open CSV file
# with open("favorites.csv", "r") as file:

#     # Create DictReader
#     reader = csv.DictReader(file)

#     # Counts
#     counts = {}

#     # Iterate over CSV file, counting favorites
#     for row in reader:
#         favorite = row["language"]
#         if favorite in counts:
#             counts[favorite] += 1
#         else:
#             counts[favorite] = 1

# # Print counts
# for favorite in sorted(counts, key=lambda language: counts[language], reverse=True):
#     print(f"{favorite}: {counts[favorite]}")



# # We can change the column we are examining, focusing on our favorite problem instead:
# # Favorite problem instead of favorite language

# import csv

# # Open CSV file
# with open("favorites.csv", "r") as file:

#     # Create DictReader
#     reader = csv.DictReader(file)

#     # Counts
#     counts = {}

#     # Iterate over CSV file, counting favorites
#     for row in reader:
#         favorite = row["problem"]
#         if favorite in counts:
#             counts[favorite] += 1
#         else:
#             counts[favorite] = 1

# # Print counts
# for favorite in sorted(counts, key=lambda problem: counts[problem], reverse=True):
#     print(f"{favorite}: {counts[favorite]}")



# # What if we wanted to allow users to provide input directly in the terminal? We can modify our code,
# # leveraging our previous knowledge about user input:

# # Favorite problem instead of favorite language

# import csv

# # Open CSV file
# with open("favorites.csv", "r") as file:

#     # Create DictReader
#     reader = csv.DictReader(file)

#     # Counts
#     counts = {}

#     # Iterate over CSV file, counting favorites
#     for row in reader:
#         favorite = row["language"]
#         if favorite in counts:
#             counts[favorite] += 1
#         else:
#             counts[favorite] = 1

# # Print count
# favorite = input("Favorite: ")
# favorite = favorite.capitalize()
# if favorite in counts:
#     print(f"{favorite}: {counts[favorite]}")


# Searches database popularity of a problem

import csv

from cs50 import SQL

# Open database
db = SQL("sqlite:///favorites.db")

# Prompt user for favorite
favorite = input("Favorite: ")

# Search for title
rows = db.execute("SELECT COUNT(*) FROM favorites WHERE problem LIKE ?", "%" + favorite + "%")



# # Get first (and only) row
row = rows[0]

