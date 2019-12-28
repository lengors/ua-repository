#include <string>

class NCCD
{

    

    public : 
        NCCD();
        

        float GetFileSize(std::string filename);

        float compress(std::string filename, std::string filename2 = "");
        // calcs NCD
        float compute(std::string filename, std::string filename2);
};