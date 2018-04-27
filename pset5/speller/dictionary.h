/**
 * Declares a dictionary's functionality.
 */

#ifndef DICTIONARY_H        // #ifndef (if not defined)
#define DICTIONARY_H

#include <stdbool.h>

// maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word);

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary);

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void);

/**
 * Unloads dictionary from memory.  Returns true if successful else false.
 */
bool unload(void);

#endif // DICTIONARY_H


// NOTES:
    // char* is a pointer that points to a location containing a value of type char that can also be chagned & pointer's value can be changed (i.e. point to a diff location)
    // const char* is a pointer, whose value can be changed, that points to a location containing a value of type char that CANNOT be changed


// similar to #define PI 3.14, PI = (#define DICTIONARY_H) and 3.14 is (everything between #define DICTIONARY_H and #endif)
// this prevents compiler from trying to include the section defined as DICTIONARY_H twice if separate files reference it
                                                                                        // (e.g. c:10 speller.c and c:7 dictionary.c)