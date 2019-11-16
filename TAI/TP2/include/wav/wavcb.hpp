#pragma once

#include <sndfile.hh>

#include <iostream>
#include <vector>

namespace WAV
{
    class Codebook
    {
    public:
        explicit Codebook (const size_t &, const size_t &, const size_t &);
        explicit Codebook (const size_t &, const size_t &);

        std::vector<std::vector<short>> compute (SndfileHandle &, const size_t & = 65536);
    private:
        size_t block_size, offset, cluster_size;
    };
}

template<typename T>
std::ostream &operator<< (std::ostream &stream, const std::vector<T> &vector)
{
    stream << "(";
    for (unsigned i = 0; i < vector.size(); ++i)
    {
        stream << value;
        if (i != vector.size() - 1)
            stream << ", "
    }
    return stream << ")";
}