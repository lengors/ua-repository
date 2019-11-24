#include <algorithm>
#include <iostream>
#include <vector>

#include <sndfile.hh>

using namespace std;

constexpr size_t FRAMES_BUFFER_SIZE = 65536; // Buffer for reading/writing frames

int main(int argc, char *argv[]) {

	if(argc < 3) {
		cerr << "Usage: wavcp <input file> <output file> [offset] [number_frames]" << endl;
		return 1;
	}

	SndfileHandle sndFileIn { argv[1] };
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

	int offset = 0;
	int number_frames = -1;

	if (argc >= 4)
		offset = stoi(argv[3]);
	
	if (argc >= 5)
		number_frames = stoi(argv[4]);

	cout << "Input file has:" << endl;
	cout << '\t' << sndFileIn.frames() << " frames" << endl;
	cout << '\t' << sndFileIn.samplerate() << " samples per second" << endl;
	cout << '\t' << sndFileIn.channels() << " channels" << endl;

	SndfileHandle sndFileOut { argv[2], SFM_WRITE, sndFileIn.format(),
	  sndFileIn.channels(), sndFileIn.samplerate() };
	if(sndFileOut.error()) {
		cerr << "Error: invalid output file" << endl;
		return 1;
    }

	size_t nFrames;
	vector<short> samples;
	short buffer[FRAMES_BUFFER_SIZE * sndFileIn.channels()];

	while (nFrames = sndFileIn.readf(buffer, FRAMES_BUFFER_SIZE))
		samples.insert(samples.end(), buffer, buffer + nFrames * sndFileIn.channels());

	number_frames = number_frames == -1 ? samples.size() / sndFileIn.channels() - offset : std::min(size_t(number_frames), samples.size() / sndFileIn.channels() - offset);
	sndFileOut.writef(samples.data() + offset * sndFileIn.channels(), number_frames);
	return 0;
}

