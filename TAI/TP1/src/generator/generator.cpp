
// STL includes
#include <iostream>
#include <fstream>

// includes MarkovModel class
#include <markov_model/markov_model.hpp>

int main (int argc, char *argv[])
{
    MarkovModel model;

    // sets filenames
    std::string input_filename = argc <= 1 ? "model.mdl" : argv[1];

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

    std::cout << model.generate_text(440) << std::endl;

    return 0;
}