#include <iostream>
#include <fstream>

#include "markov_model.hpp"

int main (int argc, char *argv[])
{
    MarkovModel model;

    unsigned k, alpha;
    std::size_t reserve_size;
    std::unordered_set<char> alphabet;

    // sets filenames
    std::string input_filename = argc <= 1 ? "model.mdl" : argv[1];

    {
        std::ifstream ifstream(input_filename, std::ios::binary);

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
}