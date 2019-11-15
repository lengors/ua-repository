#pragma once

#include <vector>
#include <map>

#include <sndfile.hh>

namespace WAV
{
    class Quant
    {
    public:
        explicit Quant (const size_t &, const size_t &, SndfileHandle &);
        explicit Quant (const size_t &, SndfileHandle &);

        const size_t &next (void);
        std::vector<short> &quantitization (void);

    private:
        SndfileHandle &fileHandle;
        std::vector<short> samples;
        size_t delta, buffer_size, frames;
    };
}