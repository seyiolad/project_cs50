# # Saves names and numbers to a CSV file

# import csv

# # Get name and number
# name = input("Name: ")
# number = input("Number: ")

# # Open CSV file
# with open("phonebook.csv", "a") as file:

#     # Print to file
#     writer = csv.writer(file)
#     writer.writerow([name, number])


# Says hello to someone

import pyttsx3

engine = pyttsx3.init()
name = input("What's your name? ")
engine.say(f"hello, {name}")
engine.runAndWait()