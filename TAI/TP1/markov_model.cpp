// this file contains the implementation of the MarkovModel class
#include "markov_model.hpp"

#include <functional>
#include <algorithm>
#include <iostream>
#include <numeric>

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
    Event(character, 1)
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

        for (int i = 0; i < content.length() - model.k; ++i)
        {
            // bool exist = false; <- not needed in current implementation
            char event_character = content[i + model.k];
            std::string text = content.substr(i, model.k);

            // this is the same as text = content.substr(i, model.k);
            /*for (int j = 0; j < model.k; j++)
                text += content[i + j];*/

            // reference to events of given sequence
            std::vector<MarkovModel::Event> &events = model.frequency[text];

            // tries to find an event with a given character [same as the for loop]
            std::vector<MarkovModel::Event>::iterator finding = std::find_if(events.begin(), events.end(),
                [&event_character](const MarkovModel::Event &event) { return event_character == event.get_character(); }); // <- this is a lambda, recommended reading:
                                                                                                                     // https://pt.cppreference.com/w/cpp/language/lambda

            // if event not found
            // if character already exists in a given context
            // then it already exists in the alphabet
            if (finding == events.end())
            {
                model.frequency[text].emplace_back(event_character);
                model.alphabet.emplace(event_character);
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

        // remaining letters
        for (int i = 0; i < model.k; ++i)
            model.alphabet.emplace(content[i]);
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
            std::vector<MarkovModel::Event> events;
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
    ostream << write(model.k) << write(model.alpha) << write(model.alphabet.size());
    for (const auto &letter : model.alphabet)
        ostream << write(letter);
    for (const auto &context : model.frequency)
    {
        ostream << write(context.first) << write(context.second.size());
        for (const auto &event : context.second)
            ostream << write(event.get_character()) << write(event.get_count());
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

float MarkovModel::get_probability(const MarkovModel::Context &context, const MarkovModel::Event &event) const
{
    const std::vector<MarkovModel::Event> &events = context.second;
    unsigned total = std::accumulate(events.begin(), events.end(), 0u, [](unsigned &accumulate, const MarkovModel::Event &event) { return accumulate + event.get_count(); });
    return float(event.get_count() + alpha) / float(total + alpha * alphabet.size());
}

float MarkovModel::get_entropy()
{
    return std::log2(frequency.size());
}
