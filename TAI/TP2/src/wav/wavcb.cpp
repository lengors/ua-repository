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

long double WAV::square_distance (const Vector &first, const Vector &second)
{
    long double distance = 0;
    for (unsigned i = 0; i < first.size(); ++i)
    {
        const long double diff = first[i] - second[i];
        distance += diff * diff;
    }
    return distance;
}

using ld = long double;
using block_t = std::vector<ld>;
using cluster_t = std::vector<WAV::Vector>;

auto key_selector = [](auto &pair) { return pair.first; };

WAV::Codebook::Codebook (const size_t &vector_size, const size_t &overlap_factor, const size_t &cluster_size, SndfileHandle &sndfile_handle, const size_t &max_iterations, const size_t &buffer_size)
{
    const size_t offset = vector_size - overlap_factor;

    if (offset == 0 || offset > vector_size)
    {
        valid = 1;
        return;
    }

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

    if (blocks.size() < cluster_size)
    {
        valid = 2;
        return;
    }

    valid = 0;
    if (blocks.size() == cluster_size)
        return;

    size_t iterations = 0;
    cluster_t keys(cluster_size);
    std::unordered_map<WAV::Vector, cluster_t> clusters(cluster_size);
    codewords = cluster_t(blocks.begin(), blocks.begin() + cluster_size);
    std::transform(clusters.begin(), clusters.end(), keys.begin(), key_selector);

    while (keys != codewords && (!max_iterations || iterations++ < max_iterations))
    {
        // clear clusters info
        clusters.clear();

        // calculate clusters
        for (const WAV::Vector &block : blocks)
        {
            std::vector<std::pair<ld, const WAV::Vector &>> distances;
            distances.reserve(codewords.size());
            for (const auto &centroid : codewords)
                distances.emplace_back(square_distance(block, centroid), centroid);
            const WAV::Vector &centroid = std::min_element(distances.begin(), distances.end(), [](const auto &centroid0, const auto &centroid1) { return centroid0.first < centroid1.first; })->second;
            std::unordered_map<WAV::Vector, cluster_t>::iterator it = clusters.find(centroid);
            if (it == clusters.end())
                clusters.emplace(centroid, cluster_t()).first->second.emplace_back(block);
            else
                it->second.emplace_back(block);
        }

        // clear centroids info
        codewords.clear();
        
        // recalculate centroids
        for (const auto &pair : clusters)
        {
            WAV::Vector &new_centroid = codewords.emplace_back(pair.first.size());
            for (unsigned i = 0; i < new_centroid.size(); ++i)
                new_centroid[i] = std::accumulate(pair.second.begin(), pair.second.end(), 0, [&i](const auto &result, const auto &block) { return result + block[i]; }) / ld(pair.second.size());
        }

        // updates keys
        std::transform(clusters.begin(), clusters.end(), keys.begin(), key_selector);
    }
}

WAV::Codebook::Codebook (void) :
    valid(3)
{
}

std::pair<long double, const WAV::Vector &> WAV::Codebook::closest (const WAV::Vector &vector) const
{
    const Vector *result = &codewords[0];
    long double mindistance = square_distance(vector, codewords[0]);
    for (unsigned i = 1; i < codewords.size(); ++i)
    {
        const Vector &codeword = codewords[i];
        const long double distance = square_distance(vector, codeword);
        if (distance < mindistance)
        {
            mindistance = distance;
            result = &codeword;
        }
    }
    return { mindistance, *result };
}

const unsigned &WAV::Codebook::get_error_code (void) const
{
    return valid;
}

bool WAV::Codebook::is_valid (void) const
{
    return !valid;
}

std::vector<WAV::Vector>::const_iterator WAV::Codebook::begin (void) const
{
    return codewords.begin();
}

std::vector<WAV::Vector>::iterator WAV::Codebook::begin (void)
{
    return codewords.begin();
}

std::vector<WAV::Vector>::const_iterator WAV::Codebook::end (void) const
{
    return codewords.end();
}

std::vector<WAV::Vector>::iterator WAV::Codebook::end (void)
{
    return codewords.end();
}

std::ostream &operator<< (std::ostream &stream, const WAV::Codebook &codebook)
{
    if (&stream == &std::cout)
        for (const WAV::Vector &block : codebook.codewords)
        {
            stream << "(";
            for (unsigned i = 0; i < block.size(); )
            {
                stream << block[i++];
                if (i != block.size())
                    stream << ", ";
            }
            stream << ")";
        }
    else
        for (const WAV::Vector &block : codebook)
        {
            auto size = block.size();
            stream.write(reinterpret_cast<const char *>(&size), sizeof(size));
            stream.write(reinterpret_cast<const char *>(block.data()), size * sizeof(long double));
        }
    return stream;
}

std::istream &operator>> (std::istream &stream, WAV::Codebook &codebook)
{
    codebook.codewords.clear();

    // positions cursor at the end of file
    stream.seekg(0, std::ios::end);

    // gets eof position
    std::streampos eof = stream.tellg();

    // resets cursor position
    stream.seekg(0, std::ios::beg);

    size_t block_size;

    while (stream.tellg() != eof)
    {
        stream.read(reinterpret_cast<char *>(&block_size), sizeof(block_size));
        WAV::Vector &block = codebook.codewords.emplace_back(block_size);
        stream.read(reinterpret_cast<char *>(block.data()), block.size() * sizeof(long double));
    }

    return stream;
}