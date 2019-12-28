import string
import re
import itertools
import math
import progressbar
import time
import argparse
import sys
from prettytable import PrettyTable
from counters import *

translator = str.maketrans(
    string.punctuation + '\n\r\t«»', ' ' * (len(string.punctuation) + 5))


def analyze(expected_events, expected_counter, counters):
    abs_errors = [abs(c.count - expected_counter) for c in counters]
    rel_errors = [error / expected_counter for error in abs_errors]
    values = [c.count for c in counters]

    mean_counter = mean(values)
    diffs = [abs(value - mean_counter) for value in values]
    maxdev = max(diffs)
    mad = mean(diffs)
    stddev = math.sqrt(mean([value * value for value in values]))

    return [
        max(rel_errors),
        min(rel_errors),
        mean(rel_errors),
        mean(abs_errors),
        expected_counter,
        max(values),
        min(values),
        mean_counter,
        mad,
        maxdev,
        stddev,
        stddev * stddev,
        expected_events,
        mean([counter.get() for counter in counters])
    ]


def analyze_logarithmic(counter, counters, a=2):
    return analyze(counter.get(), math.floor(math.log(counter.count + 1, a)), counters)


def analyze_probabilistic(counter, counters, a=2):
    return analyze(counter.get(), counter.count / a, counters)


def count(book, counter, *args, **kwargs):
    counter_dict = dict()
    for word in book:
        counter_inst = counter_dict.setdefault(word, counter(*args, **kwargs))
        counter_inst.increment()
    return counter_dict


def load_book(path, stopwords, encoding='ascii'):
    with open(path, 'r', encoding=encoding) as fin:
        return [word for word in re.split(r' +', fin.read().translate(translator).strip().lower()) if len(word) > 2 and word not in stopwords]
    return []


