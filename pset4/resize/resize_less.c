#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize factor infile outfile\n");
        return 1;
    }
    
    // check resize factor range
    int factor = atoi(argv[1]);
    if (factor < 1 || factor > 100)
    {
        fprintf(stderr, "resize factor must be must be between 1 to 100");
        return 2;
    }
    
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 5;
    }

    // set up old and new width and height
    int oldWidth = bi.biWidth;
    int oldHeight = bi.biHeight;
    bi.biWidth *= factor;
    bi.biHeight *= factor;

    // determine padding for scanlines
    int oldPadding = (4 - (oldWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // recalculate the image and file size
    bi.biSizeImage = (sizeof(RGBTRIPLE) * bi.biWidth + padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPINFOHEADER) + sizeof(BITMAPFILEHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0; i < abs(oldHeight); i++)
    {
        // set a counter for row
        int rowctr = 0;
        
        // repeat for factor # of times
        while (rowctr < factor)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < oldWidth; j++)
            {
                // temporary storage pointer | buffer
                RGBTRIPLE triple;
    
                // set a counter for pixel in a given row
                int pixelctr = 0;
                
                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            
                // write RGB triple to outfile by factor # of times
                while (pixelctr < factor)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                    pixelctr++;
                }
            }
            
            // add padding
            for (int k = 0; k < padding; k++)
                fputc(0x00, outptr);
               
            // move cursor back to the beginning of row in infile (except the last row)
            if (rowctr < (factor - 1))
                fseek(inptr, -(long int)(oldWidth * sizeof(RGBTRIPLE)), SEEK_CUR);
            
            //increase row counter since the scanline is done
            rowctr++;
        }

        // skip over old padding, if any
        fseek(inptr, oldPadding, SEEK_CUR);

    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
