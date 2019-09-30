// this file contains the implementation of the MarkovModel class
#include "markov_model.hpp"

#include <functional>
#include <algorithm>
#include <iostream>
#include <numeric>
#include <random>
#include <chrono>

// using namespace std; <- not recommended, may create ambiguity

// this and the "write" function are used to write bytes to stream
inline std::ostream &operator<< (std::ostream &stream, const std::function<std::ostream &(std::ostream &)> &function)
{
    return function(stream);
}

template<typename T>
inline T operator>> (std::istream &stream, const std::function<T (std::istream &)> &function)
{
    return function(stream);
}

template<typename T>
inline auto operator>> (const T &value, std::unordered_set<T> &set)
{
    return set.emplace(value);
}

inline std::function<std::ostream &(std::ostream &)> write (const std::string &value)
{
    return [&value](std::ostream &stream) -> std::ostream & { return stream.write(value.data(), value.size()); };
}

template<typename T>
inline std::function<std::ostream &(std::ostream &)> write (const T &value)
{
    return [&value](std::ostream &stream) -> std::ostream & { return stream.write(reinterpret_cast<const char *>(&value), sizeof(T)); };
}

inline std::function<std::istream &(std::istream &)> read (std::string &value, const unsigned &size)
{
    return [&value, &size](std::istream &stream) -> std::istream & { return stream.read((char *) value.data(), size); };
}

template<typename T>
inline std::function<std::istream &(std::istream &)> read (T &value)
{
    return [&value](std::istream &stream) -> std::istream & { return stream.read(reinterpret_cast<char *>(&value), sizeof(T)); };
}

template<typename T>
inline std::function<T(std::istream &)> read ()
{
    return [](std::istream &stream) -> T
    {
        T value;
        stream.read(reinterpret_cast<char *>(&value), sizeof(T));
        return value;
    };
}

MarkovModel::Event::Event(const char &character, const unsigned &count) :
    character(character), count(count)
{
}

MarkovModel::Event::Event(const char &character) :
    Event(character, 0)
{
}

unsigned MarkovModel::Event::operator+(const MarkovModel::Event &other) const
{
    return count + other.count;
}

MarkovModel::Event &MarkovModel::Event::operator++ (void)
{
    ++count;
    return *this;
}

// constructor
MarkovModel::MarkovModel (const unsigned &k, const unsigned &alpha) :
    k(k), alpha(alpha)
{
}

// constructor
MarkovModel::MarkovModel (void) :
    k(0)
{
}

// destructor
MarkovModel::~MarkovModel (void)
{
}

