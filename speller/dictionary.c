// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 65536;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to obtain a hash value
    unsigned int hash_value = hash(word);

    // Access the linked list at that index in the hash table
    node *cursor = table[hash_value];

    // Traverse the linked list, looking for the word
    while (cursor != NULL)
    {
        // Compare the word to the current node's word
        if (strcasecmp(word, cursor->word) == 0)
        {
            // The word is in the dictionary
            return true;
        }

        // Move on to the next node in the linked list
        cursor = cursor->next;
    }

    // The word is not in the dictionary
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // This is a simple hash function that just adds up the ASCII values of the characters
    // in the word and takes the remainder when divided by the number of buckets in the hash table
    unsigned int sum = 0;

    for (int i = 0; word[i] != '\0'; i++)
    {
        sum += toupper(word[i]);
    }

    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *file = fopen(dictionary, "r");

    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", dictionary);
        return false;
    }

    // Read words from the dictionary file and add them to the hash table
    char word[LENGTH + 1];

    while (fscanf(file, "%s", word) != EOF)
    {
        // Create a new node for the word
        node *new_node = malloc(sizeof(node));

        if (new_node == NULL)
        {
            fprintf(stderr, "Could not allocate memory for node.\n");
            return false;
        }

        strcpy(new_node->word, word);

        // Hash the word to obtain a hash value
        unsigned int hash_value = hash(word);

        // Add the new node to the beginning of the linked list at that index in the hash table
        new_node->next = table[hash_value];
        table[hash_value] = new_node;
    }

    // Close the dictionary file
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Keep track of the number of words
    unsigned int word_count = 0;

    // Traverse the hash table, counting the number of nodes
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            word_count++;
            cursor = cursor->next;
        }
    }

    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false

bool unload(void)
{
    // Iterate through each bucket of the hash table
    for (int i = 0; i < N; i++)
    {
        // Free all nodes in the current bucket
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }

    // Set the hash table to NULL to indicate that it is now empty
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Indicate that the unload was successful
    return true;
}





