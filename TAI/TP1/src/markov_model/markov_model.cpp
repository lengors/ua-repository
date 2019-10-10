// this file contains the implementation of the MarkovModel class
#include <markov_model/markov_model.hpp>

#include <unordered_set>
#include <functional>
#include <algorithm>
#include <iostream>
#include <numeric>
#include <random>
#include <chrono>

// this and the "write" functions are used to write bytes to a stream
inline std::ostream &operator<< (std::ostream &stream, const std::function<std::ostream &(std::ostream &)> &function)
{
    return function(stream);
}

// this and the "read" functions are used to read bytes from a stream
template<typename T>
inline T operator>> (std::istream &stream, const std::function<T (std::istream &)> &function)
{
    return function(stream);
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

// event constructor
MarkovModel::Event::Event (const char &character, const unsigned &count) :
    character(character), count(count)
{
}

// event constructor
MarkovModel::Event::Event (const char &character) :
    Event(character, 0)
{
}

// "sum" two events
unsigned MarkovModel::Event::operator+ (const MarkovModel::Event &other) const
{
    return count + other.count;
}

// increase event count
MarkovModel::Event &MarkovModel::Event::operator++ (void)
{
    ++count;
    return *this;
}

MarkovModel::MarkovModel (const MarkovModel &model, const std::string &text) :
    k(model.k), alpha(model.alpha), alphabet(model.alphabet)
{
    // builds model from text
    build_model(text);
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

// builds model from text
void MarkovModel::build_model (std::string content)
{
    // remove all null characters
    content.erase(std::remove(content.begin(), content.end(), '\0'), content.end());

    // creates alphabet
    for (const auto &letter : content)
        if (alphabet.find(letter) == alphabet.end())
            alphabet.emplace(letter, float(std::count(content.begin(), content.end(), letter)) / float(content.size()));

    for (int i = 0; i < content.length() - k; ++i)
    {
        // bool exist = false; <- not needed in current implementation
        char event_character = content[i + k];
        std::string text = content.substr(i, k);

        // tries to find key
        // MarkovModel::Frequency::iterator &iterator = model.frequency.find(text);
        // The code above evokes an error, cannot bind non const lvalue reference
        MarkovModel::Frequency::iterator iterator = frequency.find(text);

        // if map doesn't contain key, then initializes vector
        if (iterator == frequency.end())
        {
            auto pair = frequency.emplace(text, MarkovModel::Events());
            iterator = pair.first;
            for (const auto &letter : alphabet)
                iterator->second.emplace_back(letter.first);
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
    }
}

// reads file and builds model/loads model
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
        // reads model
        // creates string
        std::string content;

        // resizes string to the value of the cursor position
        // this line in conjunction with the previous one
        // creates a string with the same number of characters
        // as the ones in the filestream
        content.resize(eof);

        // reads file into string from cursor position
        istream.read((char *) content.data(), content.size());

        // builds model from text
        model.build_model(content);        
    }
    else
    {
        // loads model from file
        std::size_t reserve_size;
        istream >> read(model.k) >> read(model.alpha) >> read(reserve_size);
        model.alphabet.reserve(reserve_size);
        while (reserve_size--)
        {
            float prob;
            char letter;
            istream >> read(letter) >> read(prob);
            model.alphabet.emplace(letter, prob);
        }
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
    // checks if stream is the standard output,
    // and if so writes as string else writes in binary
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
        ostream << "Entropy: " << model.get_entropy();
    }
    else
    {
        ostream << write(model.k) << write(model.alpha) << write(model.alphabet.size());
        for (const auto &letter : model.alphabet)
            ostream << write(letter.first) << write(letter.second);
        for (const auto &context : model.frequency)
        {
            ostream << write(context.first) << write(context.second.size());
            for (const auto &event : context.second)
                ostream << write(event.get_character()) << write(event.get_count());
        }
    }
    return ostream;
}

unsigned MarkovModel::get_total (const MarkovModel::Frequency &frequency)
{
    return std::accumulate(frequency.begin(), frequency.end(), 0u, [](auto &accumulate, auto &context) { return accumulate + get_total(context); });
}

unsigned MarkovModel::get_total (const MarkovModel::Context &context)
{
    return std::accumulate(context.second.begin(), context.second.end(), 0u, [](auto &accumulate, auto &event) { return accumulate + event.get_count(); });
}

std::string MarkovModel::generate_text (const unsigned &max_size, const std::string &initial_text) const
{
    float random;

    // Result
    std::string text = initial_text;

    // Get current time
    auto time = std::chrono::high_resolution_clock::now();
    unsigned duration = unsigned(std::chrono::duration_cast<std::chrono::milliseconds>(time.time_since_epoch()).count());

    // Setup for random generator
    std::default_random_engine generator;
    std::uniform_real_distribution<float> real_distribution(0, 1);
    generator.seed(duration);

    if (text.size() == 0)
    {
        // This three lines create a vector with all existing contexts
        // and their respective probability
        unsigned total = get_total(frequency);
        std::vector<std::pair<std::string, float>> keys(frequency.size());
        std::transform(frequency.begin(), frequency.end(), keys.begin(), [&total](auto pair) { return std::pair(pair.first, float(get_total(pair)) / float(total)); });

        // prepares vector of contexts to choose a random context
        // this is done by ordering the vector in descending order
        std::sort(keys.begin(), keys.end(), [](auto &key0, auto &key1) { return key0.second > key1.second; });

        // Get random number
        random = real_distribution(generator);

        // Gets the appropiate key based on the random number
        std::vector<std::pair<std::string, float>>::reverse_iterator keys_riterator = keys.rbegin();
        for (; random > keys_riterator->second; ++keys_riterator)
            random -= keys_riterator->second;

        // initializes text based on random context
        text += keys_riterator->first;
    
        if (max_size != 0)
            text = text.substr(0, max_size);
    }

    if (max_size == 0 || text.size() < max_size)
    {
        do
        {   
            // Tries to get list of events based on current context
            std::size_t n = text.size() < k ? text.size() : k;
            Frequency::const_iterator iterator = frequency.find(text.substr(text.size() - n, n));

            // If current context isn't mapped
            // add random character
            if (iterator == frequency.end())
            {
                std::size_t rk = n;
                std::vector<Context> contexts;

                // creates a vector o contexts by
                // matching the first n characters of a context
                // with the last n characters of the current text
                do
                {
                    --rk;
                    std::string lookup = text.substr(text.size() - rk, rk);
                    for (Frequency::const_iterator it = frequency.begin(); it != frequency.end(); ++it)
                        if (it->first.substr(0, rk) == lookup)
                            contexts.emplace_back(it->first, it->second);
                }
                while (rk > 1 && contexts.size() == 0);

                if (contexts.size() == 0)
                    return text;

                // Generates vector of contexts and respective totals
                std::vector<std::pair<Context, unsigned>> contexts_totals(contexts.size());
                std::transform(contexts.begin(), contexts.end(), contexts_totals.begin(), [](auto &context) { return std::pair(context, get_total(context)); });

                // prepares vector of contexts to choose a random context
                // this is done by ordering the vector in descending order
                std::sort(contexts_totals.begin(), contexts_totals.end(), [](auto &context0, auto &context1) { return context0.second > context1.second; });

                // Gets random number
                random = real_distribution(generator);

                float probability;

                unsigned total = 0;
                for (auto &context_total : contexts_totals)
                    total += context_total.second;

                // Used to calculate probabilities
                float f_total = float(total);

                // Get the appropriate context based on the random number
                std::vector<std::pair<Context, unsigned>>::reverse_iterator contexts_totals_riterator = contexts_totals.rbegin();
                for (; random > (probability = float(contexts_totals_riterator->second) / f_total); ++contexts_totals_riterator)
                    random -= probability;

                const std::string &value = contexts_totals_riterator->first.first;
                text += value.substr(value.size() - rk, rk); // PROBLEM!!!!!!!!!!!!!!!!
            }
            else
            {
                // Get context
                const Context context(iterator->first, iterator->second);

                float context_total = float(get_total(context));
                if (context_total == 0)
                    return text;

                float prob_denominator = float(context_total + alpha * alphabet.size());

                // Creates vector with all events for given context
                std::vector<std::pair<char, float>> events(iterator->second.size());
                std::transform(iterator->second.begin(), iterator->second.end(), events.begin(),
                    [&prob_denominator, this](const Event &event) { return std::pair(event.get_character(), float(event.get_count() + alpha) / prob_denominator); });

                // prepares vector of events to choose a random event
                // this is done by ordering the vector in descending order
                std::sort(events.begin(), events.end(), [](auto &event0, auto &event1) { return event0.second > event1.second; });
                
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
        while (max_size == 0 || text.size() < max_size);

    }
    
    // ensures any additional character is removed
    text = text.substr(0, max_size);

    return text;
}

// calculates probabily of "event" knowing "context"
float MarkovModel::get_probability (const MarkovModel::Context &context, const MarkovModel::Event &event) const
{
    return float(event.get_count() + alpha) / float(get_total(context) + alpha * alphabet.size());
}

// calculates entropy
float MarkovModel::get_entropy () const
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
            if (event_prob != 0)
                prob += event_prob * std::log(event_prob); // P(e|c) * log(P(e|c))
        }
        entropy += prob * float(context_total) / float(total); // ^ * P(c)
    }
    return -entropy;
}

