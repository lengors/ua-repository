import engine, utils, os, rules
from itertools import product

'''
    Trabalho realizado por : 
        - Lucas Barros, nmec : 83895;
        - Pedro Cavadas, nmec : 85090;
'''

def main():
    args = engine.parser.parse_args()
    filenames = utils.get_filenames(args.input)
    files_exist = len(filenames) != 0
    stopwords_exist = os.path.isfile(args.stopwords)
    if files_exist and stopwords_exist:
        used_tokenizer = engine.tokenizers[args.tokenizer]
        if used_tokenizer.has_rule(rules.stopping):
            used_tokenizer.make_rule(rules.stopping, args.stopwords)
        values = [ 'store_positions', 'calculate_tfidf' ]
        combinations = [ { key : value for key, value in zip(values, option) } for option in product([ True, False ], repeat = len(values)) ]
        for combination in combinations:
            (indexer, max_memory) , interval = utils.timeit(utils.profileit,
                engine.indexit, used_tokenizer, filenames, memory_usage = args.memory, **combination)
            indexer.save(args.output)
            print('Answers({}):'.format(', '.join([ '{} = {}'.format(key, value) for key, value in combination.items() ])))
            print('Time taken: {}s'.format(interval))
            print('Max memory usage: {}'.format(utils.sizeof_fmt(max_memory)))
            print('Disk size: {}'.format(utils.sizeof_fmt(os.path.getsize(args.output))))
            indexer.dispose()
            del indexer
    else:
        if not files_exist:
            print('Error: File or directory (with files) to index doesn\'t exist!')
        if not stopwords_exist:
            print('Error: Stopwords\' file doesn\'t exist!')

if __name__ == '__main__':
    main()