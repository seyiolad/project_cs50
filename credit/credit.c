#include <cs50.h>
#include <stdio.h>

int main(void)
{
    do
    {
        long number;
        number = get_long("Number: ");
    }
    while (number < 0);
}