#include <fstream>
#include <iostream>
#include <filesystem>
#include <wav/wavfind.hpp>

using namespace std;

int main (int argc, char *argv[])
{
    if(argc < 5) {
		cerr << "Usage: wavfind <vector size> <overlap factor> <input file> <directiory>" << endl;
		return 1;
	}

    size_t vector_size = std::stoi(argv[1]);
    size_t overlap_factor = std::stoi(argv[2]);

    if (overlap_factor < 0 || overlap_factor >= vector_size)
    {
        cerr << "Error: overlap factor should be between [0, vector size[" << std::endl;
        return 1;
    }

    SndfileHandle sndFileIn{ argv[3] };
    if(sndFileIn.error()) {
		cerr << "Error: invalid input file" << endl;
		return 1;
    }

	if((sndFileIn.format() & SF_FORMAT_TYPEMASK) != SF_FORMAT_WAV) {
		cerr << "Error: file is not in WAV format" << endl;
		return 1;
	}

	if((sndFileIn.format() & SF_FORMAT_SUBMASK) != SF_FORMAT_PCM_16 && (sndFileIn.format() & SF_FORMAT_SUBMASK) != SF_FORMAT_PCM_U8) {
		cerr << "Error: file is not in PCM_16 or PCM_U8 format" << endl;
		return 1;
	}

	if (!std::filesystem::exists(argv[4]))
	{
		cerr << "Error: specified directory doesn't exist" << endl;
		return 1;
	}

    WAV::Find finder;
    std::vector<std::string> files;

    for (const auto &file : std::filesystem::directory_iterator(argv[4]))
    {
        WAV::Codebook &codebook = finder.add_codebook();
        files.emplace_back(file.path().c_str());
        std::ifstream stream(file.path().c_str(), std::ios::binary);
        stream >> codebook;
    }

    auto found = finder.find(vector_size, overlap_factor, sndFileIn);

    if (found.has_value())
        std::cout << "Original: " << files[found.value().index] << std::endl;
    else
    {
        cerr << "Error: an error occurred during processing" << endl;
        return 1;
    }

    return 0;    
}