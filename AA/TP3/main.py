# from bloom_filter2 import BloomFilter2
from concurrent.futures import ProcessPoolExecutor
from bloom_filter import BloomFilter
from prettytable import PrettyTable
from matplotlib import pyplot
import re, string, os, math
import collections

translator = str.maketrans(
    string.punctuation + '\n\r\t«»', ' ' * (len(string.punctuation) + 5))

def analyze(expected_counter, counters):
    abs_errors = [ abs(c - expected_counter) for c in counters ]
    rel_errors = [ error / expected_counter for error in abs_errors ]

    mean_counter = mean(counters)
    diffs = [ abs(value - mean_counter) for value in counters ]
    maxdev = max(diffs)
    mad = mean(diffs)
    stddev = math.sqrt(mean([ value * value for value in counters ]))

    return [
        max(rel_errors),
        min(rel_errors),
        mean(rel_errors),
        mean(abs_errors),
        expected_counter,
        max(counters),
        min(counters),
        mean_counter,
        mad,
        maxdev,
        stddev,
        stddev * stddev,
    ]

def load_book(path, encoding = 'ascii'):
    with open(path, 'r', encoding=encoding) as fin:
        return [ word for word in re.split(r' +', fin.read().translate(translator).strip().lower()) ]
    return []

def mean(x):
    return sum(x) / len(x)

def test(args):
    counts, lengths = list(), list()
    diff_words, k, size, amount = args
    for i in range(amount):
        bf = BloomFilter(m = size * len(diff_words), k = k)
        counts.append(bf.extend(diff_words))
        lengths.append(len(bf))
    return lengths, counts, k

def write_results(file, metrics_pt, table_pt, results):
    if type(file) == str:
        with open(file, 'w', encoding = 'utf-8') as fout:
            write_results(fout, metrics_pt, table_pt, results)
    else:
        file.write('Info. Table\n')
        file.write('{}\n'.format(metrics_pt))

        for book, book_results in results.items():
            for size, size_results in book_results.items():
                inserted_pt = table_pt.copy()
                approxst_pt = table_pt.copy()
                for size, k, theoric, counts_analysis, lengths_analysis in size_results:
                    inserted_pt.add_row([ size, k, theoric ] + counts_analysis)
                    approxst_pt.add_row([ size, k, theoric ] + lengths_analysis)
                file.write('\nAnalysis by inserted (book = "{}")\n'.format(book))
                file.write('{}\n'.format(inserted_pt))

                file.write('\nAnalysis by statistical approximation (book = "{}")\n'.format(book))
                file.write('{}\n'.format(approxst_pt))

if __name__ == '__main__':
    metrics = [
        'Size Bit Array',
        ' Number Of Hashes',
        'Theorical Optimal Number Of Hashes',
        'Max Rel. Error',
        'Min Rel. Error',
        'Mean Rel. Error',
        'Mean Abs. Error',
        'Expected Value',
        'Max Counter Value',
        'Min Counter Value',
        'Mean Counter Value',
        'Mean Abs. Deviation',
        'Maximal Deviation',
        'Standard Deviation',
        'Variance'
    ]

    abbr = [
        'Size',
        'k',
        'Optimal k',
        'MaxRE',
        'MinRE',
        'MeanRE',
        'MeanAE',
        'ExpValue',
        'MaxCV',
        'MinCV',
        'MeanCV',
        'MeanAD',
        'MD',
        'SD',
        'Variance'
    ]

    metrics_pt = PrettyTable(['Metric', 'Used Abbreviation'])
    for value in zip(metrics, abbr):
        metrics_pt.add_row(list(value))

    table_pt = PrettyTable(abbr)
    table_pt.float_format = '.2'

    amount = 1000
    k_hashes = list(range(1, 13))
    rel_sizes = [ 2, 3, 5, 7, 8, 10, 12, 15 ]

    results = dict()
    for bj, book in enumerate(os.listdir('books')[:]):

        words = load_book(os.path.join('books', book), 'utf-8')
        book_results = results.setdefault(book, collections.OrderedDict())
        diff_words = list(set(words))

        print('Livro : {}'.format(book))
        print('Número de palavras distintas : {}'.format(len(diff_words)))

        kvalues = dict()
        for size in rel_sizes:
            size_results = book_results.setdefault(size, list())
            theoric = math.ceil(math.log(2) * size)
            ks = kvalues.setdefault(size, { 'theoric' : theoric, 'ks' : list() })
            with ProcessPoolExecutor(max_workers = len(k_hashes)) as executor:
                for lengths, counts, k in executor.map(test, [ (diff_words, k, size, amount) for k in k_hashes ]):
                    counts_analysis = analyze(len(diff_words), counts)
                    lengths_analysis = analyze(len(diff_words), lengths)
                    size_results.append((size, k, theoric, counts_analysis, lengths_analysis))
                    ks['ks'].append((k, counts_analysis[2], lengths_analysis[2], counts_analysis[7]))

        if bj == 0:
            rows, columns = 2, 4
            fig0, axs0 = pyplot.subplots(rows, columns)
            fig1, axs1 = pyplot.subplots(rows, columns)
            fig2, axs2 = pyplot.subplots(rows, columns)
            for i, size in enumerate(rel_sizes):
                ks = kvalues[size]['ks']
                theoric = kvalues[size]['theoric']
                index = (i // columns, i % columns)
                axs0[index].plot([ x for x, _, _, _ in ks ], [ y for _, y, _, _ in ks ])
                axs1[index].plot([ x for x, _, _, _ in ks ], [ y for _, y, _, _ in ks ])
                axs1[index].plot([ x for x, _, _, _ in ks ], [ y for _, _, y, _ in ks ])
                axs2[index].plot([ x for x, _, _, _ in ks ], [ y for _, _, _, y in ks ])
                axs1[index].legend([ 'Estimation by inserted', 'Estimation by statistical approximation' ])
                best = min(ks, key = lambda x : x[1])
                ks = { x : (y0, y1, y2) for x, y0, y1, y2 in ks }
                axs0[index].scatter([ theoric ], [ ks[theoric][0] ])
                axs1[index].scatter([ theoric ], [ ks[theoric][0] ])
                axs0[index].scatter([ best[0] ], [ best[1] ], c = 'r')
                axs1[index].scatter([ best[0] ], [ best[1] ], c = 'r')
                axs2[index].scatter([ best[0] ], [ best[3] ], c = 'r')
                axs0[index].set_xlabel('Number Of Hash Functions')
                axs1[index].set_xlabel('Number Of Hash Functions')
                axs2[index].set_xlabel('Number Of Hash Functions')
                axs0[index].set_ylabel('Mean Relative Error')
                axs1[index].set_ylabel('Mean Relative Error')
                axs2[index].set_ylabel('Count Estimation')
                axs0[index].set_title('Mean Relative Error Analysis (size = {})'.format(size))
                axs1[index].set_title('Mean Relative Error Analysis (size = {})'.format(size))
                axs2[index].set_title('Count Estimation Analysis (size = {})'.format(size))

            fig0.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)
            fig1.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)
            fig2.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)
            pyplot.show()

    write_results('results.txt', metrics_pt, table_pt, results)