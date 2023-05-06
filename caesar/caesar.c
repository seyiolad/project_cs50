#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // Initialize the key

    int k;
    if (argc == 2)
    {
        string holder = argv[1];

        //Check if the text is only positive digits
        if (only_digits(holder) == false)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
        else
        {
            // convert the string to integer
            sscanf(holder, "%i", &k);
            string text = get_string("plaintext:  ");
            printf("ciphertext: ");

            //Find the length of the string and convert accordingly to the key given (k)
            for (int i = 0, a = strlen(text); i < a; i++)
            {
                printf("%c", rotate(text[i], k));
            }
            printf("\n");
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

}


// Function that determines if the text is positive digit(s)
bool only_digits(string s)
{
    int count = 0;
    int n = strlen(s);
    for (int i = 0; i < n; i++)
    {
        if (isdigit(s[i]) && s[i] != '-') //Test if the character is a positive digit
        {
            count++;
        }
        else
        {
            return false;
        }
    }
    if (count == n)
    {
        return true;
    }
    else
    {
        return false;
    }
}


//Function that rotates the text into a ciphered one
char rotate(char c, int n)
{
    //find the ASCII value of lowercase
    int cipk, mod;
    if (isalpha(c) != 0)
    {
        //Rotate for lowercases
        cipk = c + n;
        if (islower(c))
        {
            if (cipk > 122)
            {
                mod = (cipk - 97) % 26; // computation for lowercase rotation
                return mod + 97;
            }
            else
            {
                return cipk;
            }

        }

        //Rotate for uppercases
        else if (isupper(c))
        {
            if (cipk > 90)
            {
                mod = (cipk - 65) % 26;   // computation for uppercase rotation
                return mod + 65;
            }
            else
            {
                return  cipk;
            }
        }
    }
    return c;
}