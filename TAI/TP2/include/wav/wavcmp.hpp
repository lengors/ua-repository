#pragma once

#include <optional>

#include <sndfile.hh>

namespace WAV
{
    std::optional<float> compare(const SndfileHandle &, const SndfileHandle &, const size_t & = 65536);
}