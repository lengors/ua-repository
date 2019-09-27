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

    // sets filenames
    std::string input_filename = argc <= 3 ? "test.txt" : argv[3];
    std::string output_filename = argc <= 4 ? "model.mdl" : argv[4];

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

    std::cout << " Text total appearances " << std::endl;
    for (const auto &context : model)
    {
        std::cout << context.first << "-";
        for (auto &event : context.second)
            std::cout << "[" << event.get_character() << "," << event.get_count() << "]" << ", ";
        std::cout << ";\n";
    }
    std::cout << " Conditional Probability " << std::endl;

    for (const auto &context : model)
        for (auto &event : context.second)
            std::cout << context.first << " followed by " << event.get_character() << ":" << model.get_probability(context, event) << std::endl;

    // model.analyze(); -> code moved to operator>>
    // model.writeToFile("output.txt"); -> code moved to operator<<

    std::cout << model.get_entropy() << std::endl;

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