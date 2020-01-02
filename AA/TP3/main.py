import re
from bloom_filter import BloomFilter
import os

def read_file(filename):
    l = list()
    with open(filename, encoding = 'UTF-8') as file:
        for line in file:               # podemos usar o tokenizer de RI maybe
            if line != '':
                lista = re.split('; |, |\*|\n|\s|\.',line.strip())  
                l.extend(lista)

    return l


if __name__ == "__main__":


    rel_sizes = [2, 3, 5, 7, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50]
    for book in os.listdir("books"):
        words = read_file(os.path.join("books", book))
        diff_words = list(set(words))
        print("Livro : {}".format(book))
        print("Número de palavras distintas : {}".format(len(diff_words)))
        

        for size in rel_sizes:
            bf = BloomFilter(rel = size)
            bf.extend(words)
            print("rel {}x - {}".format(size, len(bf)))
        print("")
    

    
