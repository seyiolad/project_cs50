#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s input.wav output.wav\n", argv[0]);
        return 1;
    }

    // Open input file for reading
    char *infile = argv[1];
    FILE *inptr = fopen(infile, "rb");
    if (inptr == NULL)
    {
        fprintf(stderr, "Input is not a WAV file.\n");
        return 2;
    }

    // Read header
    WAVHEADER header;
    fread(&header, sizeof(WAVHEADER), 1, inptr);

    // Use check_format to ensure WAV format
    if (!check_format(header))
    {
        fprintf(stderr, "Unsupported file format.\n");
        return 3;
    }

    // Open output file for writing
    char *outfile = argv[2];
    FILE *outptr = fopen(outfile, "wb");
    if (outptr == NULL)
    {
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // Write header to file
    fwrite(&header, sizeof(WAVHEADER), 1, outptr);

    // Use get_block_size to calculate size of block
    int block_size = get_block_size(header);

    // Write reversed audio to file
    int16_t buffer[block_size];
    while (fread(buffer, sizeof(int16_t), block_size, inptr) == block_size)
    {
        for (int i = block_size - 1; i >= 0; i--)
        {
            fwrite(&buffer[i], sizeof(int16_t), 1, outptr);
        }
    }

    // Close files
    fclose(inptr);
    fclose(outptr);

    return 0;
}

int check_format(WAVHEADER header)
{
    // Check if file is in WAV format
    if (header.chunkID[0] != 'R' || header.chunkID[1] != 'I' ||
        header.chunkID[2] != 'F' || header.chunkID[3] != 'F' ||
        header.format[0] != 'W' || header.format[1] != 'A' ||
        header.format[2] != 'V' || header.format[3] != 'E')
    {
        return 0;
    }

    // Check if audio format is PCM
    if (header.audioFormat != 1)
    {
        return 0;
    }

    // Check if number of channels is 1 (mono)
    if (header.numChannels != 1)
    {
        return 0;
    }

    // Check if bits per sample is 16
    if (header.bitsPerSample != 16)
    {
        return 0;
    }

    // Check if subchunk2ID is "data"
    if (header.subchunk2ID[0] != 'd' || header.subchunk2ID[1] != 'a' ||
        header.subchunk2ID[2] != 't' || header.subchunk2ID[3] != 'a')
    {
        return 0;
    }

    // Format is supported
    return 1;
}

//Finding the block size
int get_block_size(WAVHEADER header)
{
    // Calculate the block size based on the number of channels and bits per sample
    int block_align = header.numChannels * header.bitsPerSample / 8;
    return block_align / 8;
}


// // Simulate genetic inheritance of blood type

// #include <stdbool.h>
// #include <stdio.h>
// #include <stdlib.h>
// #include <time.h>

// // Each person has two parents and two alleles
// typedef struct person
// {
//     struct person *parents[2];
//     char alleles[2];
// }
// person;

// const int GENERATIONS = 3;
// const int INDENT_LENGTH = 4;

// person *create_family(int generations);
// void print_family(person *p, int generation);
// void free_family(person *p);
// char random_allele();

// int main(void)
// {
//     // Seed random number generator
//     srand(time(0));
//     // Create a new family with three generations
//     person *p = create_family(GENERATIONS);

//     // Print family tree of blood types
//     print_family(p, 0);

//     // Free memory
//     free_family(p);
// }

// // Recursively creates a new individual with generations
// person *create_family(int generations)
// {
//     // TODO: Allocate memory for new person
//     person *new_person = malloc(sizeof(person));

//     // If there are still generations left to create
//     if (generations > 1)
//     {
//         // Create two new parents for current person by recursively calling create_family
//         person *parent0 = create_family(generations - 1);
//         person *parent1 = create_family(generations - 1);

//         // Set parent pointers for current person
//         new_person->parents[0] = parent0;
//         new_person->parents[1] = parent1;

//         // Randomly assign current person's alleles based on the alleles of their parents
//         new_person->alleles[0] = parent0->alleles[rand() % 2];
//         new_person->alleles[1] = parent1->alleles[rand() % 2];
//     }
//     // If there are no generations left to create
//     else
//     {
//         // Set parent pointers to NULL
//         new_person->parents[0] = NULL;
//         new_person->parents[1] = NULL;

