
#include <iostream>
#include <string>
#include "NCD.hpp"

int main(int args, char *argv[]){

    if (args < 2){
        std::cerr << "Número de argumentos inválido" << std::endl;
        return 1;
    }

    std::string img_name = argv[1];

    NCD* ncd = new NCD();

    float value = ncd->compute(img_name, "02.pgm");
    std::cout << value << std::endl;
    
    return 0;
}