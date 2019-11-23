#pragma once

#include <vector>
#include <optional>

#include <sndfile.hh>
#include <wav/wavcb.hpp>

namespace WAV
{
    class Find
    {
    public:
        Codebook &add_codebook (void);
        std::optional<std::pair<unsigned, Codebook &>> find (const size_t &, const size_t &, SndfileHandle &, const size_t & = 65536);
    private:
        std::vector<Codebook> codebooks;
    };
}