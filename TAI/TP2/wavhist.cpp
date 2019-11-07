#include <wavhist.hpp>

WAVHist::WAVHist(const SndFileHandle &sfh)
{
    counts.resize(sfh.channels());
}

void WAVHist::update(const std::vector<short> &samples)
{
    size_t n = 0;
    for (const short &sample : samples)
        ++counts[n++ % counts.size()][sample]
}

void WAVHist::dump(const size_t &channel) const
{
    for (auto [value, counter] : counts[channel])
        std::cout << value << "\t" << counter << std::endl;
}

void WAVHist::dump_average(void) const
{
    std::map<short, std::size_t> average_counts;
    for (const auto &channel_counts : counts)
        for (auto [value, counter] : channel_counts)
            average_counts[value] += counter
    for (auto [value, counter] : average_counts)
        std::cout << value << "\t" << float(counter) / float(counts.size()) << std::endl;
}