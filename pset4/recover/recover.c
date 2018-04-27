#include <stdio.h>
#include <stdint.h>

// define unsigned 8 bit integer as BYTE
typedef uint8_t BYTE;

// define buffer size
#define BUFFERSIZE 512

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover file\n");
        return 1;
    }

    // store argv[1] into *infile
    char *infile = argv[1];

    //open memory card file
    FILE *file = fopen(infile, "r");
    if (file == NULL)
    {
        printf("Could not open file\n");
        return 2;
    }


    // create a variable for jpeg number
    int jpgcounter = 0;

    // create an output file
    FILE *outfile = NULL;

    // create a buffer array to store 512 bytes (i.e. a block)
    BYTE buffer[BUFFERSIZE];

    // until the end of file
    while (fread(buffer, BUFFERSIZE * sizeof(BYTE), 1, file) != 0)
    {
        // check the first 4 bytes are jpg header
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
           (buffer[3] & 0xf0) == 0xe0)
        {
            // close previous file if it's not null
            if (outfile != NULL)
                fclose(outfile);

            // create an array for jpg file name (e.g. 000.jpg)
            char filename[8];

            // store jpgcounter.jpg to filename
            sprintf(filename, "%03d.jpg", jpgcounter);

            // increase counter
            jpgcounter++;

            // open filename and store the returning pointer into *outfile
            outfile = fopen(filename, "w");

            // check if outfile is valid
            if (outfile == NULL)
            {
                printf("Could not create file\n");
                return 3;
            }

            // write one buffer (512 bytes sized array) into outfile
            fwrite(buffer, BUFFERSIZE, 1, outfile);
        }

        // if the first 4 bytes of block aren't a jpg header
        else if (outfile != NULL) {
            fwrite(buffer, BUFFERSIZE, 1, outfile);
        }
    }

    fclose(outfile);

    return 0;
}