#pragma once

#include <vector>
#include <map>

#include <sndfile.hh>

class WAVHist
{
private:
	std::vector<std::map<short, size_t>> counts;

public:
	WAVHist (const SndfileHandle &);

	void update (const std::vector<short> &);

	void dump (const size_t &) const;
	void dump_average (void) const;
};