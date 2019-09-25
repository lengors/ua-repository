// STL includes
#include <iostream>
#include <fstream>
#include <string>

// includes MarkovModel class
#include "markov_model.hpp"




int main (int argc, char *argv[])
{
    // Checks if at least two arguments exist (k and alpha)
    if (argc < 3)
    {
        std::cerr << "Error: Invalid number of arguments!" << std::endl;
        return 1;
    }

    // converts string to integer
    int k = std::stoi(argv[1]);

    // converts string to integer
    int alpha = std::stoi(argv[2]);

    // sets filename
    std::string filename = argc == 3 ? "test.txt" : argv[3];

    // Creates file stream from filename
    std::ifstream fileStream(filename);
    
    // If file doesn't exist display error and exit
    if (!fileStream)
    {
        std::cerr << "Error: Specified file does't exist!" << std::endl;
        return 1;
    }

    // Creates markov model
    MarkovModel model(k, alpha);

    // Processes file and creates model
    fileStream >> model;

    model.analyze();

    // Closes file
    fileStream.close();

    // Prints all letters and respective amount
    // "auto" tells the compiler to determine the type
    model.writeToFile("output.txt");

    return 0;
}