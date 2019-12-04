import os
from math import ceil


def save(segment, num, directory_output):
    global segments_info
    if not os.path.exists(directory_output):
        os.mkdir(directory_output)

    with open(os.path.join(directory_output , "segment" + str(num)), "w") as file:
        for line in segment:
            file.write(line)

    if ':' in segment[0].split(";")[0]:
        segments_info["segment" + str(num)] = (segment[0].split(";")[0].split(":")[0], segment[-1].split(";")[0].split(":")[0])
    else:
        segments_info["segment" + str(num)] = (segment[0].split(";")[0], segment[-1].split(";")[0])

def segment_index(filename, segments_num, directory_output):
    size = ceil(os.stat(filename).st_size / segments_num)
    with open(filename) as file:
        for i in range(segments_num):
            segment = file.readlines(size)
            save(segment, i, directory_output)



number_segments = 10
segments_info = dict()
segment_index("output", number_segments, "index")

