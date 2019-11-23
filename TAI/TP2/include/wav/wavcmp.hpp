#pragma once

#include <optional>
#include <tuple>

#include <sndfile.hh>

namespace WAV
{
    std::optional<std::tuple<float, unsigned>> compare(SndfileHandle &, SndfileHandle &, const size_t & = 65536);
}