from FileReader import FileReader
from datetime import datetime
from model import *
import sys, os

def main(argv : list):
    # read taxi records
    folder = os.path.join('Pequim2019', 'TextFiles')
    taxireader = FileReader(os.path.join(folder, 'my_taxisgps.txt'))
    # roadreader = FileReader(os.path.join(folder, 'my_road_segments.txt'))

    taxireader.taxifilereader()
    # roadreader.roadfilereader()

    # create model
    model = Model(taxireader.list_taxis)

    # group by taxi
    by_taxi = model.group('taxi', 'date')

    # group by date
    by_date = model.group('date', 'taxi')

    # average that amount over some taxi (or all taxis)
    # print(model.average()) # average of all taxis
    # print(by_taxi.average(1)) # average of taxi 1

    print(by_taxi.average(1))
    print(by_date.average())
    print(by_date.average())

    '''total = 0
    for taxi, events in by_taxi.events.items():
        es = events.get(datetime.strptime('2008-02-08', '%Y-%m-%d').date())
        if es:
            total += len(set([ event.segment for event in es ]))

    print(total / len(by_taxi.events))
    print(by_date.average(datetime.strptime('2008-02-08', '%Y-%m-%d').date()))'''

if __name__ == '__main__':
    main(sys.argv[1:])