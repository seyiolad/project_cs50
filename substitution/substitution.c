#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>


char rotate(char c, string n, char upp[26], char low[26]);   // declaring funtion to rotate the plaintex
char key(string s); // declaring function for key validation


int main(int argc, string argv[])
{
    string text, holder;
    if (argc == 2)
    {
        char substitution = key(holder = argv[1]);
        if (substitution == 'a')
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
        else if (substitution == 'b')
        {
            printf("key must all be alphabets\n");
            return 1;
        }
        else if (substitution == 'c')
        {
            int modU = 65, modL = 97;
            char upperHolder[26], lowerHolder[26];
            // string final = NULL;
            //Store indices for the uppercases and lowercases
            for (int i = 0; i < 26; i++)
            {
                // holder[i];  // Run the key indices
                upperHolder[i] = (char)modU; //Run upperCase indices
                lowerHolder[i] = (char)modL; //Run loweCase indices
                modU++, modL++;
            }


            // Enter the plaintext to be ciphered
            text = get_string("plaintext:  ");
            printf("ciphertext: ");


            // Initiating the conversion process
            for (int i = 0, b = strlen(text); i < b; i++)
            {
                printf("%c", rotate(text[i], holder, lowerHolder, upperHolder));
            }
            printf("\n");
            return 0;
        }
        else if (substitution == 'd')
        {
            printf("Key cannot contain duplicates\n");
            return 1;
        }

    }
    printf("Usage: ./substitution key\n");
    return 1;
}


// function that checks if the substitution key is valid or not
char key(string s)
{
    int i, n = strlen(s);
    char temp = ' ';
    if (n == 26)
    {
        for (i = 0; i < n; i++)
        {
            if (isalpha(s[i]) != 0)
            {
                for (int j = i + 1; j < n; j++) // Testing for duplicates
                {
                    if (s[i] == s[j])
                    {
                        temp = 'd';  // Testing for duplicate
                        return temp;
                    }
                }

                if (i == 25)
                {
                    temp = 'c';  // All key characters are alphabets
                    break;
                }
            }
            else
            {
                temp = 'b'; //key must all be alphabets
                break;
            }
        }
        return temp;
    }
    else
    {
        temp = 'a';
        return temp;  // Key must contain 26 characters
    }
}


// Function that rotates the plaintext into ciphertext
char rotate(char text, string holder, char lowerHolder[26], char upperHolder[26])
{

    int index;
    string temp;
    if (isalpha(text) != 0)
    {
        // Check case type if lower
        if (islower(text))
        {
            temp = strchr(lowerHolder, text);
            index = (int)(temp - lowerHolder);
            return tolower(holder[index]);
        }
        else if (isupper(text))
        {
            temp = strchr(upperHolder, text);
            index = (int)(temp - upperHolder);
            return toupper(holder[index]);
        }
    }
    return text;
}