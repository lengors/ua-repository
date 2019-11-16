#include <wav/wavcmp.hpp>

#include <vector>
#include <cmath>

std::optional<std::tuple<float, unsigned>> WAV::compare(SndfileHandle &file, SndfileHandle &original, const size_t &buffer_size)
{
    if (file.channels() != original.channels())
        return {};
    int max = 0;
    using ld = long double;
    ld sum = 0, diff_sum = 0;
    const int channels = file.channels();
    std::vector<short> vector(buffer_size * channels);
    std::vector<short> original_vector(buffer_size * channels);
    while (size_t frames = file.readf(vector.data(), buffer_size))
    {
        size_t original_frames = original.readf(original_vector.data(), buffer_size);
        if (original_frames != frames)
            return {};
        for (unsigned i = 0; i < frames * channels; ++i)
        {
            short &value = vector[i];
            short &original_value = original_vector[i];
            sum += original_value * original_value;
            int diff = int(original_value) - int(value);
            max = std::max(max, std::abs(diff));
            diff_sum += diff * diff;
        }
    }
    return std::tuple<float, unsigned>({ 10 * std::log10(sum / diff_sum), max });
}