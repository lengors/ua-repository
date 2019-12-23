import time, os, psutil, multiprocessing

def get_filenames(inputname):
    if os.path.isfile(inputname):
        return [ inputname ]
    elif os.path.isdir(inputname):
        return [ os.path.join(inputname, filename) for filename in os.listdir(inputname) if os.path.isfile(os.path.join(inputname, filename)) ]
    return [ ]

def profileit(function, *args, **kwargs):
    profiler = Profiler()
    profiler.start()
    result = function(*args, **kwargs)
    return result, profiler.stop()

# taken and adapted from: https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
# converts size in bytes to a human readable version of that size
def sizeof_fmt(size, number_fmt = '{:.1f}', suffix = 'B'):
    fmt = number_fmt + '{}{}'
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if size < 1024:
            return fmt.format(size, unit, suffix)
        size /= 1024.0
    return fmt.format(size, 'Yi', suffix)

def timeit(function, *args, **kwargs):
    start = time.time()
    result = function(*args, **kwargs)
    end = time.time()
    return result, end - start

# profiles memory from specified process
class Profiler(multiprocessing.Process):
    def __init__(self, pid = os.getpid()):
        self.exit = multiprocessing.Event()
        self.max_memory = multiprocessing.Value('i', 0)
        super().__init__(target = self.profile, args = (pid, ))

    def profile(self, pid):
        process = psutil.Process(pid)
        while not self.exit.is_set():
            self.max_memory.value = max(self.max_memory.value, process.memory_info().vms)
        self.max_memory.value = max(self.max_memory.value, process.memory_info().vms)

    def stop(self):
        self.exit.set()
        self.join()
        return self.max_memory.value