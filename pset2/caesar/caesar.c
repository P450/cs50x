#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    // print error unless 2-argument input
    if (argc != 2)
    {
        printf("Incorrect number of arguments\n");
        return 1;
    }

    int key = atoi(argv[1]); // convert key to int from string

    // print plaintext
    printf("plaintext: ");
    string p = get_string();
    printf("ciphertext: ");

    // for every character of plaintext
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        if (isalpha(p[i]))
        {
            if (islower(p[i]))
            {
                // making letter 0 indexed (i.e. a = 0) then coverting back to original ascii value
                char lower = ( (p[i] - 97 + key) % 26 + 97);
                printf("%c", lower);
            }

            else
            {
                char upper = ( (p[i] - 65 + key) % 26 + 65);
                printf("%c", upper);
            }
        }

        else
        {
            printf("%c", p[i]);
        }

    }

    printf("\n");

    return 0;
}
