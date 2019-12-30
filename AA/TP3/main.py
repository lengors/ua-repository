import re
from bloom_filter import BloomFilter

def read_file(filename):
    l = list()
    with open(filename, encoding = 'UTF-8') as file:
        for line in file:               # podemos usar o tokenizer de RI maybe
            lista = re.split('; |, |\*|\n|\s|\.',line.strip())  
            l.extend(lista)

    return l


if __name__ == "__main__":
    words = read_file("Maias.txt")
    bf = BloomFilter()
    bf.extend(words)
    print(str(bf))
    print(bf.contains("Maia"))
