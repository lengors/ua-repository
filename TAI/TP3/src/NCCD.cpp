#include "../include/NCCD.hpp"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>



NCCD::NCCD(){
	ctx_file = "ImgCondComp/examples/ctx1";
	directory = "ImgCondComp/orl_faces/";
}

NCCD::NCCD(std::string dataset){
	ctx_file = "ImgCondComp/examples/ctx1";
	directory = dataset;
}



// ./NCCD3 01.pgm 01.pgm 01.pgm 01.pgm
float NCCD::compute(std::string filename1, std::string* files){
	
	std::string command = "./NCCD3 " + filename1 +" "; //+ files[0] +" "+ files[1] +" "+ files[2] + " " + ctx_file;
	for (int i = 0; i < 3; i++){
		command += " "+ files[i];
	}
	command += " " + ctx_file;
	
	FILE *output = popen (command.c_str() , "r");
	char buffer [100];
	 
	 if (output == NULL) perror ("Error opening file");
	   else
	   {
	     while ( ! feof (output) )
	     {
	       if ( fgets (buffer , 100 , output) == NULL ) break;

	       fclose (output);
	       return std::stof(buffer);
	       
	     }
	     
	   }
	 

}


float NCCD::compute(std::string filename1, int id){
	
	std::string idString = id < 10 ? "0"+std::to_string(id) : std::to_string(id);
	

	//std::string filename = "ImgCondComp/orl_faces/s"+ idString +"/"+ idString+".pgm";
	std::string files[3];
	for (int i = 0; i < 3; i++){
		std::string id = i< 10 ? "0"+std::to_string(i+4) : std::to_string(i+4);
		files[i] = directory+"s"+idString+"/"+id+".pgm";
	}	


	return compute(filename1,files);
	
}