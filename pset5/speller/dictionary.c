/**
 * Implements a dictionary's functionality.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"

const int HASH_SIZE = 65536;

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// declare hash table array
node *ht_array[HASH_SIZE] = {NULL};

// declare word counter
int wordctr = 0;
char word[LENGTH + 1];

// declare check point for load()
bool loaded = false;


/**
 * Returns hash code of the passed word (source of hash function: reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9nlkn/)
 */
unsigned int hash_it(const char* needs_hashing)
{
    unsigned int hash = 0;

    for (int i = 0; i < HASH_SIZE && needs_hashing[i] != '\0'; i++)
    {
        hash = (hash << 2) ^ needs_hashing[i];
    }

    return (unsigned int) (unsigned short) hash;
}


/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // create an array for lower case word in type char
    char low_word[LENGTH + 1];

    // convert const char* to type char* and change case, character by character
    for (int i = 0, t = strlen(word) + 1; i < t; i++)
    {
        low_word[i] = word[i];
        low_word[i] = tolower(low_word[i]);
    }

    unsigned int hcode = hash_it(low_word);

    // put the pointer in hash table array at that index into cursor
    node *cursor = ht_array[hcode];

    // until cursor reaches the end of the linked list
    while (cursor != NULL)
    {
        // compare word in node & word in text
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }

        // move the cursor to the next node
        cursor = cursor->next;
    }

    return false;
}


/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // open dictionary
    FILE *fp = fopen(dictionary, "r");
    if (fp == NULL)
    {
        printf("Could not open dictionary\n");
        return false;
    }

    // NULL all elements of the hash table array
    for (int i = 0; i < HASH_SIZE; i++)
    {
        ht_array[i] = NULL;
    }

    // declare an array to store dictionary words
    char word[LENGTH + 1];

    // loop until EOF is reached
    while (fscanf(fp, "%s\n", word) != EOF)
    {
        // allocate memory for node
        node *newnode = malloc(sizeof(node));
        if (newnode == NULL)
        {
            unload();
            return false;
        }

        // copy a word in the dictionary into the word field of a node
        strcpy(newnode->word, word);

        wordctr++;

        // create a hash code for each word
        unsigned int hash_code = hash_it(newnode->word);

        // check if hash table array at index [hash_code] is empty
        if (ht_array[hash_code] == NULL)
        {
            // if so, put a pointer to a new node there
            ht_array[hash_code] = newnode;
            newnode->next = NULL;
        }
        // if there is already a pointer there
        else
        {
            // insert the new node into the linked list
            newnode->next = ht_array[hash_code];
            ht_array[hash_code] = newnode;
        }
    }

    fclose(fp);

    loaded = true;

    return true;
}


/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    if (loaded == true)
    {
        return wordctr;
    }
    else
    {
        return 0;
    }
}


/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // repeat for all elements in hash table array
    for (int i = 0; i < HASH_SIZE; i++)
    {
        // create a pointer and store the value of hash table array at each index (no need to malloc since the nodes exist)
        node *cursor = ht_array[i];

        // check all the nodes in the linked list
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }

        // NULL the head pointers in the hash table array
        ht_array[i] = NULL;
    }

    return true;
}
