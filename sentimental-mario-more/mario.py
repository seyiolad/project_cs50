# prompt user to enter non-negative height between 1 and 8 inclusive
while True:
    try:
        height = int(input("Height: "))
        if 1 <= height <= 8:
            break
    except ValueError:
        print("Non-negative height between 1 and 8 inclusive")

# loop through the height
for i in range(height):
    # Print spaces
    for a in range(height, i + 1, -1):
        print(" ", end='')

    # Print Hash(#) on both left and right
    b = 0
    while b < 2:
        for j in range(i + 1):
            print("#", end='')
        b += 1
        print(" ", end='')

    print()
