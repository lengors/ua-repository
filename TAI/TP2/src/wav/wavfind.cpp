#include <wav/wavfind.hpp>

#include <iostream>
#include <algorithm>

using ld = long double;

long double calculate_error (const std::vector<WAV::Vector> &blocks, const WAV::Codebook &codebook)
{
    long double error = 0;
    for (const WAV::Vector &block : blocks)
        error += codebook.closest(block).first;
    return error;
}

WAV::Codebook &WAV::Find::add_codebook (void)
{
    return codebooks.emplace_back();
}

std::optional<WAV::Find::Result> WAV::Find::find (const size_t &vector_size, const size_t &overlap_factor, SndfileHandle &sndfile_handle, const size_t &buffer_size)
{
    const size_t offset = vector_size - overlap_factor;

    if (offset == 0 || offset > vector_size)
        return {};

    const size_t size = buffer_size * sndfile_handle.channels();
    std::vector<short> samples;
    std::vector<short> buffer(size);
    
    while (size_t frames = sndfile_handle.readf(buffer.data(), buffer_size))
        samples.insert(samples.end(), buffer.begin(), buffer.begin() + frames * sndfile_handle.channels());

    std::vector<Vector> blocks;
    const size_t end = samples.size() - vector_size;
    for (unsigned i = 0; i < samples.size() - vector_size; i += offset)
    {
        Vector &block = blocks.emplace_back(vector_size);
        std::transform(samples.begin() + i, samples.begin() + i + vector_size, block.begin(), [](const auto &value) { return ld(value); });
    }

    Result result{ 0, 0, codebooks[0] };
    result.error = calculate_error(blocks, result.codebook);
    for (unsigned i = 1; i < codebooks.size(); ++i)
    {
        Codebook &codebook = codebooks[i];
        const long double error = calculate_error(blocks, codebook);
        if (error < result.error)
        {
            result.index = i;
            result.error = error;
            result.codebook = codebook;
        }
    }

    return result;
}