#include <vector>
#include <iostream>
#include <sndfile.hh>
#include <wav/wavcb.hpp>

using namespace std;

int main(int argc, char *argv[])
{

	if(argc < 5) {
		cerr << "Usage: wavcb <vector size> <overlap factor> <cluster size> <audio file>" << endl;
		return 1;
	}

    size_t vector_size = std::stoi(argv[argc - 4]);
    size_t overlap_factor = std::stoi(argv[argc - 3]);

    if (overlap_factor < 0 || overlap_factor >= vector_size)
    {
        cerr << "Error: overlap factor should be between [0, vector size[" << std::endl;
        return 1;
    }

    size_t cluster_size = std::stoi(argv[argc - 2]);

	SndfileHandle sndFileIn { argv[argc - 1] };
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

	cout << "Input file has:" << endl;
	cout << '\t' << sndFileIn.frames() << " frames" << endl;
	cout << '\t' << sndFileIn.samplerate() << " samples per second" << endl;
	cout << '\t' << sndFileIn.channels() << " channels" << endl;

	WAV::Codebook codebook(vector_size, overlap_factor, cluster_size);

    auto [error_code, cluster] = codebook.compute(sndFileIn);

    if (error_code == 2)
    {
        cerr << "Error: cluster size bigger than the number of blocks" << std::endl;
        return 1;
    }

    for (const std::vector<short> &block : cluster)
        cout << block << endl;

	return 0;
}