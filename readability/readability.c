#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string letters);
int count_words(string letters);
int count_sentences(string letters);
float L = 5.2f, index = 5.2f, S = 5.2f;
int grade;


int main(void)
{
    //input the desired string text
    string letters = get_string("Text: ");

    // Calculate the average letters per every 100 words
    L = 100 * count_letters(letters) / (float)count_words(letters);

    // Calculate the average sentences per every 100 words
    S = (100 / (float)count_words(letters)) * count_sentences(letters);

    //Compute Coleman-Liau index
    index = 0.0588 * L - 0.296 * S - 15.8;

    //Compute the grade and its equivalent levels
    grade = round(index);
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }


}

//Funtion to count the numbers of letters in the inputed string
int count_letters(string text)
{
    int i, n;
    int count = 0;
    for (i = 0, n = strlen(text); i < n; i++)
    {
        //checking if lower case letters a - z are entered
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            count++;
        }
        //checking if upper case letters A - Z are entered
        else if ((toupper(text[i]) >= 'A' && toupper(text[i]) <= 'Z'))
        {
            count++;
        }

    }
    return count;
}

//Funtion to count the numbers of words in the inputed string
int count_words(string letters)
{
    int wordcount = 1;
    int i, n;

    for (i = 0, n = strlen(letters); i < n; i++)
    {
        //Condition that ensures usage of space in deterning word count
        if (letters[i] == ' ' && letters[i + 1] != ' ')
        {
            wordcount++;
        }
    }
    return wordcount;
}


//Funtion to count the numbers of sentences in the inputed string
int count_sentences(string letters)
{
    int sentcount = 0;
    int i, n;

    for (i = 0, n = strlen(letters); i < n; i++)
    {
        //Condition to ensure a sentence ends in .! and ?
        if (letters[i] == '.' || letters[i] == '!' || letters[i] == '?')
        {
            sentcount++;
        }
    }
    return sentcount;
}