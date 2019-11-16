#include <wav/wavquant.hpp>

WAV::Quant::Quant (const size_t &bits, const size_t &buffer_size, SndfileHandle &fileHandle) :
    samples(buffer_size * fileHandle.channels()), fileHandle(fileHandle), delta(1 << (16 - bits)), buffer_size(buffer_size)
{
}

WAV::Quant::Quant (const size_t &bits, SndfileHandle &fileHandle) :
    Quant(bits, 65536, fileHandle)
{
}

const size_t &WAV::Quant::next (void)
{
    frames = fileHandle.readf(samples.data(), buffer_size);
    return frames;
}

std::vector<short> &WAV::Quant::quantization (void)
{
    using ld = long double;
    short *address = samples.data();
    short *end = address + frames * fileHandle.channels();
    while (address != end)
    {
        *address = (*address / delta) * delta;
        ++address;
    }
    return samples;
}