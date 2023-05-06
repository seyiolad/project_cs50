# # TODO
# # A message to request for a name and print the message
# message = input("What is your name?\n")
# print(f'hello, {message}')



list_of_dicts = [
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25},
    {'name': 'Charlie', 'age': 40}
]

# Iterate over each dictionary in the list
for i, dictionary in enumerate(list_of_dicts):
    print(f"Dictionary {i+1}:")
    # Iterate over the keys and values in the current dictionary
    for key, value in dictionary.items():
        print(f"\t{key}: {value}")
