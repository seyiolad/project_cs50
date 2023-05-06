#include "helpers.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>


// This program includes several image manipulation functions, including converting an image to grayscale,
// reflecting an image horizontally, blurring an image, and detecting edges in an image.

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate over each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate the average of the red, green, and blue values
            BYTE gray = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3;

            // Set the red, green, and blue values to the average
            image[i][j].rgbtRed = gray;
            image[i][j].rgbtGreen = gray;
            image[i][j].rgbtBlue = gray;
        }
    }
}
//Convert image to grayscale
// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Iterate over each row in the image
    for (int i = 0; i < height; i++)
    {
        // Iterate over each column up to the midpoint
        for (int j = 0; j < width / 2; j++)
        {
            // Swap the current pixel with its reflection
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create temporary copy of image
    RGBTRIPLE(*temp)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    if (temp == NULL)
    {
        return;
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // Apply blur filter to each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int count = 0;
            int red = 0;
            int green = 0;
            int blue = 0;

            // Iterate over each pixel in 3x3 grid around current pixel
            for (int k = -1; k <= 1; k++)
            {
                if (i + k < 0 || i + k >= height)
                {
                    continue;
                }
                for (int m = -1; m <= 1; m++)
                {
                    if (j + m < 0 || j + m >= width)
                    {
                        continue;
                    }
                    count++;
                    red += temp[i + k][j + m].rgbtRed;
                    green += temp[i + k][j + m].rgbtGreen;
                    blue += temp[i + k][j + m].rgbtBlue;
                }
            }

            // Set new color values to average of 3x3 grid
            image[i][j].rgbtRed = round((float) red / count);
            image[i][j].rgbtGreen = round((float) green / count);
            image[i][j].rgbtBlue = round((float) blue / count);
        }
    }

    // Free memory for temporary copy of image
    free(temp);
}

// This function detects edges in an image using the Sobel operator.
// It takes in the height and width of the image, as well as the image itself as an array of RGBTRIPLE structs.

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Allocate memory for a new image that will store the edge-detected version of the input image.
    RGBTRIPLE(*new_image)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    if (new_image == NULL)
    {
        // If there is not enough memory to store the new image, print an error message and return.
        printf("Not enough memory to store image.\n");
        return;
    }

    // Define the two kernels for the Sobel operator.
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    // Loop through each pixel in the image.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Initialize variables to store the gradient in each color channel.
            int gx_red = 0, gx_green = 0, gx_blue = 0;
            int gy_red = 0, gy_green = 0, gy_blue = 0;

            // Loop through each neighboring pixel in a 3x3 grid centered on the current pixel.
            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)
                {
                    // Calculate the row and column indices of the neighboring pixel.
                    int row = i + k;
                    int col = j + l;

                    // If the neighboring pixel is outside the image boundary, skip it.
                    if (row < 0 || row >= height || col < 0 || col >= width)
                    {
                        continue;
                    }

                    // Calculate the gradient in each color channel for the current neighboring pixel.
                    gx_red += gx[k + 1][l + 1] * image[row][col].rgbtRed;
                    gx_green += gx[k + 1][l + 1] * image[row][col].rgbtGreen;
                    gx_blue += gx[k + 1][l + 1] * image[row][col].rgbtBlue;

                    gy_red += gy[k + 1][l + 1] * image[row][col].rgbtRed;
                    gy_green += gy[k + 1][l + 1] * image[row][col].rgbtGreen;
                    gy_blue += gy[k + 1][l + 1] * image[row][col].rgbtBlue;
                }
            }

            // Calculate the magnitude of the gradient for each color channel using the Pythagorean theorem.
            int new_red = round(sqrt(gx_red * gx_red + gy_red * gy_red));
            int new_green = round(sqrt(gx_green * gx_green + gy_green * gy_green));
            int new_blue = round(sqrt(gx_blue * gx_blue + gy_blue * gy_blue));

            // Clamp the magnitude of the gradient for each color channel to a maximum of 255.
            if (new_red > 255)
            {
                new_red = 255;
            }
            if (new_green > 255)
            {
                new_green = 255;
            }
            if (new_blue > 255)
            {
                new_blue = 255;
            }

            new_image[i][j].rgbtRed = new_red;
            new_image[i][j].rgbtGreen = new_green;
            new_image[i][j].rgbtBlue = new_blue;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = new_image[i][j];
        }
    }
    // Free the memory
    free(new_image);
    return;
}

