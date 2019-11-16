#pragma once

#include <optional>

#include <sndfile.hh>

namespace WAV
{
    std::optional<float> compare(SndfileHandle &, SndfileHandle &, const size_t & = 65536);
}