from count_min_sketch import CountMinSketch

def main():
    real_count = dict()
    count_min_sketch = CountMinSketch(10, 3)

    write = input('Value [ENTER to exit]: ').strip()
    while len(write) != 0:
        count_min_sketch.update(write)
        real_count[write] = real_count.get(write, 0) + 1
        write = input('Value [ENTER to exit]: ').strip()

    print()
    print('Results:')
    for key, value in real_count.items():
        print('{}: [REAL = {}, COUNTED = {}]'.format(key, value, count_min_sketch[key]))

if __name__ == '__main__':
    main()