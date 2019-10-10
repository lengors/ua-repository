
// STL includes
#include <iostream>
#include <fstream>

// includes MarkovModel class
#include <markov_model/markov_model.hpp>

int main (int argc, char *argv[])
{
    MarkovModel model;

    int index = 1;
    unsigned max_size = 0;
    std::string initial_text, input_filename;

    while (index < argc)
    {
        std::string current = argv[index++];
        if (current.substr(0, 2) == "-s" && max_size == 0)
            max_size = std::stoi(current.size() == 2 ? argv[index++] : current.substr(2));
        else if (current.substr(0, 2) == "-t" && initial_text.size() == 0)
            initial_text = current.size() == 2 ? argv[index++] : current.substr(2);
        else if (input_filename.size() == 0)
            input_filename = current;
        else
        {
            std::cerr << "Usage: " << argv[0] << " [-s max_size] [-t initial_text] [model_filename]" << std::endl;
            return 1;
        } 
    }

    if (input_filename.size() == 0)
        input_filename = "model.mdl";

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

    std::string text_generated = model.generate_text(max_size, initial_text);
    std::cout << text_generated  << std::endl;
    std::cout << "SIZE: " << text_generated.size() << std::endl;

    return 0;
}