def load_stopwords(path):
    with open(path, 'r', encoding='utf-8') as fin:
        return [line.strip() for line in fin.readlines() if len(line.strip()) != 0]
    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-to-file',
                        help='File to store results', type=str)

    args = parser.parse_args()

    languages = ['french', 'german', 'english', 'italian']
    encodings = ['utf-8', 'iso-8859-1', 'iso-8859-1', 'iso-8859-1']
    stopwords = {language: load_stopwords(
        'stopwords\\{}.txt'.format(language)) for language in languages}
    books = {language: load_book('books\\stripped_{}.txt'.format(
        language), stopwords[language], encoding=encoding) for language, encoding in zip(languages, encodings)}

    n = 10
    log_a = 2
    prob_a = 64
    trials = [ 10 ]#, 100, 1000, 10000 ]

    metrics = [
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
        'Variance',
        'Expected Number Of Events',
        'Counted Number Of Events'
    ]

    abbr = [
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
        'Variance',
        'ExpEvents',
        'Events'
    ]

    metrics_pt = PrettyTable(['Metric', 'Used Abbreviation'])
    for value in zip(metrics, abbr):
        metrics_pt.add_row(list(value))

    template_pt = PrettyTable(['Word'] + abbr)
    template_pt.float_format = '.2'

    logarithmic_pts = dict()
    probabilistic_pts = dict()

    template_comparsion_pt = PrettyTable()
    template_comparsion_pt.add_column(
        'Order', ['{}º'.format(i) for i in range(1, n + 1)])

    comparsion_pts = dict()
    logarithmic_counters = list()
    probabilistic_counters = list()

    intervals_ec = dict()
    intervals_lc = dict()
    intervals_pc = dict()

    mmm_ec = dict()
    mmm_lc = dict()
    mmm_pc = dict()

    log_results = dict()
    prob_results = dict()

    default_counter = Counter()
    default_logarithmic_counter = LogarithmicCounter()
    default_probabilistic_counter = ProbabilisticCounter()
    headers = {language: 'Processing {} '.format(
        language) for language in languages}
    max_length = max([len(header) for header in headers.values()])
    headers = {language: header + ' ' *
               (max_length - len(header)) for language, header in headers.items()}

    for amount in trials:
        print()
        print('For {} trials:'.format(amount))
        comparsion_pt = comparsion_pts.setdefault(
            amount, template_comparsion_pt.copy())

        length = 0
        for language, book in books.items():
            iec = ilc = ipc = 0
            logarithmic_counters.clear()
            probabilistic_counters.clear()
            exact_counters = count(book, Counter)
            with progressbar.ProgressBar(maxval=amount, term_width=60 + max_length, widgets=[headers[language],  progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(format='%(percentage)6.2f%%')]) as bar:
                for i in range(amount):
                    interval_ec, _ = timeit(count, book, Counter)
                    interval_lc, lc = timeit(
                        count, book, LogarithmicCounter, a=log_a)
                    interval_pc, pc = timeit(
                        count, book, ProbabilisticCounter, a=prob_a)

                    logarithmic_counters.append(lc)
                    probabilistic_counters.append(pc)
                    bar.update(i + 1)

                    iec += interval_ec
                    ilc += interval_lc
                    ipc += interval_pc

            intervals_ec.setdefault(amount, dict())[language] = iec / amount
            intervals_lc.setdefault(amount, dict())[language] = ilc / amount
            intervals_pc.setdefault(amount, dict())[language] = ipc / amount

            logarithmic_pt = logarithmic_pts.setdefault(
                amount, dict()).setdefault(language, template_pt.copy())
            probabilistic_pt = probabilistic_pts.setdefault(
                amount, dict()).setdefault(language, template_pt.copy())

            column = []
            ex_max_value = log_max_mean_value = prob_max_mean_value = 0
            for word, counter in itertools.islice(sorted(exact_counters.items(), key=lambda pair: -pair[1].get()), n):
                log_counters = [logarithmic_counter.get(
                    word) for logarithmic_counter in logarithmic_counters]
                prob_counters = [probabilistic_counter.get(
                    word) for probabilistic_counter in probabilistic_counters]

                log_analysis = analyze_logarithmic(
                    counter, log_counters, a=log_a)
                prob_analysis = analyze_probabilistic(
                    counter, prob_counters, a=prob_a)

                for i in range(3):
                    log_analysis[i] = '{:.2}%'.format(log_analysis[i] * 100)
                    prob_analysis[i] = '{:.2}%'.format(prob_analysis[i] * 100)

                ex_max_value = max(ex_max_value, counter.count)
                log_max_mean_value = max(log_max_mean_value, log_analysis[-7])
                prob_max_mean_value = max(
                    prob_max_mean_value, prob_analysis[-7])

                logarithmic_pt.add_row([word] + log_analysis)
                probabilistic_pt.add_row([word] + prob_analysis)
                column.append('{} [{:.2f}, {:.2f}, {:.2f}]'.format(
                    word, counter.get(), log_analysis[-1], prob_analysis[-1]))
            comparsion_pt.add_column(language, column)

            for word, counter in exact_counters.items():
                log_counters = [logarithmic_counter.get(
                    word) for logarithmic_counter in logarithmic_counters]
                prob_counters = [probabilistic_counter.get(
                    word) for probabilistic_counter in probabilistic_counters]

                log_analysis = analyze_logarithmic(
                    counter, log_counters, a=log_a)
                prob_analysis = analyze_probabilistic(
                    counter, prob_counters, a=prob_a)

                log_results[amount] = [
                    v0 + v1 for v0, v1 in zip(log_results.get(amount, [0] * len(log_analysis)), log_analysis)]
                prob_results[amount] = [
                    v0 + v1 for v0, v1 in zip(prob_results.get(amount, [0] * len(prob_analysis)), prob_analysis)]

            length += len(exact_counters)

            mmm_ec.setdefault(amount, dict())[language] = 'Used: {:.4f} bits, Real: {} bits'.format(
                math.log2(ex_max_value), int(math.ceil(math.log2(ex_max_value))))
            mmm_lc.setdefault(amount, dict())[language] = 'Used: {:.4f} bits, Real: {} bits'.format(
                math.log2(log_max_mean_value), int(math.ceil(math.log2(log_max_mean_value))))
            mmm_pc.setdefault(amount, dict())[language] = 'Used: {:.4f} bits, Real: {} bits'.format(
                math.log2(prob_max_mean_value), int(math.ceil(math.log2(prob_max_mean_value))))

        log_results[amount] = [
            value / length for value in log_results.get(amount, [])]
        prob_results[amount] = [
            value / length for value in prob_results.get(amount, [])]

    performance_pt = PrettyTable(['Language', 'Exact Counter', 'Logarithmic Counter (base = {})'.format(
        log_a), 'Probabilistic Counter (probability = 1/{})'.format(prob_a)])
    performance_pt.float_format = '.4'

    template_overall_pt = PrettyTable(['Trials'] + abbr)
    template_overall_pt.float_format = '.4'

    log_overall_pt = template_overall_pt.copy()
    prob_overall_pt = template_overall_pt.copy()

    print()
    write(sys.stdout, metrics_pt, trials, log_overall_pt, prob_overall_pt, log_results, prob_results, languages, log_a, prob_a,
          logarithmic_pts, probabilistic_pts, comparsion_pts, performance_pt, intervals_ec, intervals_lc, intervals_pc, mmm_ec, mmm_lc, mmm_pc)

    if args.write_to_file:
        with open(args.write_to_file, 'w') as fout:
            write(fout, metrics_pt, trials, log_overall_pt, prob_overall_pt, log_results, prob_results, languages, log_a, prob_a,
                  logarithmic_pts, probabilistic_pts, comparsion_pts, performance_pt, intervals_ec, intervals_lc, intervals_pc, mmm_ec, mmm_lc, mmm_pc)