// reads file and builds model
MarkovModel &operator>> (std::istream &istream, MarkovModel &model)
{
    // resets alphabet
    model.alphabet.clear();

    // resets frequency
    model.frequency.clear();

    // positions cursor at the end of file
    istream.seekg(0, std::ios::end);

    // gets eof position
    std::streampos eof = istream.tellg();

    // resets cursor position
    istream.seekg(0, std::ios::beg);

    if (model.k != 0)
    {
        // creates string
        std::string content;

        // resizes string to the value of the cursor position
        // this line in conjunction with the previous one
        // creates a string with the same number of characters
        // as the ones in the filestream
        content.resize(eof);

        // reads file into string from cursor position
        istream.read((char *) content.data(), content.size());

        // creates alphabet
        for (const auto &letter : content)
            model.alphabet.emplace(letter);

        for (int i = 0; i < content.length() - model.k; ++i)
        {
            // bool exist = false; <- not needed in current implementation
            char event_character = content[i + model.k];
            std::string text = content.substr(i, model.k);

            // this is the same as text = content.substr(i, model.k);
            /*for (int j = 0; j < model.k; j++)
                text += content[i + j];*/

            // tries to find key
            MarkovModel::Frequency::iterator &iterator = model.frequency.find(text);

            // if map doesn't contain key, then initializes vector
            if (iterator == model.frequency.end())
            {
                auto pair = model.frequency.emplace(text, MarkovModel::Events());
                iterator = pair.first;
                for (const auto &letter : model.alphabet)
                    iterator->second.emplace_back(letter);
            }

            // reference to events of given sequence
            MarkovModel::Events &events = iterator->second;

            // tries to find an event with a given character [same as the for loop]
            MarkovModel::Events::iterator finding = std::find_if(events.begin(), events.end(),
                [&event_character](const MarkovModel::Event &event) { return event_character == event.get_character(); }); // <- this is a lambda, recommended reading:
                                                                                                                     // https://pt.cppreference.com/w/cpp/language/lambda

            // if event not found
            // if character already exists in a given context
            // then it already exists in the alphabet
            if (finding == events.end())
            {
                std::cerr << "Error: character not found!" << std::endl;
                std::exit(1);
            }
            else
                finding->operator++();

            /*for (auto &other_event : model.frequency[text])
                if (other_event.character == event_character)
                {
                    other_event.count++;
                    exist = true;
                    break;
                }

            MarkovModel::Event event;
            if (!exist)
            {
                event.count = 1;
                model.frequency[text].push_back(event);
            } -> same as the previous lines but with enhanced use of the standard library*/
        }
    }
    else
    {
        std::size_t reserve_size;
        istream >> read(model.k) >> read(model.alpha) >> read(reserve_size);
        model.alphabet.reserve(reserve_size);
        while (reserve_size--)
            istream >> read<char>() >> model.alphabet;
        while (istream.tellg() != eof)
        {
            std::string sequence;
            MarkovModel::Events events;
            sequence.resize(model.k);
            istream >> read(sequence, model.k) >> read(reserve_size);
            events.reserve(reserve_size);
            while (reserve_size--)
            {
                char character;
                unsigned count;
                istream >> read(character) >> read(count); 
                events.emplace_back(character, count);
            }
            model.frequency.emplace(sequence, events);
        }
    }

    return model;
}

std::ostream &operator<< (std::ostream &ostream, const MarkovModel &model)
{   
    if (&ostream == &std::cout)
    {
        ostream << " Text total appearances " << std::endl;
        for (const auto &context : model)
        {
            ostream << context.first << "-";
            for (auto &event : context.second)
                ostream << "[" << event.get_character() << "," << event.get_count() << "]" << ", ";
            ostream << ";\n";
        }
        ostream << " Conditional Probability " << std::endl;
        for (const auto &context : model)
            for (auto &event : context.second)
                ostream << context.first << " followed by " << event.get_character() << ":" << model.get_probability(context, event) << std::endl;
        ostream << model.get_entropy();
    }
    else
    {
        ostream << write(model.k) << write(model.alpha) << write(model.alphabet.size());
        for (const auto &letter : model.alphabet)
            ostream << write(letter);
        for (const auto &context : model.frequency)
        {
            ostream << write(context.first) << write(context.second.size());
            for (const auto &event : context.second)
                ostream << write(event.get_character()) << write(event.get_count());
        }
    }
    return ostream;
}

/*void MarkovModel::analyze (void)
{
    std::cout << " Text total appearances " << std::endl;
    for (auto it = tableMap.begin(); it != tableMap.end(); ++it)
    {
        std::cout << it->first << "-";
        for (auto &symbol : tableMap[it->first])
        {
            std::cout << "[" << symbol.c << "," << symbol.count << "]"
                      << ", ";
        }
        std::cout << ";\n";
    }
    std::cout << " Conditional Probability " << std::endl;

    for (auto it = tableMap.begin(); it != tableMap.end(); ++it)
    {
        for (auto &obj : tableMap[it->first])
        {
            int count = 0;
            for (auto &obj2 : tableMap[it->first])
                count += obj2.count;
            std::cout << it->first << " followed by " << obj.c << ":" << ((float)obj.count + alpha) / ((alpha * frequency.size()) + count) << std::endl;
        }
    }
}*/

/*void MarkovModel::writeToFile(std::string filename)
{
    std::ofstream tempfile;
    tempfile.open("output.txt");
    tempfile << "k = " << k << "\n";
    tempfile << "alpha = " << alpha << "\n";
    tempfile << "\n";
    for (auto &it : frequency)
    {
        tempfile << it.first << " - " << it.second << "\n";
    }
    tempfile << "\n";

    // for (auto& str : data){
    //     tempfile << str.text << " - " << str.c << " - " << str.count << "\n";
    // }
}*/

