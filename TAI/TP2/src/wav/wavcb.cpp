#include <wav/wavcb.hpp>

#include <numeric>
#include <algorithm>
#include <functional>
#include <unordered_map>

namespace std
{
    template<typename T>
    class hash;

    template<typename T>
    class hash<std::vector<T>>
    {
    public:
        std::size_t operator() (const std::vector<T> &vector) const
        {
            size_t value = 0;
            std::hash<T> hashing;
            for (unsigned i = 0; i < vector.size(); ++i)
                value += hashing(vector[i]) * i;
            return value;
        }
    };
}

using ld = long double;
using block_t = std::vector<ld>;
using cluster_t = std::vector<block_t>;

auto key_selector = [](auto &pair) { return pair.first; };

size_t square_distance(const block_t &first, const block_t &second)
{
    size_t distance = 0;
    for (unsigned i = 0; i < first.size(); ++i)
    {
        const size_t value = size_t(second[i]) - size_t(first[i]);
        distance += value * value;
    }
    return distance;
}

WAV::Codebook::Codebook (const size_t &vector_size, const size_t &overlap_factor, const size_t &cluster_size) :
    vector_size(vector_size), offset(vector_size - overlap_factor), cluster_size(cluster_size)
{
}

WAV::Codebook::Codebook (const size_t &vector_size, const size_t &cluster_size) :
    vector_size(vector_size), offset(1), cluster_size(cluster_size)
{
}

std::tuple<unsigned, cluster_t> WAV::Codebook::compute (SndfileHandle &fileHandle, const size_t &max_iterations, const size_t &buffer_size)
{
    if (offset == 0 || offset > vector_size)
        return { 1, cluster_t() };

    const size_t size = buffer_size * fileHandle.channels();
    std::vector<short> samples;
    std::vector<short> buffer(size);
    
    while (size_t frames = fileHandle.readf(buffer.data(), buffer_size))
        samples.insert(samples.end(), buffer.begin(), buffer.begin() + frames * fileHandle.channels());

    std::vector<block_t> blocks;
    const size_t end = samples.size() - vector_size;
    for (unsigned i = 0; i < samples.size() - vector_size; i += offset)
    {
        block_t &block = blocks.emplace_back(vector_size);
        std::transform(samples.begin() + i, samples.begin() + i + vector_size, block.begin(), [](const auto &value) { return ld(value); });
    }

    if (blocks.size() < cluster_size)
        return { 2, cluster_t() };

    if (blocks.size() == cluster_size)
        return { 0, cluster_t(blocks.begin(), blocks.begin() + cluster_size) };

    size_t iterations = 0;
    cluster_t keys(cluster_size);
    std::unordered_map<block_t, cluster_t> clusters(cluster_size);
    cluster_t centroids(blocks.begin(), blocks.begin() + cluster_size);
    std::transform(clusters.begin(), clusters.end(), keys.begin(), key_selector);

    while (keys != centroids && (!max_iterations || iterations++ < max_iterations))
    {
        // clear clusters info
        clusters.clear();

        // calculate clusters
        for (const block_t &block : blocks)
        {
            std::vector<std::pair<size_t, const block_t &>> distances;
            distances.reserve(centroids.size());
            for (const auto &centroid : centroids)
                distances.emplace_back(square_distance(block, centroid), centroid);
            const block_t &centroid = std::min_element(distances.begin(), distances.end(), [](const auto &centroid0, const auto &centroid1) { return centroid0.first < centroid1.first; })->second;
            std::unordered_map<block_t, cluster_t>::iterator it = clusters.find(centroid);
            if (it == clusters.end())
                clusters.emplace(centroid, cluster_t()).first->second.emplace_back(block);
            else
                it->second.emplace_back(block);
        }

        // clear centroids info
        centroids.clear();
        
        // recalculate centroids
        for (const auto &pair : clusters)
        {
            block_t &new_centroid = centroids.emplace_back(pair.first.size());
            for (unsigned i = 0; i < new_centroid.size(); ++i)
                new_centroid[i] = std::accumulate(pair.second.begin(), pair.second.end(), 0, [&i](const auto &block) { return block[i]; }) / ld(pair.second.size());
        }

        // updates keys
        std::transform(clusters.begin(), clusters.end(), keys.begin(), key_selector);
    }

    return  { 0, centroids };
}