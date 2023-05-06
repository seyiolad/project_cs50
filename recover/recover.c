// #include <stdio.h>
// #include <stdlib.h>

// int main(int argc, char *argv[])
// {

// }
// ..................................

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define BLOCK_SIZE 512

bool is_jpeg_header(unsigned char buffer[]);

int main(int argc, char *argv[])
{
    // Check if there is exactly one command-line argument
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover IMAGE\n");
        return 1;
    }

    // Open the forensic image for reading
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s for reading.\n", argv[1]);
        return 1;
    }

    unsigned char buffer[BLOCK_SIZE];
    int file_count = 0;
    FILE *outptr = NULL;
    bool jpeg_found = false;

    // Read the forensic image block by block
    while (fread(buffer, BLOCK_SIZE, 1, inptr) == 1)
    {
        // Check if block is the start of a JPEG file
        if (is_jpeg_header(buffer))
        {
            // If a JPEG file was previously found, close the file
            if (jpeg_found)
            {
                fclose(outptr);
            }
            // Start writing the new JPEG file
            else
            {
                jpeg_found = true;
            }

            char filename[8];
            sprintf(filename, "%03d.jpg", file_count);
            outptr = fopen(filename, "w");
            file_count++;
        }

        // If a JPEG file has been found, write the block to the file
        if (jpeg_found)
        {
            fwrite(buffer, BLOCK_SIZE, 1, outptr);
        }
    }

    // Close any open files
    fclose(inptr);
    if (jpeg_found)
    {
        fclose(outptr);
    }

    return 0;
}

bool is_jpeg_header(unsigned char buffer[])
{
    return buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;
}
