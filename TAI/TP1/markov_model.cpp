// this file contains the implementation of the MarkovModel class
#include "markov_model.hpp"

#include <iostream>

// using namespace std; <- not recommended, may create ambiguity

// constructor
MarkovModel::MarkovModel (const unsigned &k, const unsigned &alpha) :
    k(k), alpha(alpha)
{
}

// destructor
MarkovModel::~MarkovModel (void)
{
}

// reads file and builds model
MarkovModel &operator>> (std::ifstream &fileStream, MarkovModel &model)
{
    char letter;
    // iterates over every character in the file
    // and counts how many times each character appears
    // TODO: replace with (k) sequence of characters
    while (fileStream.get(letter))
    {
        std::unordered_map<char, unsigned>::iterator iterator = model.frequency.find(letter);
        if (iterator == model.frequency.end())
            model.frequency[letter] = 1;
        else
            ++iterator->second; // slightly more efficient than "++frequency[letter]"";
    }
    return model;
}