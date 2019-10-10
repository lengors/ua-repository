
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
    bool print_text = false;
    std::string initial_text, input_filename, output_filename;

    while (index < argc)
    {
        std::string current = argv[index++];
        if (current.substr(0, 2) == "-s" && max_size == 0)
            max_size = std::stoi(current.size() == 2 ? argv[index++] : current.substr(2));
        else if (current.substr(0, 2) == "-t" && initial_text.size() == 0)
            initial_text = current.size() == 2 ? argv[index++] : current.substr(2);
        else if (current.substr(0, 2) == "-o" && output_filename.size() == 0)
            output_filename = current.size() == 2 ? argv[index++] : current.substr(2);
        else if (current.substr(0, 2) == "-p" && !print_text)
            print_text = true;
        else if (input_filename.size() == 0)
            input_filename = current;
        else
        {
            std::cerr << "Usage: " << argv[0] << " [-s max_size] [-t initial_text] [-o output_model_filename] [-p] [input_model_filename]" << std::endl;
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

    if (max_size != 0 && max_size < model.get_k())
    {
        std::cerr << "Error: specified max_size is less tha k (" << model.get_k() << ")!" << std::endl;
        return 1;
    }

    std::string generated_text = model.generate_text(max_size, initial_text);
    
    if (print_text)
        std::cout << generated_text  << std::endl;

    if (output_filename.size() != 0)
    {
        MarkovModel g_model(model, generated_text);

        {
            std::ofstream ofstream(output_filename, std::ios::binary);

            if (!ofstream)
            {
                std::cerr << "Error: Save model failed!" << std::endl;
                return 1;
            }

            ofstream << g_model;
        }
    }


    return 0;
}