
#include "../include/NCD.hpp"
#include <iostream>

NCD::NCD() {
    compressor = "gzip";
}

NCD::NCD(std::string comp) {
    compressor = comp;
}

float NCD::GetFileSize(std::string filename)
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



float NCD::compress(std::string filename, std::string filename2){
    std::string command = "";
    float size;

    if (filename2 != ""){
        system(("convert " + filename + " " + filename2 + " -append " + "full.pgm").c_str());
        filename = "full.pgm";
    }

    if (compressor == "gzip"){
        command = compressor + " -k " + filename; 
        
        system((command).c_str());
        size = GetFileSize(filename + ".gz");
        system(("rm " + filename + ".gz").c_str());
        
    }

    else if (compressor == "lzma"){
        command = "lzma -k " + filename; 
        system((command).c_str());
        
        size = GetFileSize(filename + ".lzma");
        system(("rm -f " + filename + ".lzma").c_str());
        
    }
    system("rm -f full.pgm");
    
    
    
    return size;


}

float NCD::compute(std::string filename, std::string filename2) {

    float cxy = compress(filename, filename2);
    float cx = compress(filename);
    float cy = compress(filename2);

    //std::cout << cxy << " - " <<  cx << " - " << cy << std::endl; 
    return ((cxy - (cx > cy ? cy : cx)) / (cx > cy ? cx : cy)); 
    

}