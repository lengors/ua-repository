#include <iostream>
#include <sndfile.hh>
#include <wav/wavcmp.hpp>

using namespace std;

int main(int argc, char *argv[]) {

	if(argc < 3) {
		cerr << "Usage: wavcmp <audio file> <original audio file>" << endl;
		return 1;
	}

	SndfileHandle sndFile { argv[argc-2] };
	if(sndFile.error()) {
		cerr << "Error: invalid audio file" << endl;
		return 1;
    }

    SndfileHandle originalSndFile { argv[argc-1] };
	if(originalSndFile.error()) {
		cerr << "Error: invalid original audio file" << endl;
		return 1;
    }

	if((sndFile.format() & SF_FORMAT_TYPEMASK) != SF_FORMAT_WAV) {
		cerr << "Error: audio file is not in WAV format" << endl;
		return 1;
	}

	if((sndFile.format() & SF_FORMAT_SUBMASK) != SF_FORMAT_PCM_16 && (sndFile.format() & SF_FORMAT_SUBMASK) != SF_FORMAT_PCM_U8) {
		cerr << "Error: audio file is not in PCM_16 or PCM_U8 format" << endl;
		return 1;
	}

    if((originalSndFile.format() & SF_FORMAT_TYPEMASK) != SF_FORMAT_WAV) {
		cerr << "Error: original audio file is not in WAV format" << endl;
		return 1;
	}

	if((originalSndFile.format() & SF_FORMAT_SUBMASK) != SF_FORMAT_PCM_16 && (originalSndFile.format() & SF_FORMAT_SUBMASK) != SF_FORMAT_PCM_U8) {
		cerr << "Error: original audio file is not in PCM_16 format or PCM_U8 format" << endl;
		return 1;
	}

    if (sndFile.frames() != originalSndFile.frames()) {
        cerr << "Error: audio file and original audio file have a different number of frames" << endl;
		return 1;
    }

    if (sndFile.samplerate() != originalSndFile.samplerate()) {
        cerr << "Error: audio file and original audio file have different sample rates" << endl;
		return 1;
    }

    if (sndFile.channels() != originalSndFile.channels()) {
        cerr << "Error: audio file and original audio file have a different number of channels" << endl;
		return 1;
    }

	cout << "Files have:" << endl;
	cout << '\t' << sndFile.frames() << " frames" << endl;
	cout << '\t' << sndFile.samplerate() << " samples per second" << endl;
	cout << '\t' << sndFile.channels() << " channels" << endl;

    std::optional<std::tuple<float, unsigned>> snrmax = WAV::compare(sndFile, originalSndFile);
    if (snrmax.has_value())
	{
		auto [snr, max] = snrmax.value();
        std::cout << "SNR: " << snr << std::endl;
        std::cout << "Maximum per sample absolute error: " << max << std::endl;

	}

	return 0;
}
