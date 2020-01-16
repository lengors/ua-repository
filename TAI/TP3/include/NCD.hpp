
#include <string>

class NCD
{

    private : 
        std::string compressor;

    public : 
        NCD();
        NCD(std::string compressor);

        float GetFileSize(std::string filename);

        float compress(std::string filename, std::string filename2 = "");
        

        // calcs NCD
        float compute(std::string filename, std::string filename2);
};