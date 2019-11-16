#include <wav/wavcb.hpp>

WAV::Codebook::Codebook (const size_t &vector_size, const size_t &overlap_factor, const size_t &cluster_size) :
    vector_size(vector_size), offset(vector_size - overlap_factor), cluster_size(cluster_size)
{
}

WAV::Codebook::Codebook (const size_t &vector_size, const size_t &cluster_size) :
    vector_size(vector_size), offset(1), cluster_size(cluster_size)
{
}

std::tuple<unsigned, std::vector<std::vector<short>>> WAV::Codebook::compute (SndfileHandle &fileHandle, const size_t &buffer_size)
{
    if (offset == 0 || offset > vector_size)
        return { 1, std::vector<std::vector<float>>() };

    const size_t size = buffer_size * fileHandle.channels();
    std::vector<short> samples;
    std::vector<short> buffer(size);
    
    while (size_t frames = fileHandle.readf(buffer.data(), buffer_size))
        samples.insert(samples.end(), buffer.begin(), buffer.begin() + frames * fileHandle.channels());

    std::vector<std::vector<short>> blocks;
    const size_t end = samples.size() - vector_size;
    for (unsigned i = 0; i < samples.size() - vector_size; i += offset)
        blocks.emplace_back(std::vector(samples.begin() + i, samples.begin() + i + vector_size));

    if (blocks.size() < cluster_size)
        return { 2, std::vector<std::vector<float>>() };

    std::vector<std::vector<short>> cluster(blocks.begin(), blocks.end() + cluster_size);

    return  { 0, cluster };
}