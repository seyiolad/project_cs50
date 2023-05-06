def get_cents():
    # Enter a non-negative number as cent
    while True:
        try:
            store = float(input("Change owed: "))
            if store >= 0:
                break
        except ValueError:
            continue
    return int(store * 100)


def calculate_quarters(cents):
    # Calculate the number of quarters to give
    quarters = cents // 25
    return quarters


def calculate_dimes(cents):
    # Calculate the number of dimes to give
    dimes = cents // 10
    return dimes


def calculate_nickels(cents):
    # Calculate the number of nickels to give
    nickels = cents // 5
    return nickels


def calculate_pennies(cents):
    # Calculate the number of pennies to give
    pennies = cents % 5
    return pennies


# Ask how many cents the customer is owed
cents = get_cents()

# Calculate the number of quarters to give the customer
quarters = calculate_quarters(cents)
cents -= quarters * 25

# Calculate the number of dimes to give the customer
dimes = calculate_dimes(cents)
cents -= dimes * 10

# Calculate the number of nickels to give the customer
nickels = calculate_nickels(cents)
cents -= nickels * 5

# Calculate the number of pennies to give the customer
pennies = calculate_pennies(cents)

# Sum coins
coins = quarters + dimes + nickels + pennies

# Print total number of coins to give the customer
print(coins)
