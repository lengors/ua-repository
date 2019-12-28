#include "NCCD.hpp"
#include <iostream>


float NCCD::GetFileSize(std::string filename)
{
    
    FILE* outputfile = popen(("ls -l " + filename + " | cut -d ' ' -f5").c_str(), "r");
    std::string result = "";
    char buffer[100];
    while ( ! feof (outputfile) )
    {
        if ( fgets (buffer , 100 , outputfile) == NULL ) break;
        result += buffer;
    }
    fclose (outputfile);
    
    return stof(result);
}



float NCCD::compress(std::string filename, std::string filename2){
    return 0;

}

float NCCD::compute(std::string filename, std::string filename2) {

    float cxy = compress(filename, filename2);
    float cyx = compress(filename2, filename);
    float cx = compress(filename);
    float cy = compress(filename2);

    //std::cout << cxy << " - " <<  cx << " - " << cy << std::endl; 
    return ((cxy > cyx ? cxy : cyx) / (cx > cy ? cx : cy)); 
    

}