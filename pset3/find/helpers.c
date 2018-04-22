/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

// Returns true if value is in array values[] of size n, else false.
bool search(int value, int values[], int n)
{
    // binary search
    int start = 0;
    int end = (n - 1);
    int mid;
    
    while (start <= end)
    {
        mid = (start + end) / 2;
        
        if (value == values[mid])
        {
            return true;
        }
        else if (value < values[mid])
        {
            end = mid - 1;
        }
        else if (value > values[mid])
        {
            start = mid + 1;
        }
    }
    
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    int a, b, tempValue;
    
    // bubble sort
    for (a = 0; a < (n - 1); a++)
    {
        for (b = 0; b < (n - 1 - a); b++)
        {
            if (values[b] > values[b + 1])
            {
                tempValue = values[b];
                values[b] = values[b + 1];
                values[b + 1] = tempValue;
            }
        }
    }
    
    return;
}
