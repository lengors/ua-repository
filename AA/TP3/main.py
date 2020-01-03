# from bloom_filter2 import BloomFilter2
from bloom_filter import BloomFilter
import re, string
import os

translator = str.maketrans(
    string.punctuation + '\n\r\t«»', ' ' * (len(string.punctuation) + 5))

def read_file(filename):
    l = list()
    with open(filename, encoding = 'UTF-8') as file:
        for line in file:               # podemos usar o tokenizer de RI maybe
            if line != '':
                lista = re.split('; |, |\*|\n|\s|\.',line.strip())  
                l.extend(lista)

    return l

def load_book(path, encoding = 'ascii'):
    with open(path, 'r', encoding=encoding) as fin:
        return [ word for word in re.split(r' +', fin.read().translate(translator).strip().lower()) ]
    return []

if __name__ == "__main__":
    rel_sizes = [2, 3, 5, 7, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50]
    for book in os.listdir("books"):
        words = load_book(os.path.join("books", book), 'utf-8')
        diff_words = list(set(words))
        print("Livro : {}".format(book))
        print("Número de palavras distintas : {}".format(len(diff_words)))
        for size in rel_sizes:
            bf = BloomFilter(m = size * len(diff_words))
            bf.extend(diff_words)
            print("rel {}x - {}".format(size, len(bf)))
        print()