float MarkovModel::compare (const MarkovModel &model0, const MarkovModel &model1)
{
    // Build alphabet union
    std::unordered_set<char> alphabet;
    for (auto &character : model0.alphabet)
        alphabet.emplace(character.first);
    for (auto &character : model1.alphabet)
        alphabet.emplace(character.first);

    // Build contexts union
    std::unordered_set<std::string> contexts;
    for (auto &context : model0.frequency)
        contexts.emplace(context.first);
    for (auto &context : model1.frequency)
        contexts.emplace(context.first);

    float total = 0;
    for (auto &context : contexts)
    {
        Frequency::const_iterator iterator0 = model0.frequency.find(context);
        Frequency::const_iterator iterator1 = model1.frequency.find(context);
        // model 0 or model1 don't contain the current context
        if (iterator0 == model0.frequency.end() || iterator1 == model1.frequency.end())
            ++total;
        // both models contain the current context
        else
        {
            const Context context0(iterator0->first, iterator0->second);
            const Context context1(iterator1->first, iterator1->second);
            float total0 = float(get_total(context0));
            float total1 = float(get_total(context1));
            for (auto &character : alphabet)
            {
                Events::const_iterator event0 = std::find_if(context0.second.begin(), context0.second.end(), [&character](auto &event) { return character == event.get_character(); });
                Events::const_iterator event1 = std::find_if(context1.second.begin(), context1.second.end(), [&character](auto &event) { return character == event.get_character(); });
                float prob_event0 = float(event0 == context0.second.end() ? 0 : event0->get_count()) / total0;
                float prob_event1 = float(event1 == context1.second.end() ? 0 : event1->get_count()) / total1;
                float diff_prob = prob_event0 - prob_event1;
                total += diff_prob * diff_prob;
            }
        }
    }

    return total / contexts.size();
}