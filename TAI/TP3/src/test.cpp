#include <iostream>
#include <string>
#include <stdlib.h>
#include <stdio.h>
#include <cstring>

int main(int args, char *argv[]){
	if (args < 2){
		std::cerr << "./run.sh [dataset]" << std::endl;
		return -1;
	}
	std::string directory = argv[1];
	std::string faces[7] = {"04","05","06","07","08","09","10"};
	int ncd[40];
	int nccd[40];
	int flag = 0;
	for(int i = 1; i < 41; i++){
		ncd[i-1] = 0;
		nccd[i-1] = 0;

		std::string person = i < 10 ? "0" + std::to_string(i) : std::to_string(i);
		std::string temp = "s"+person;
		char *subject = new char [3];
		std::strcpy(subject,temp.c_str());
		//subject = temp.c_str();
		std::cout << "s" << person << std::endl;
		for(auto face : faces)
    	{
      	   std::string command = "./run.sh main "+directory+"s"+ person +"/"+face+".pgm | cut -d\" \" -f3";
      	   FILE *fpipe;
      	   char c = 0;
      	   std::string temp2 = "";
      	   if (0 == (fpipe = (FILE*)popen(command.c_str(), "r")))
		    {
		        perror("popen() failed.");
		        exit(1);
		    }
		    while (fread(&c,  sizeof c, 1, fpipe))
			{
					//printf("%c",c);
					if( c == '\n'){
						if (std::strcmp(temp2.c_str(), subject) == 0){
							if(flag == 0)
								ncd[i-1]++;
							printf("Match\n");
						}
						flag = flag == 1 ? 0 : 1;
						std::cout << temp2 << std::endl;
						temp2 = "";

					}else
						temp2 += c;

			        
			}
			printf("%s",temp2.c_str());
			pclose(fpipe);
      	   //std::system(command.c_str());
    	}
	}

}