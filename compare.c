// #include <cs50.h>
// #include <stdio.h>

// int main(void)
// {
//     // Get two strings
//     char *s = get_string("s: ");
//     char *t = get_string("t: ");

//     // Compare strings' addresses
//     if (s == t)
//     {
//         printf("Same\n");
//     }
//     else
//     {
//         printf("Different\n");
//     }
// }


// Modify your code as follows:

// #include <cs50.h>
// #include <stdio.h>

// int main(void)
// {
//     // Get two strings
//     char *s = get_string("s: ");
//     char *t = get_string("t: ");

//     // Print strings
//     printf("%s\n", s);
//     printf("%s\n", t);
// }

// You can see the locations of these two stored strings with a small modification:

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get two strings
    char *s = get_string("s: ");
    char *t = get_string("t: ");

    // Print strings' addresses
    printf("%p\n", s);
    printf("%p\n", t);
}