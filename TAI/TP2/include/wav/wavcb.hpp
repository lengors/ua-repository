#pragma once

#include <sndfile.hh>

#include <iostream>
#include <vector>

namespace WAV
{
    class Codebook;
}

std::ostream &operator<< (std::ostream &, const WAV::Codebook &);
std::istream &operator>> (std::istream &, WAV::Codebook &);

namespace WAV
{
    using Vector = std::vector<long double>;
    
    long double square_distance (const Vector &, const Vector &);
    
    class Codebook
    {
    public:
        Codebook (const size_t &, const size_t &, const size_t &, SndfileHandle &, const size_t & = 0, const size_t & = 65536);
        Codebook (void);

        std::pair<long double, const Vector &> closest (const Vector &) const;
        
        const unsigned &get_error_code (void) const;
        bool is_valid (void) const;

        friend std::ostream &(::operator<<) (std::ostream &, const Codebook &);
        friend std::istream &(::operator>>) (std::istream &, Codebook &);

        std::vector<Vector>::const_iterator begin (void) const;
        std::vector<Vector>::iterator begin (void);

        std::vector<Vector>::const_iterator end (void) const;
        std::vector<Vector>::iterator end (void);
    private:
        std::vector<Vector> codewords;
        unsigned valid;
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