// #include <cs50.h>
// #include <ctype.h>
// #include <math.h>
// #include <stdio.h>
// #include <string.h>

// int convert(string input);

// int main(void)
// {
//     string input = get_string("Enter a positive integer: ");

//     for (int i = 0, n = strlen(input); i < n; i++)
//     {
//         if (!isdigit(input[i]))
//         {
//             printf("Invalid Input!\n");
//             return 1;
//         }
//     }

//     // Convert string to int
//     printf("%i\n", convert(input));
// }

// int convert(string input)
// {
//     int n = strlen(input);
//     for (i=n-1; i < n; i--)
//      input[n-1]
//     // TODO
// }

#include <stdio.h>

// Iterative function to implement `atoi()` function in C
long atoi(const char S[])
{
    long num = 0;
    int i = 0, sign = 1;

    // skip white space characters
    while (S[i] == ' ' || S[i] == '\n' || S[i] == '\t') {
        i++;
    }

    // note sign of the number
    if (S[i] == '+' || S[i] == '-')
    {
        if (S[i] == '-') {
            sign = -1;
        }
        i++;
    }

    // run till the end of the string is reached, or the
    // current character is non-numeric
    while (S[i] && (S[i] >= '0' && S[i] <= '9'))
    {
        num = num * 10 + (S[i] - '0');
        i++;
    }

    return sign * num;
}

// Implement `atoi()` function in C
int main(void)
{
    char S[] = " +17890";

    printf("%ld ", atoi(S));

    return 0;
}