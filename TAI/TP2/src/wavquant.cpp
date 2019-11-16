#include <iostream>
#include <sndfile.hh>
#include <wav/wavquant.hpp>

using namespace std;

int main(int argc, char *argv[])
{

	if(argc < 4) {
		cerr << "Usage: wavcp <bits> <input file> <output file>" << endl;
		return 1;
	}

    size_t bits = std::stoi(argv[argc - 3]);

	SndfileHandle sndFileIn { argv[argc-2] };
	if(sndFileIn.error()) {
		cerr << "Error: invalid input file" << endl;
		return 1;
    }

	if((sndFileIn.format() & SF_FORMAT_TYPEMASK) != SF_FORMAT_WAV) {
		cerr << "Error: file is not in WAV format" << endl;
		return 1;
	}

	if((sndFileIn.format() & SF_FORMAT_SUBMASK) != SF_FORMAT_PCM_16) {
		cerr << "Error: file is not in PCM_16 format" << endl;
		return 1;
	}

	cout << "Input file has:" << endl;
	cout << '\t' << sndFileIn.frames() << " frames" << endl;
	cout << '\t' << sndFileIn.samplerate() << " samples per second" << endl;
	cout << '\t' << sndFileIn.channels() << " channels" << endl;

	SndfileHandle sndFileOut { argv[argc-1], SFM_WRITE, SF_FORMAT_WAV | SF_FORMAT_PCM_U8,
	  sndFileIn.channels(), sndFileIn.samplerate() };
	if(sndFileOut.error()) {
		cerr << "Error: invalid output file" << endl;
		return 1;
    }

    WAV::Quant quantitizer(bits, sndFileIn);
    while (size_t frames = quantitizer.next())
        sndFileOut.writef(quantitizer.quantization().data(), frames);

	return 0;
}