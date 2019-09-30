
// STL includes
#include <iostream>
#include <fstream>

// includes MarkovModel class
#include <markov_model/markov_model.hpp>

int main (int argc, char *argv[])
{
    MarkovModel model;

    if (argc < 2)
    {
        std::cerr << "Error: Invalid number of arguments!" << std::endl;
        return 1;
    }

    // gets size from arguments
    int size = std::stoi(argv[1]);

    // sets filenames
    std::string input_filename = argc <= 2 ? "model.mdl" : argv[2];

    {
        std::ifstream ifstream(input_filename, std::ios::binary);

        if (!ifstream)
        {
            std::cerr << "Error: Specified file does't exist!" << std::endl;
            return 1;
        }

        ifstream >> model;
    }

    // std::cout << model << std::endl;
    std::cout << "Generating text from model..." << std::endl << std::endl;

    std::cout << model.generate_text(size) << std::endl;

    return 0;
}