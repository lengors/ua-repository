#pragma once

#include <vector>
#include <map>

#include <sndfile.hh>

namespace WAV
{
	class Hist
	{
	private:
		std::vector<std::map<short, size_t>> counts;

	public:
		Hist (const SndfileHandle &);

		void update (const std::vector<short> &);

		void dump (const size_t &) const;
		void dump_average (void) const;
	};
}