def mean(x):
    return sum(x) / len(x)


def timeit(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    return end - start, result


def write(output, metrics_pt, trials, log_overall_pt, prob_overall_pt, log_results, prob_results, languages, log_a, prob_a, logarithmic_pts, probabilistic_pts, comparsion_pts, performance_pt, intervals_ec, intervals_lc, intervals_pc, mmm_ec, mmm_lc, mmm_pc):
    output.write('Info. Table\n')
    output.write('{}\n'.format(metrics_pt))

    log_overall_pt.clear_rows()
    prob_overall_pt.clear_rows()

    for amount in trials:
        log_overall_pt.add_row([amount] + log_results.get(amount, []))
        prob_overall_pt.add_row([amount] + prob_results.get(amount, []))

        output.write('\n')
        output.write('For {} trials:'.format(amount))
        for language in languages:
            output.write('\n')
            output.write('Logarithmic Counter (base = {}) [{} trials|{}]:\n'.format(
                log_a, amount, language))
            output.write('{}\n'.format(logarithmic_pts[amount][language]))

            output.write('\n')
            output.write(
                'Probabilistic Counter (probability = 1/{}) [{} trials|{}]:\n'.format(prob_a, amount, language))
            output.write('{}\n'.format(probabilistic_pts[amount][language]))

        output.write('\n')
        output.write('Language Comparsion [{} trials]:\n'.format(amount))
        output.write('{}\n'.format(comparsion_pts[amount]))

        performance_pt.clear_rows()
        for language in languages:
            performance_pt.add_row([language, intervals_ec[amount][language],
                                    intervals_lc[amount][language], intervals_pc[amount][language]])

        output.write('\n')
        output.write('Avg. Times [{} trials]:\n'.format(amount))
        output.write('{}\n'.format(performance_pt))

        performance_pt.clear_rows()
        for language in languages:
            performance_pt.add_row(
                [language, mmm_ec[amount][language], mmm_lc[amount][language], mmm_pc[amount][language]])

        output.write('\n')
        output.write('Avg. Max Memory Usage [{} trials]:\n'.format(amount))
        output.write('{}\n'.format(performance_pt))

    output.write('\n')
    output.write('Overall Logarithmic Counter (base = {}):\n'.format(log_a))
    output.write('{}\n'.format(log_overall_pt))

    output.write('\n')
    output.write('Overall Probabilistic Counter (probability = 1/{}):\n'.format(prob_a))
    output.write('{}\n'.format(prob_overall_pt))


if __name__ == '__main__':
    main()