unsigned MarkovModel::get_total (const MarkovModel::Frequency &frequency)
{
    return std::accumulate(frequency.begin(), frequency.end(), 0u, [](unsigned &accumulate, const Context &context) { return accumulate + get_total(context); });
}

unsigned MarkovModel::get_total (const MarkovModel::Context &context)
{
    return std::accumulate(context.second.begin(), context.second.end(), 0u, [](unsigned &accumulate, const Event &event) { return accumulate + event.get_count(); });
}

std::string MarkovModel::generate_text (const unsigned &size) const
{
    float random;

    // Result
    std::string text;

    // Get current time
    auto time = std::chrono::high_resolution_clock::now();
    unsigned duration = std::chrono::duration_cast<std::chrono::milliseconds>(time.time_since_epoch()).count();

    // Setup for random generator
    std::default_random_engine generator;
    std::uniform_real_distribution<float> real_distribution(0, 1);
    generator.seed(duration);

    // This three lines create a vector with all existing contexts
    // and their respective probability
    unsigned total = get_total(frequency);
    std::vector<std::pair<std::string, float>> keys(frequency.size());
    std::transform(frequency.begin(), frequency.end(), keys.begin(), [&total](auto pair) { return std::pair(pair.first, float(get_total(pair)) / float(total)); });
    
    // prepares vector of contexts to choose a random context
    // this is done by ordering the vector in descending order
    std::sort(keys.begin(), keys.end(), [](auto key0, auto key1) { return key0.second > key1.second; });

    // Get random number
    random = real_distribution(generator);

    // Gets the appropiate key based on the random number
    std::vector<std::pair<std::string, float>>::reverse_iterator keys_riterator = keys.rbegin();
    for (; random > keys_riterator->second; ++keys_riterator)
        random -= keys_riterator->second;

    // initializes text based on random context
    text += keys_riterator->first.substr(0, size);

    if (text.size() < size)
    {
        // Setup for alphabet and random generator for alphabet
        std::vector<char> alphabet(this->alphabet.begin(), this->alphabet.end());
        std::uniform_int_distribution<int> int_distribution(0, alphabet.size() - 1);
        do
        {   
            // Tries to get list of events based on current context
            Frequency::const_iterator iterator = frequency.find(text.substr(text.size() - k, k));

            // If current context isn't mapped
            // add random character
            if (iterator == frequency.end())
                text += alphabet[int_distribution(generator)];
            else
            {
                // Get context
                const Context context(iterator->first, iterator->second);
                
                // Creates vector with all events for given context
                std::vector<std::pair<char, float>> events(iterator->second.size());
                std::transform(iterator->second.begin(), iterator->second.end(), events.begin(),
                    [&context, this](const Event &event) { return std::pair(event.get_character(), get_probability(context, event)); });

                // prepares vector of events to choose a random event
                // this is done by ordering the vector in descending order
                std::sort(events.begin(), events.end(), [](auto event0, auto event1) { return event0.second > event1.second; });
                
                // Get random number
                random = real_distribution(generator);
                
                // Get the appropriate character based on the random number
                std::vector<std::pair<char, float>>::reverse_iterator events_riterator = events.rbegin();
                for (; random > events_riterator->second; ++events_riterator)
                    random -= events_riterator->second;

                // Adds that character to the text
                text += events_riterator->first;
            }
        }
        while (text.size() < size);
    }

    return text;
}

float MarkovModel::get_probability(const MarkovModel::Context &context, const MarkovModel::Event &event) const
{
    return float(event.get_count() + alpha) / float(get_total(context) + alpha * alphabet.size());
}

float MarkovModel::get_entropy() const
{
    float entropy = 0;
    unsigned total = get_total(frequency);
    for (const Context &context : frequency)
    {
        float prob = 0;
        unsigned context_total = get_total(context);
        for (const Event &event : context.second)
        {
            float event_prob = float(event.get_count() + alpha) / float(context_total + alpha * alphabet.size());
            prob += event_prob * std::log(event_prob);
        }
        entropy += prob * float(context_total) / float(total);
    }
    return -entropy;
}