//         // Randomly assign alleles
//         new_person->alleles[0] = random_allele();
//         new_person->alleles[1] = random_allele();
//     }

//     // Return newly created person
//     return new_person;
// }

// // Frees p and all ancestors of p.
// void free_family(person *p)
// {
//     // Handle base case
//     if (p == NULL)
//     {
//     return;
//     }
//     // Free parents recursively
//     free_family(p->parents[0]);
//     free_family(p->parents[1]);

//     // Free child
//     free(p);

//     // Free parents recursively
//     free_family(p->parents[0]);
//     free_family(p->parents[1]);

//     // Free child
//     free(p);
// }

// // Prints each family member and their alleles.
// void print_family(person *p, int generation)
// {
//     // Handle base case
//     if (p == NULL)
//     {
//         return;
//     }

//     // Print indentation
//     for (int i = 0; i < generation * INDENT_LENGTH; i++)
//     {
//         printf(" ");
//     }

//     // Print person
//     if (generation == 0)
//     {
//         printf("Child (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
//     }
//     else if (generation == 1)
//     {
//         printf("Parent (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
//     }
//     else
//     {
//         for (int i = 0; i < generation - 2; i++)
//         {
//             printf("Great-");
//         }
//         printf("Grandparent (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
//     }

//     // Print parents of current generation
//     print_family(p->parents[0], generation + 1);
//     print_family(p->parents[1], generation + 1);
// }

// // Randomly chooses a blood type allele.
// char random_allele()
// {
//     int r = rand() % 3;
//     if (r == 0)
//     {
//         return 'A';
//     }
//     else if (r == 1)
//     {
//         return 'B';
//     }
//     else
//     {
//         return 'O';
//     }
// }


// Simulate genetic inheritance of blood type

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Each person has two parents and two alleles
typedef struct person
{
    struct person *parents[2];
    char alleles[2];
}
person;

const int GENERATIONS = 3;
const int INDENT_LENGTH = 4;

person *create_family(int generations);
void print_family(person *p, int generation);
void free_family(person *p);
char random_allele();

int main(void)
{
    // Seed random number generator
    srand(time(0));

    // Create a new family with three generations
    person *p = create_family(GENERATIONS);

    // Print family tree of blood types
    print_family(p, 0);

    // Free memory
    free_family(p);
}

// Create a new individual with `generations`
person *create_family(int generations)
{
    // Allocate memory for new person
    person *p = malloc(sizeof(person));

    // If there are still generations left to create
    if (generations > 1)
    {
        // Create two new parents for current person by recursively calling create_family
        person *parent0 = create_family(generations - 1);
        person *parent1 = create_family(generations - 1);

        // Set parent pointers for current person
        p->parents[0] = parent0;
        p->parents[1] = parent1;

        // Randomly assign current person's alleles based on the alleles of their parents
        p->alleles[0] = parent0->alleles[rand() % 2];
        p->alleles[1] = parent1->alleles[rand() % 2];
    }

    // If there are no generations left to create
    else
    {
        // Set parent pointers to NULL
        p->parents[0] = NULL;
        p->parents[1] = NULL;

        // Randomly assign alleles
        p->alleles[0] = random_allele();
        p->alleles[1] = random_allele();
    }

    // Return newly created person
    return p;
}

// Free `p` and all ancestors of `p`.
void free_family(person *p)
{
    // Handle base case
    if (p == NULL)
    {
        return;
    }

    // Free parents recursively
    free_family(p->parents[0]);
    free_family(p->parents[1]);

    // Free child
    free(p);
}

// Print each family member and their alleles.
void print_family(person *p, int generation)
{
    // Handle base case
    if (p == NULL)
    {
        return;
    }

    // Print indentation
    for (int i = 0; i < generation * INDENT_LENGTH; i++)
    {
        printf(" ");
    }

    // Print person
    if (generation == 0)
    {
        printf("Child (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }
    else if (generation == 1)
    {
        printf("Parent (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }
    else
    {
        for (int i = 0; i < generation - 2; i++)
        {
            printf("        ");
        }
        printf("Grandparent (Generation %i): blood type %c%c\n", generation, p->alleles[
