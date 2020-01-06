#include "NCCD.hpp"
NCCD::NCCD(){
	ctx_file = "ImgCondComp/examples/ctx1";
}

NCCD::NCCD(std::string name){
	ctx_file = name;
}



// ./NCCD3 01.pgm 01.pgm 01.pgm 01.pgm
float NCCD::compute(std::string filename1, std::string* files){
	
	std::string command = "./NCCD3 " + filename1 +" "+ files[0] +" "+ files[1] +" "+ files[2] + " " + ctx_file;
	
	FILE *output = popen (command.c_str() , "r");
	char buffer [100];
	 
	 if (output == NULL) perror ("Error opening file");
	   else
	   {
	     while ( ! feof (output) )
	     {
	       if ( fgets (buffer , 100 , output) == NULL ) break;

	      
	       return std::stof(buffer);
	       
	     }
	     
	   }

}

float NCCD::compute(std::string filename1, int id){
	std::string idString;
	if (id >= 10)
		idString =std::to_string(id);
	else
		idString = "0"+std::to_string(id);

	//std::string filename = "ImgCondComp/orl_faces/s"+ idString +"/"+ idString+".pgm";
	std::string files[3] = {"ImgCondComp/orl_faces/s"+ idString +"/01.pgm","ImgCondComp/orl_faces/s"+ idString +"/02.pgm","ImgCondComp/orl_faces/s"+ idString +"/03.pgm"};


	return compute(filename1,files);
}