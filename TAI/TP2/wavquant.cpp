#include "wavquant.hpp"
#include <cmath>
#include <iostream>

WAVQuant::WAVQuant (const size_t &bits, const size_t &buffer_size, SndfileHandle &fileHandle) :
    samples(buffer_size * fileHandle.channels()), fileHandle(fileHandle), delta(1 << (16 - bits)), buffer_size(buffer_size)
{
}

WAVQuant::WAVQuant (const size_t &bits, SndfileHandle &fileHandle) :
    WAVQuant(bits, 65536, fileHandle)
{
}

const size_t &WAVQuant::next (void)
{
    frames = fileHandle.readf(samples.data(), buffer_size);
    return frames;
}

std::vector<short> &WAVQuant::quantitization (void)
{
    using ld = long double;
    short *address = samples.data();
    short *end = address + frames * fileHandle.channels();
    while (address != end)
    {
        *address = (short) std::floor(ld(*address) / ld(delta)) * delta;
        ++address;
    }
    return samples;
}

using namespace std;
constexpr size_t FRAMES_BUFFER_SIZE = 65536; // Buffer for reading/writing frames

int main(int argc, char *argv[])
{

	if(argc < 4) {
		cerr << "Usage: wavcp <step> <input file> <output file>" << endl;
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

	SndfileHandle sndFileOut { argv[argc-1], SFM_WRITE, sndFileIn.format(),
	  sndFileIn.channels(), sndFileIn.samplerate() };
	if(sndFileOut.error()) {
		cerr << "Error: invalid output file" << endl;
		return 1;
    }

    WAVQuant quantitizer(bits, sndFileIn);
    while (size_t frames = quantitizer.next())
        sndFileOut.writef(quantitizer.quantitization().data(), frames);

	return 0;
}