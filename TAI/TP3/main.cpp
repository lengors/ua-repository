#include <iostream>
#include <string>
#include "NCD.hpp"
#include <map>
#include <iterator>
#include <algorithm>

bool compare(std::pair<std::string, float> first, std::pair<std::string, float> sec){
    return first.second < sec.second;
}

int main(int args, char *argv[]){

    if (args < 2){
        std::cerr << "Número de argumentos inválido" << std::endl;
        return 1;
    }

    std::string img = argv[1];
    std::string directory = "./ImgCondComp/orl_faces/";
    if (args == 3){
        directory = argv[2];
    } 
    

    NCD* ncd = new NCD("lzma");
    std::map<std::string, float> computations;
    for (int i = 1; i < 41; i++){
        std::string face = i < 10 ? "0" + std::to_string(i) : std::to_string(i);
        float value = 0;
        for (int j = 1; j < 11; j++){
            std::string aux = j < 10 ? "0" + std::to_string(j) : std::to_string(j);
            std::cout << "s" + face + "/" + aux + ".pgm" << std::endl;
            value += ncd->compute(img, directory + "s" + face + "/" + aux + ".pgm");
        }
        float avg = value / 10;
        computations.insert(std::pair<std::string, float>("s" + face, avg));
    }

    for(auto elem : computations)
    {
        std::cout << elem.first << " " << elem.second << "\n";
    }

    std::cout << "\n";
    std::pair<std::string, float> min = *std::min_element(computations.begin(), computations.end(), compare); 
    std::cout << "The person in the picture is " << min.first << " " << std::endl;

    /*
    float value = ncd->compute(img_name, "02.pgm");
    std::cout << value << std::endl;
    */
    
    return 0;
}