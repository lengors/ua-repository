#include <wav/wavquant.hpp>

#include <cmath>

WAV::Quant::Quant (const size_t &bits, const size_t &buffer_size, SndfileHandle &fileHandle) :
    samples(buffer_size * fileHandle.channels()), fileHandle(fileHandle), delta(1 << (16 - bits)), buffer_size(buffer_size)
{
}

WAV::Quant::Quant (const size_t &bits, SndfileHandle &fileHandle) :
    WAVQuant(bits, 65536, fileHandle)
{
}

const size_t &WAV::Quant::next (void)
{
    frames = fileHandle.readf(samples.data(), buffer_size);
    return frames;
}

std::vector<short> &WAV::Quant::quantitization (void)
{
    using ld = long double;
    short *address = samples.data();
    short *end = address + frames * fileHandle.channels();
    while (address != end)
    {
        *address = (short) std::floor(ld(*address) / ld(delta)) * delta;
        ++address;
    }
    return samples;
}