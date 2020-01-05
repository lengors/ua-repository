
#include <string>

class NCCD
{

    private : 
       std::string ctx_file;

    public : 
        NCCD();
        NCCD(std::string ctx_file);
        



        // calculates NCCD
        float compute(std::string filename, std::string* files);
        float compute(std::string filename, int id);
};