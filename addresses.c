// #include <stdio.h>

// int main(void)
// {
//     int n = 50;
//     printf("%i\n", n);
// }

// #include <stdio.h>

// int main(void)
// {
//     int n = 50;
//     printf("%p\n", &n);
// }

// #include <stdio.h>

// int main(void)
// {
//     int n = 50;
//     int *p = &n;
//     printf("%p\n", p);
// }


// #include <stdio.h>

// int main(void)
// {
//     int n = 50;
//     int *p = &n;
//     printf("%i\n", *p);
// }


// #include <cs50.h>
// #include <stdio.h>

// int main(void)
// {
//     string s = "HI!";
//     printf("%p\n", s);
//     printf("%p\n", &s[0]);
//     printf("%p\n", &s[1]);
//     printf("%p\n", &s[2]);
//     printf("%p\n", &s[3]);
// }

// #include <stdio.h>

// int main(void)
// {
//     char *s = "HI!";
//     printf("%s\n", s);
// }


// // Pointer Arithmetic
// // You can modify your code to accomplish the same thing in a longer form as follows:

// #include <stdio.h>

// int main(void)
// {
//     char *s = "HI!";
//     printf("%c\n", s[0]);
//     printf("%c\n", s[1]);
//     printf("%c\n", s[2]);
// }


// Notice that we are printing each character at the location of s.

// Further, you can modify your code as follows:

#include <stdio.h>

int main(void)
{
    char *s = "HI!";
    printf("%c\n", *s);
    printf("%c\n", *(s + 1));
    printf("%c\n", *(s + 2));
}