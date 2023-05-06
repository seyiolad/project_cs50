// #include <cs50.h>
// #include <stdio.h>

// int main(void)
// {
//     // An array of integers
//     int numbers[] = {20, 500, 10, 5, 100, 1, 50};

//     // Search for number
//     int n = get_int("Number: ");
//     for (int i = 0; i < 7; i++)
//     {
//         if (numbers[i] == n)
//         {
//             printf("Found\n");
//             return 0;
//         }
//     }
//     printf("Not found\n");
//     return 1;
// }


#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // An array of strings
    string strings[] = {"battleship", "boot", "cannon", "iron", "thimble", "top hat"};

    // Search for string
    string s = get_string("String: ");
    for (int i = 0; i < 6; i++)
    {
        if (strcmp(strings[i], s) == 0)
        {
            printf("Found\n");
            return 0;
        }
    }
    printf("Not found\n");
    return 1;
}