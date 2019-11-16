from FileReader import FileReader
from datetime import datetime
from model import *
from matplotlib import pyplot as plt
import sys, os

weekdays = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ]

def main(argv : list):
    # read taxi records
    folder = os.path.join('Pequim2019', 'TextFiles')
    taxireader = FileReader(os.path.join(folder, 'my_taxisgps.txt'))
    # roadreader = FileReader(os.path.join(folder, 'my_road_segments.txt'))

    taxireader.taxifilereader()
    # roadreader.roadfilereader()

    # create model
    model = Model(taxireader.list_taxis)

    # group by date
    by_date = model.group('date', 'taxi')

    # average that amount over some taxi (or all taxis)
    # print(model.average()) # average of all taxis
    # print(by_taxi.average(1)) # average of taxi 1

    print()
    print('Average number of roads passed by a taxi during a day: {:.2f}'.format(by_date.average()))
    print()

    x = list(sorted(by_date.events[1].keys()))
    y = [ by_date.average(date) for date in x ]
    x = [ '{} ({})'.format(str(date), weekdays[date.weekday]) for date in x ]

    plt.plot(x, y)
    plt.title('Average number of roads passed by a taxi per day')
    plt.xlabel('Date')
    plt.ylabel('Average number of roads')
    plt.show()

if __name__ == '__main__':
    main(sys.argv[1:])