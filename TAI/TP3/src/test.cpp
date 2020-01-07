#include <iostream>
#include <string>
#include <stdlib.h>
#include <stdio.h>
#include <cstring>
#include "../include/NCD.hpp"
#include "../include/NCCD.hpp"
#include <map>
#include <iterator>
#include <algorithm>

bool compare(std::pair<std::string, float> first, std::pair<std::string, float> sec){
    return first.second < sec.second;
}

std::pair<std::string, float> computeNCD(std::string pic, std::string directory){
	NCD* ncd = new NCD();
    std::map<std::string, float> computations;
	for (int i = 1; i < 41; i++){
        std::string face = i < 10 ? "0" + std::to_string(i) : std::to_string(i);
        float value = 0;
        for (int j = 4; j < 11; j++){
            std::string aux = j < 10 ? "0" + std::to_string(j) : std::to_string(j);
            
            value += ncd->compute(pic, directory + "s" + face + "/" + aux + ".pgm");
        }
        float avg = value / 7;
        computations.insert(std::pair<std::string, float>("s" + face, avg));
    }
	
    std::pair<std::string, float> min = *std::min_element(computations.begin(), computations.end(), compare); 
	return min;
}

std::string computeNCCD(std::string pic, std::string directory){
	NCCD* nccd = new NCCD(directory);
	int valor = -1;
	int id;
	for(int i = 1; i < 41; i++){ // first 10 ppl
		int temp = nccd->compute(pic,i);
		if ((valor == -1) || (valor > temp)){
			id = i;
			valor = temp;
		}
	}
	std::string output = "s" + (id < 10 ? "0" + std::to_string(id) : std::to_string(id));
	return output;
}

int main(int args, char *argv[]){
	if (args < 2){
		std::cerr << "./run.sh [dataset]" << std::endl;
		return -1;
	}
	std::string directory = argv[1];
	std::string faces[3] = {"01.pgm","02.pgm","03.pgm"};
	int datasetSize = 40;
	int ncd[datasetSize];
	int nccd[datasetSize];
	
	for (int i = 1; i < 41; i++){ //first 10 ppl
		ncd[i - 1] = 0;
		nccd[i - 1] = 0;
        std::string face = "s" + (i < 10 ? "0" + std::to_string(i) : std::to_string(i));

		for (int j = 1; j < 4; j++){
			std::cout << face + " - image : " + faces[j - 1] << std::endl;
			std::string pic = directory + face + "/" + faces[j - 1];
			std::pair<std::string, float> min = computeNCD(pic, directory);
			std::string minNCCD = computeNCCD(pic, directory);
			if (face == min.first){
				ncd[i - 1]++;
			}
			if(face == minNCCD){
				nccd[i-1]++;
			}

		}
	
	}

	for(int i = 0; i < datasetSize; i++)
    {
    	std::cout << "Test Subject: " << i+1 << std::endl;
        std::cout << std::string("ncd face ") + std::to_string(i) + " = " + std::to_string(ncd[i]) << std::endl;
        std::cout << std::string("nccd face ") + std::to_string(i) + " = " + std::to_string(nccd[i]) << std::endl;
    }
	

}