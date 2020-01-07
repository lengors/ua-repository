#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include<stdio.h>

int main(int args, char *argv[]){
	if (args < 2){
		
        std::cerr << "./resize [resize multiplier]" << std::endl;
        return 1;
    } 
    float mult = std::stof(argv[1]); //multiplier
    std::string command = "mkdir reduced/"+std::to_string(mult);
    std::system(command.c_str());

	for (int i = 1; i < 41; i++){

		std::string id = i < 10 ? "0" + std::to_string(i) : std::to_string(i);
		command = "mkdir reduced/"+std::to_string(mult)+"/s"+id;
		std::system(command.c_str());
		for (int j = 1; j < 11; j++){
			std::string face = j < 10 ? "0" + std::to_string(j) : std::to_string(j);
			
			cv::Mat input = cv::imread("ImgCondComp/orl_faces/s"+id+"/"+face+".pgm", 1);
			cv::Mat output;
			cv::resize(input, output, cv::Size(), mult, mult, CV_INTER_LINEAR);
			//cv::FileStorage file("reduced/"+std::to_string(mult)+"/s"+id+"/"+face+".pgm", cv::FileStorage::WRITE);

			cv::imwrite("reduced/"+std::to_string(mult)+"/s"+id+"/"+face+".pgm", output); 
		}
	}
	std::cout << "Done!" << std::endl;
	return 0;
}