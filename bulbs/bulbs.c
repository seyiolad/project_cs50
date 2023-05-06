#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    int s[BITS_IN_BYTE];

    // prompt user for string imput
    string text = get_string("Message: ");

    //Get the length of the inputed string
    int n = strlen(text);

    int asci[n]; //Create an integer array to store each converted character of the string
    int temp;    // initialize a temporaty storage to hold the converted character

    //Loop throgh the string to convert each character to its integer equivalent
    for (int i = 0; i < n; i++)
    {
        asci[i] = text[i];

        //convert to binary and store in 8bits
        for (int a = BITS_IN_BYTE - 1; a >= 0 ; a--)
        {
            temp = asci[i];
            asci[i] = asci[i] / 2;
            if (temp % 2 == 0)
            {
                s[a] = 0;
            }
            else
            {
                s[a] = 1;
            }
        }
        for (int b = 0; b < BITS_IN_BYTE; b++)
        {
            print_bulb(s[b]);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
