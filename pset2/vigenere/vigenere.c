#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{

    // if incorrect # of key (i.e. 1)
    if (argc != 2)
    {
        printf("Incorrect number of arguments\n");
        return 1;
    }
    
    // if correct # of key
    else
    {
        int key[26];    // set up int array for each char in the key
        int ctr = 0;    // set up a counter for key
        
        // error if any of the characters isn't alphabetic
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("key is not alphabetic\n");
                return 1;
            }
            
        }    

        // if all chars are alphabetic
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (isalpha(argv[1][i]))
            {
                // storing the key A-Z as 0-25
                key[i] = toupper(argv[1][i]) - 65;
                

            }
        }
        
        printf("plaintext: ");
        
        string plain = get_string();
        
        printf("ciphertext: ");

        for (int i = 0, n = strlen(plain); i < n; i++)
        {
            // if alphabet
            if (isalpha(plain[i]))
            {
                // if lowercase
                if (islower(plain[i]))
                {
                    char lower = ((plain[i] - 97) + ( key[(ctr % (strlen(argv[1])))])) % 26 + 97;
                    printf("%c", lower);
                    
                }
                
                // if uppercase
                else if (isupper(plain[i]))
                {
                    char upper = ((plain[i] - 65) + ( key[ctr % (strlen(argv[1]))])) % 26 + 65;
                    printf("%c", upper);
                }
                
                ctr++;
            }            
            
            // if not alphabet
            else if (!isalpha(plain[i]))
            {
                printf("%c", plain[i]);
            }
           
        }
        
        printf("\n");
        
        return 0;
    }                       
}