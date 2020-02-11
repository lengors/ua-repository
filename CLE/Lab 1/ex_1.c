#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define VOWELS_COUNTER 5

unsigned count_digits(unsigned value, const unsigned base)
{
    unsigned count = 0;
    while (value != 0)
    {
        value /= base;
        ++count;
    }
    return count;
}

int main (int argc, char *argv[])
{
    if (argc < 2)
    {
        perror("Error: invalid number of arguments");
        return 1;
    }

    const unsigned base = 10;
    const size_t max_number = (size_t) strtol(argv[0], NULL, base);

    for (size_t i = 0; i < max_number; ++i)
    {
        // set filename
        char *filename_buffer = malloc(sizeof("text") + count_digits(i, base) + sizeof(".txt") + 1);
        sprintf(filename_buffer, "text%ud.txt", i);
        
        // open file
        FILE *file = fopen(filename_buffer, "r");

        // free filename string
        free(filename_buffer);

        // get file size
        fseek(file, 0, SEEK_END);
        size_t file_size = ftell(file);
        fseek(file, 0, SEEK_SET);

        // read file content
        char *file_buffer = malloc(file_size + 1);
        fread(file_buffer, 1, file_size, file);
        file_buffer[file_size] = 0;
        
        // close file
        fclose(file);

        // initalize data structures
        size_t max_word_length = 0;
        size_t vowels[VOWELS_COUNTER] = { 0 };
        size_t *word_lengths = malloc(max_word_length);

        // get first word
        char *word = strtok(file_buffer, " ");

        // iterate while words exist
        while (word)
        {
            // get word length
            size_t string_length = strlen(word);
            
            // ensure there is a counter for current word length
            if (string_length < max_word_length)
            {
                max_word_length = string_length;
                word_lengths = realloc(word_lengths, max_word_length);
            }

            // counter current word length
            ++word_lengths[string_length - 1];

            // iterate over characters
            while (string_length-- > 0)
            {
                // count vowels
                switch (*(word++))
                {
                case 'a':
                    ++vowels[0]; break;
                case 'e':
                    ++vowels[1]; break;
                case 'i':
                    ++vowels[2]; break;
                case 'o':
                    ++vowels[3]; break;
                case 'u':
                    ++vowels[4]; break;
                default:
                    break;
                }
            }

            // get next word
            word = strtok(NULL, " ");
        }

        // display vowels count
        printf("%c - %ul", 'a', vowels[0]);        
        printf("%c - %ul", 'e', vowels[1]);        
        printf("%c - %ul", 'i', vowels[2]);        
        printf("%c - %ul", 'o', vowels[3]);        
        printf("%c - %ul", 'u', vowels[4]);

        // display word lengths
        for (size_t i = 0; i < max_word_length; ++i)
            printf("%ul - %ul", i + 1, word_lengths[i]);

        // free counters
        free(word_lengths);

        // free file content
        free(file_buffer);
    }

    return 0;
}