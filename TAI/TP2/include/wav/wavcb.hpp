#pragma once

#include <sndfile.hh>

#include <iostream>
#include <vector>
#include <tuple>

namespace WAV
{
    class Codebook
    {
    public:
        explicit Codebook (const size_t &, const size_t &, const size_t &);
        explicit Codebook (const size_t &, const size_t &);

        std::tuple<unsigned, std::vector<std::vector<short>>> compute (SndfileHandle &, const size_t & = 0, const size_t & = 65536);
    private:
        size_t vector_size, offset, cluster_size;
    };
}

template<typename T>
std::ostream &operator<< (std::ostream &stream, const std::vector<T> &vector)
{
    stream << "(";
    for (unsigned i = 0; i < vector.size(); )
    {
        stream << vector[i++];
        if (i != vector.size())
            stream << ", ";
    }
    return stream << ")";
}