# prompt user to enter non-negative height between 1 and 8 inclusive
while True:
    try:
        height = int(input("Height: "))
        if 1 <= height <= 8:
            break
    except ValueError:
        print("Enter non-negative height between 1 and 8 inclusive")

# loop through the height
for i in range(height):

    # Print Space
    for a in range(height, i + 1, -1):
        print(" ", end='')

    # Print Hash(#)
    for j in range(i + 1):
        print("#", end='')

    print()
