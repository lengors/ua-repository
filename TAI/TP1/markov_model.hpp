// this file contains the declaration of the MarkovModel class
// ensures that header is only included once
#pragma once

#include <fstream>
#include <unordered_map>
#include <string>
#include <list>
#include <map>


struct CharData{
    char c;
    int count;
};

// this class represents a markov model
// an "unsigned" variable is equivelant to an "unsinged int"
class MarkovModel
{
private:
    // Helps writting code allowing to write "Frequency"
    // insted of "std::unordered_map<char, unsigned>"
    typedef std::unordered_map<char, unsigned> Frequency;

    unsigned k, alpha;
    Frequency frequency;
    std::string content;
   
    std::map<std::string,std::list <CharData>> tableMap;
   

public:
    // constructor
    MarkovModel (const unsigned &k, const unsigned &alpha);

    // destructor
    ~MarkovModel (void);

    // reads file and builds model
    // marking a function as friend allows that function to use private members of the class
    friend MarkovModel &operator>> (std::ifstream &, MarkovModel &);

    void analyze ();

    void writeToFile(std::string filename);

    // Writting a "begin" and "end" function allows the use of a "for each"
    // loop over an instance of this class. Making this functions return
    // a const iterator allows the use of the "for each" loop even if an instance
    // is marked as a constant variable
    inline Frequency::const_iterator begin (void) const { return frequency.begin(); }
    inline Frequency::const_iterator end (void) const { return frequency.end(); }
};