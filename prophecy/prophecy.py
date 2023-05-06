import csv
from cs50 import SQL

# Open database
db = SQL("sqlite:///roster.db")

# Open CSV file
with open('students.csv', 'r') as file:
    # Create DictReader
    reader = csv.DictReader(file)

    # Iterate over the CSV file
    for row in reader:
        # Populate by inserting into student table
        # db.execute("INSERT INTO student (id, student_name) VALUES (:id, :name)", id=int(row['id']), name=row['student_name'])
        # db.execute("INSERT INTO houses (id, house) VALUES (:id, :name)", id=int(row['id']), name=row['house'])
        # db.execute("INSERT INTO house_assignment (id, head) VALUES (:id, :name)", id=int(row['id']), name=row['head'])