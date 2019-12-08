
#include "NCD.hpp"
#include <iostream>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

NCD::NCD() {
    compressor = "gzip";
}

NCD::NCD(std::string comp) {
    compressor = comp;
}

float NCD::GetFileSize(std::string filename)
{
    struct stat stat_buf;
    int rc = stat(filename.c_str(), &stat_buf);
    return rc == 0 ? stat_buf.st_size : -1;
}



float NCD::compress(std::string filename, std::string filename2){
    std::string command = "";
    if (filename2 != ""){
        system(("convert " + filename + " " + filename2 + " -append " + "full.pgm").c_str());
        filename = "full.pgm";
    }
    if (filename == "full.pgm"){
        command = compressor + " " + filename;
    }
    else {
        command = compressor + " -k " + filename;
    }
    
    system((command).c_str());
    float size = GetFileSize(filename + ".gz");
    system("rm *.gz");
    return size;


}

float NCD::compute(std::string filename, std::string filename2) {

    float cxy = compress(filename, filename2);
    float cx = compress(filename);
    float cy = compress(filename2);

    std::cout << cxy << " - " <<  cx << " - " << cy << std::endl; 
    return ((cxy - (cx > cy ? cy : cx)) / (cx > cy ? cx : cy)); 

}