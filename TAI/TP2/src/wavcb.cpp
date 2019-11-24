#include <mutex>
#include <vector>
#include <future>
#include <fstream>
#include <iostream>
#include <experimental/filesystem>

#include <sndfile.hh>
#include <wav/wavcb.hpp>

using namespace std;
namespace fs = std::experimental::filesystem;

static std::mutex m_Mutex;

void process_file (const size_t vector_size, const size_t overlap_factor, const size_t cluster_size, const fs::path input, const fs::path output, const size_t max_iterations)
{
	SndfileHandle sndFileIn { input.c_str() };

	if(sndFileIn.error()) {
		cerr << "Error: invalid input file" << endl;
		exit(1);
    }

	if((sndFileIn.format() & SF_FORMAT_TYPEMASK) != SF_FORMAT_WAV) {
		cerr << "Error: file is not in WAV format" << endl;
		exit(1);
	}

	if((sndFileIn.format() & SF_FORMAT_SUBMASK) != SF_FORMAT_PCM_16 && (sndFileIn.format() & SF_FORMAT_SUBMASK) != SF_FORMAT_PCM_U8) {
		cerr << "Error: file is not in PCM_16 or PCM_U8 format" << endl;
		exit(1);
	}

	{
		std::lock_guard<std::mutex> lock(m_Mutex);
		cout << "Input file (" << input.c_str() << ") has:" << endl;
		cout << '\t' << sndFileIn.frames() << " frames" << endl;
		cout << '\t' << sndFileIn.samplerate() << " samples per second" << endl;
		cout << '\t' << sndFileIn.channels() << " channels" << endl;
	}

	WAV::Codebook codebook(vector_size, overlap_factor, cluster_size, sndFileIn, max_iterations);
    
	if (codebook.get_error_code() == 2)
    {
        cerr << "Error: cluster size bigger than the number of blocks" << std::endl;
        exit(1);
    }
	
	{
		std::ofstream ostream(output.c_str(), std::ios::binary);
		ostream << codebook;
	}

	{
		std::lock_guard<std::mutex> lock(m_Mutex);
		std::cout << output.c_str() << " created!" << std::endl;
	}
}

int main(int argc, char *argv[])
{

	if(argc < 6) {
		cerr << "Usage: wavcb <vector size> <overlap factor> <cluster size> <input file/directory> <output file/directiory> [max iterations]" << endl;
		return 1;
	}

    size_t vector_size = std::stoi(argv[1]);
    size_t overlap_factor = std::stoi(argv[2]);

    if (overlap_factor < 0 || overlap_factor >= vector_size)
    {
        cerr << "Error: overlap factor should be between [0, vector size[" << std::endl;
        return 1;
    }

    size_t cluster_size = std::stoi(argv[3]);

	if (!fs::exists(argv[4]))
	{
		cerr << "Error: specified path doesn't exist" << endl;
		return 1;
	}

	size_t max_iterations = argc == 6 ? 0 : std::stoi(argv[6]);

	if (fs::is_directory(argv[4]))
	{
		if (fs::exists(argv[5]) && !fs::is_directory(argv[5]))
		{
			cerr << "Error: specified output path is not a directory" << endl;
			return 1;
		}
		else if (!fs::exists(argv[5]))
			fs::create_directory(argv[5]);
        std::vector<std::pair<fs::path, fs::path>> paths;
		for (const auto &file : fs::directory_iterator(argv[4]))
		{
			fs::path output_path = argv[5];
			output_path /= file.path().filename();
			output_path.replace_extension(".cdb");
			paths.emplace_back(file.path(), output_path);
		}
		
		std::vector<std::future<void>> futures;
		for (const auto &entries : paths)
			futures.push_back(std::async(std::launch::async, process_file, vector_size, overlap_factor, cluster_size, entries.first, entries.second, max_iterations));
	}
	else
		process_file(vector_size, overlap_factor, cluster_size, argv[4], argv[5], max_iterations);


	return 0;
}