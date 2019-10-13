
// STL includes
#include <iostream>
#include <fstream>

// includes MarkovModel class
#include <markov_model/markov_model.hpp>

int main (int argc, char *argv[])
{
    if (argc < 3)
    {
        std::cerr << "Error: Invalid number of arguments!" << std::endl;
        return 1;
    }

    std::string input_filename0 = argv[1];
    std::string input_filename1 = argv[2];
    MarkovModel model0, model1;

    {
        std::ifstream ifstream(input_filename0, std::ios::binary);

        if (!ifstream)
        {
            std::cerr << "Error: The first specified file does't exist!" << std::endl;
            return 1;
        }

        ifstream >> model0;
    }

    {
        std::ifstream ifstream(input_filename1, std::ios::binary);

        if (!ifstream)
        {
            std::cerr << "Error: The second specified file does't exist!" << std::endl;
            return 1;
        }

        ifstream >> model1;
    }

    std::cout << MarkovModel::compare(model0, model1) << std::endl;

    return 0;
}