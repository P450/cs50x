/**
 * generate.c
 *
 * Generates pseudorandom numbers in [0,MAX), one per line.
 *
 * Usage: generate n [s]
 *
 * where n is number of pseudorandom numbers to print
 * and s is an optional seed
 */

#define _XOPEN_SOURCE

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// upper limit on range of integers that can be generated
#define LIMIT 65536

int main(int argc, string argv[])
{
    // if argc isn't 2 or 3
    if (argc != 2 && argc != 3)
    {
        printf("Usage: ./generate n [s]\n");
        return 1;
    }

    // converting argv[1] to int; then storing it into n
    int n = atoi(argv[1]);

    // if argc is 3, seed srand48 the long data type of int of argv[2]
    if (argc == 3)
    {
        srand48((long) atoi(argv[2]));
    }
    // else (argc == 2), seed srand48 the output of time(null)
    else
    {
        srand48((long) time(NULL));
    }

    // for [0 to argv[1]), print int of drand48*limit
    for (int i = 0; i < n; i++)
    {
        printf("%i\n", (int) (drand48() * LIMIT));
    }

    // success
    return 0;
}
