// this file contains the declaration of the MarkovModel class
// ensures that header is only included once
#pragma once

#include <unordered_map>
#include <fstream>
#include <string>
#include <vector>

// this class represents a markov model
// an "unsigned" variable is equivelant to an "unsinged int"
class MarkovModel
{
private:
    // Helps writting code allowing to write "Frequency"
    // insted of "std::unordered_map<char, unsigned>"
    class Event
    {
    private:
        char character;
        unsigned count;
    
    public:
        Event (const char &, const unsigned &);
        Event (const char &);

        unsigned operator+ (const MarkovModel::Event &) const;
        Event &operator++ (void);

        inline const char &get_character (void) const { return character; }
        inline const unsigned &get_count (void) const { return count; }
    };

    typedef std::vector<Event> Events;
    typedef std::pair<std::string, Events> Context;
    typedef std::unordered_map<char, float> Alphabet;
    typedef std::unordered_map<std::string, Events> Frequency;

    unsigned k, alpha;
    Alphabet alphabet;
    Frequency frequency;

    static unsigned get_total (const Frequency &); // gets total occurences of each event
    static unsigned get_total (const Context &); // gets occurrences of event for given context

public:
    // constructors
    // used to build a new model
    MarkovModel (const unsigned &k, const unsigned &alpha);

    // used to load a model from file
    MarkovModel (void);

    // destructor
    ~MarkovModel (void);

    // reads stream and builds model
    // marking a function as friend allows that function to use private members of the class
    friend MarkovModel &operator>> (std::istream &, MarkovModel &);

    // writes model data to stream
    friend std::ostream &operator<< (std::ostream &, const MarkovModel &);

    // void analyze (void); -> code moved to operator>>
    // void writeToFile (std::string filename); -> code operator<<

    // Generates text based on the model
    std::string generate_text (const unsigned &, const std::string &) const;

    float get_probability (const Context &, const Event &) const;
    float get_entropy (void) const;

    // Writting a "begin" and "end" function allows the use of a "for each"
    // loop over an instance of this class. Making this functions return
    // a const iterator allows the use of the "for each" loop even if an instance
    // is marked as a constant variable
    inline Frequency::const_iterator begin (void) const { return frequency.begin(); }
    inline Frequency::const_iterator end (void) const { return frequency.end(); }
};