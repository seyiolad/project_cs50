// #include <cs50.h>
// #include <ctype.h>
// #include <stdio.h>
// #include <string.h>

// int main(void)
// {
//     // Get a string
//     string s = get_string("s: ");

//     // Copy string's address
//     string t = s;

//     // Capitalize first letter in string
//     t[0] = toupper(t[0]);

//     // Print string twice
//     printf("s: %s\n", s);
//     printf("t: %s\n", t);
// }


// // Notice that strlen is used to make sure string t exists. If it does not, nothing will be copied.
// #include <cs50.h>
// #include <ctype.h>
// #include <stdio.h>
// #include <string.h>

// int main(void)
// {
//     // Get a string
//     string s = get_string("s: ");

//     // Copy string's address
//     string t = s;

//     // Capitalize first letter in string
//     if (strlen(t) > 0)
//     {
//         t[0] = toupper(t[0]);
//     }

//     // Print string twice
//     printf("s: %s\n", s);
//     printf("t: %s\n", t);
// }

// We can modify our code to create an authentic copy of our string as follows:

// #include <cs50.h>
// #include <ctype.h>
// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>

// int main(void)
// {
//     // Get a string
//     char *s = get_string("s: ");

//     // Allocate memory for another string
//     char *t = malloc(strlen(s) + 1);

//     // Copy string into memory, including '\0'
//     for (int i = 0; i <= strlen(s); i++)
//     {
//         t[i] = s[i];
//     }

//     // Capitalize copy
//     t[0] = toupper(t[0]);

//     // Print strings
//     printf("s: %s\n", s);
//     printf("t: %s\n", t);
// }



// // It turns out that there is an inefficiency in our code. Modify your code as follows:

// #include <cs50.h>
// #include <ctype.h>
// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>

// int main(void)
// {
//     // Get a string
//     char *s = get_string("s: ");

//     // Allocate memory for another string
//     char *t = malloc(strlen(s) + 1);

//     // Copy string into memory, including '\0'
//     for (int i = 0, n = strlen(s); i <= n; i++)
//     {
//         t[i] = s[i];
//     }

//     // Capitalize copy
//     t[0] = toupper(t[0]);

//     // Print strings
//     printf("s: %s\n", s);
//     printf("t: %s\n", t);
// }


// // The C Language has a built-in function to copy strings called strcpy. It can be implemented as follows:

// #include <cs50.h>
// #include <ctype.h>
// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>

// int main(void)
// {
//     // Get a string
//     char *s = get_string("s: ");

//     // Allocate memory for another string
//     char *t = malloc(strlen(s) + 1);

//     // Copy string into memory
//     strcpy(t, s);

//     // Capitalize copy
//     t[0] = toupper(t[0]);

//     // Print strings
//     printf("s: %s\n", s);
//     printf("t: %s\n", t);
// }


// Both get_string and malloc return NULL, a special value in memory, in the event that something goes wrong. You can write code that can check for this NULL condition as follows:

#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    // Get a string
    char *s = get_string("s: ");
    if (s == NULL)
    {
        return 1;
    }

    // Allocate memory for another string
    char *t = malloc(strlen(s) + 1);
    if (t == NULL)
    {
        return 1;
    }

    // Copy string into memory
    strcpy(t, s);

    // Capitalize copy
    if (strlen(t) > 0)
    {
        t[0] = toupper(t[0]);
    }

    // Print strings
    printf("s: %s\n", s);
    printf("t: %s\n", t);

    // Free memory
    free(t);
    return 0;
}