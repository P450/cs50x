#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;

    do
    {
        printf("Height: ");
        height = get_int();
    } while ((height > 23) || (height < 0));

    for (int i = 0; i < height; i++)
    {
        for (int j = (height - (i + 1)); j > 0; j--)
        {
            printf(" ");
        }

        for (int j = 0; j < (i + 2); j++)
        {
            printf("#");
        }
        printf("\n");
    }
}