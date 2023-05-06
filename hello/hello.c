// #include <stdio.h>
// #include <cs50.h>

// int main(void)
// {
//     //Getting User Input
//     string answer = get_string("What's your name? ");

//     //Printing the formatted string
//     printf("hello, %s\n", answer);
// }

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>


int main(void)
{
    string text, holder;
    holder = get_string("key: ");
    text = get_string("plaintex: ");

    int modU = 65, modL = 97;
    char upperHolder[26], lowerHolder[26];
    char *final = " ";
    for (int i = 0, a = strlen(holder); i < a; i++)
    {
        // holder[i];  // Run the key indices
        upperHolder[i] = (char)modU; //Run upperCase indices
        lowerHolder[i] = (char)modL; //Run loweCase indices
        modU++, modL++;
    }

    for (int i = 0, b = strlen(text); i < b; i++)
    {
        int index;
        string temp = NULL;
        if (isalpha(text[i]) != 0)
        {
            // Check case type if lower
            if (islower(text[i]))
            {

                temp = strchr(lowerHolder, text[i]);
                index = (int)(temp - lowerHolder);
                strcat(final, &holder[index]);
                // final = final + holder[index];
                // printf("%s: \n", final);
                printf("%s\n", final);
            }
    //         else if (isupper(text[i]))
    //         {
    //             temp = strchr(upperHolder, text[i]);
    //             index = (int)(temp - upperHolder);
    //             final += holder[index];
    //         }
    //     }
    //     else
    //     {
    //        final += text[i];
    //     }
       }
    }
    // printf("final is: %s",final);
}
