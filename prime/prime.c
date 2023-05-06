#include <cs50.h>
#include <stdio.h>

//bool prime(int number);

int main(void)
{
    int min;
    do
    {
        min = get_int("Minimum: ");
    }
    while (min < 1);

    int max;
    do
    {
        max = get_int("Maximum: ");
    }
    while (min >= max);

    for (int i = min; i <= max; i++)
    {

        if (i == 1)
        {
             continue;
        }
        else if (i ==2 || i == 3 || i == 5 || i == 7)
        {
             printf("%i\n", i);
        }
         else if (i%2 !=0 && i%3 !=0 && i%5 !=0 && i%7 !=0)
        {
            printf("%i\n", i);
        }

    }
}

/*bool prime (int number) {
    // TODO
    if (number == 1)
    {
        return false;
    }
    else if (number ==2 || number == 3)
    {
         return true;
    }
    else if (number%2 !=0 && number%3 !=0)
    {

        return true;
    }
*/

