import math


def count_letters(letters):
    count = 0
    for char in letters:
        if char.isalpha():
            count += 1
    return count


def count_words(letters):
    wordcount = 1
    for char in letters:
        if char.isspace():
            wordcount += 1
    return wordcount


def count_sentences(letters):
    sentcount = 0
    for char in letters:
        if char in ['.', '!', '?']:
            sentcount += 1
    return sentcount


# input the desired string text
letters = input("Text: ")

# Calculate the average letters per every 100 words
L = 100 * count_letters(letters) / count_words(letters)

# Calculate the average sentences per every 100 words
S = 100 * count_sentences(letters) / count_words(letters)

# Compute Coleman-Liau index
index = 0.0588 * L - 0.296 * S - 15.8

# Compute the grade and its equivalent levels
grade = round(index)

if grade >= 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print(f"Grade {grade}")
