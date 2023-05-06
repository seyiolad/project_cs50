// Write a function to replace vowels with numbers
// Get practice with strings
// Get practice with command line
// Get practice with switch

#include <cs50.h>
#include <stdio.h>

string replace(string input);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Missing command-line argument\n");
        return 1;
    }
    printf("%s\n", replace(argv[1]));
    return 0;
}





// The replace function that deciphers the entered string
string replace(string input)
{
    int i = 0;
    char output = ' ';
    while (input[i] != '\0')
    {
        output = input[i];
        switch (output)
        {
            case  'a':
                output = '6';
                break;

            case  'e':
                output = '3';
                break;

            case 'i':
                output = '1';
                break;

            case 'o':
                output = '0';
                break;
        }
        input[i] = output;
        i++;

    }
    return input;
}