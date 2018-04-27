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
    double factor = atof(argv[1]);
    if (factor <= 0 || factor > 100)
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

    // // write outfile's BITMAPFILEHEADER and BITMAPINFOHEADER
    // fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    // fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // declare a 2-dimensional array to hold the pixels
    RGBTRIPLE pixels[bi.biWidth][abs(bi.biHeight)];

    // iterate over infile's scanlines
    for (int y = 0, n = abs(bi.biHeight); y < n; y++)
    {
        // iterate over the pixels in scanline
        for (int x = 0; x < bi.biWidth; x++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read a pixel and store the return in temp
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // store the read pixel in pixels array
            pixels[x][y] = triple;
        }

        // skip over padding in scanline
        fseek(inptr, padding, SEEK_CUR);
    }

    /*
    *
    *       resizing image
    *
    */

    // update width and height
    bi.biWidth *= factor;
    bi.biHeight *= factor;

    // update padding
    padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // update image and file sizes
    bi.biSizeImage = (sizeof(RGBTRIPLE) * bi.biWidth + padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPINFOHEADER) + sizeof(BITMAPFILEHEADER);

    // write outfile's BITMAPFILEHEADER and BITMAPINFOHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // iterate over infile's scanlines
    for (int y = 0, n = abs(bi.biHeight); y < n; y++)
    {
        // iterate over the pixels in scanline
        for (int x = 0; x < bi.biWidth; x++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // update the pixel array dimensions and put in storage
            triple = pixels[(int)(x / factor)][(int)(y / factor)];

            // write pixel to outfile
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
        }

        // add padding
        for (int i = 0; i < padding; i++)
        {
            fputc(0x00, outptr);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
