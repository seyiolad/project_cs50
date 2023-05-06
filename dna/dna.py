import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py databases/large.csv sequences/5.txt")

    if not sys.argv[1].endswith(".csv"):
        sys.exit("Second argument should be a valid '.csv' file e.g. databases/large.csv")

    if not sys.argv[2].endswith(".txt"):
        sys.exit("Third argument should be a valid '.txt' file e.g. sequences/5.txt")

    # Read database file into a variable
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        csv_list = [row for row in reader]

    # Read DNA sequence file into a variable
    with open(sys.argv[2]) as seq:
        data = seq.read()

    # Find longest match of each STR in DNA sequence
    matches = {}
    for row in csv_list:
        for key, value in row.items():
            if key != "name":
                longest_str = longest_match(data, key)
                matches[key] = longest_str


# Check database for matching profiles
    for row in csv_list:
        match_count = 0
        for key, value in row.items():
            if key != "name":
                if int(value) == matches[key]:
                    match_count += 1
        if match_count == len(matches):
            print(row["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
