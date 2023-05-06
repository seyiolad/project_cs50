
#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // Change all black pixels to a color of your choosing
    //I choose RED

    // Iterate over each pixel in the image
    for (int a = 0; a < height; a++)
    {
        for (int b = 0; b < width; b++)
        {
            // Check if the pixel's color is black
            if (image[a][b].rgbtRed == 0x00 && image[a][b].rgbtGreen == 0x00 && image[a][b].rgbtBlue == 0x00)
            {
                // Change the color to red
                image[a][b].rgbtRed = 0xFF;
                image[a][b].rgbtGreen = 0x00;
                image[a][b].rgbtBlue = 0x00;
            }
        }
    }
}



