#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // prompt user to enter non-negative height between 1 and 8 inclusive
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // loop through the height
    for (int i = 0; i < height; i++)
    {
        // Print spaces()
        for (int a = height; a > i + 1; a--)
        {
            printf(" ");
        }

        // Print Hash(#) on both left and right

        int b = 0;
        while (b < 2)
        {
            for (int j = 0; j <= i ; j++)
            {
                printf("#");
            }
            b++;
            printf("  ");
        }
        printf("\n");

    }

}