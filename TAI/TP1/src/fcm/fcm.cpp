// STL includes
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

// includes MarkovModel class
#include <markov_model/markov_model.hpp>

int main (int argc, char *argv[])
{

    bool print_model = false;
    std::vector<std::string> arguments;
    
    arguments.reserve(argc - 1);
    for (int i = 1; i < argc; )
    {
        std::string argument = argv[i++];
        if (argument == "-p")
            print_model = true;
        else
            arguments.emplace_back(argument);
    }

    // Checks if at least two arguments exist (k and alpha)
    if (arguments.size() < 2)
    {
        std::cerr << "Error: Invalid number of arguments!" << std::endl;
        return 1;
    }

    // converts string to integer
    int k = std::stoi(arguments[0]);

    // converts string to integer
    int alpha = std::stoi(arguments[1]);

    // sets filenames
    std::string input_filename = arguments.size() <= 2 ? "test.txt" : arguments[2];
    std::string output_filename = arguments.size() <= 3 ? "model.mdl" : arguments[3];

    // Creates markov model
    MarkovModel model(k, alpha);

    // Scope used to open, read an close file
    // Close operation happens automatically at the end of the scope 
    {
        // Creates file stream from filename
        std::ifstream ifstream(input_filename);

        // If file doesn't exist display error and exit
        if (!ifstream)
        {
            std::cerr << "Error: Specified file does't exist!" << std::endl;
            return 1;
        }

        // Processes file and creates model
        ifstream >> model;
    }

    // std::cout << model << std::endl;

    // model.analyze(); -> code moved to operator>>
    // model.writeToFile("output.txt"); -> code moved to operator<<

    // TODO: remove this, just for testing
    {
        std::ofstream ofstream(output_filename, std::ios::binary);

        if (!ofstream)
        {
            std::cerr << "Error: Save model failed!" << std::endl;
            return 1;
        }

        ofstream << model;
    }

    return 0;
}