#/usr/bin/env python3
"""
Object for each calendar entry
Load csv
"""

# TODO:
# Create x new objects following serie (also, x mgs per week)

import csv
from collections import abc
from collections import deque
from datetime import datetime
from sequencer import generate_sequence
import rnn

class Dates:
    list = []
    bufferlist = []
    ix_sintrom_date = []

    def __init__(self, csv_file):
        csv_opener = open(csv_file)
        entries_dict = csv.DictReader(csv_opener)
        for row in entries_dict:
            new_entry = DateEntry(row)
            # adding to index before appending makes it store the right position for the index
            ix_entry = {}
            ix_entry['Position'] = len(self.list)
            ix_entry['Timestamp'] = new_entry.start_datetime
            self.ix_sintrom_date.append(ix_entry)
            self.list.append(new_entry)
        # Sort the index after loading
        self.ix_sintrom_date.sort(key=lambda x:x['Timestamp'])

    def select(self, start, number, reference):
        selection = []
        if reference in ['end', 'bottom']:
            first = len(self.ix_sintrom_date) - start
            last = len(self.ix_sintrom_date) - start + number
        else:
            first = start
            last = number
        ix_selection = self.ix_sintrom_date[first:last]
        for ix_entry in ix_selection:
            selection.append(self.list[ix_entry['Position']])

        return selection

    def add(self, sequence, start_datetime_sequence):
        ix = 0
        for sintrom_amount in sequence:
            row = {}
            row['description'] = 'Sintrom Amount: ' + str(sintrom_amount)
            row['summary'] = 'Sintrom Amount: ' + str(sintrom_amount)
            try:
                row['start_datetime'] = start_datetime_sequence[ix]
            except IndexError:
                #TODO: calculate subsequent datetimes, also for end
                row['start_datetime'] = "none"
            new_entry = DateEntry(row)
            self.bufferlist.append(new_entry)
            ix += 1
        for entry in self.bufferlist:
            print(entry.summary)
            print(entry.start_datetime)

class DateEntry:
    """ Taken from FrozenJSON on 'Fluent Python' """

    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return DateEntry.build(self.__data[name])
        
    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence): 
            return [cls.build(item) for item in obj] 
        else:
            return obj

def get_datasamples():
    dates_back = 10
    last_pills = deque()
    last_measure = 0
    last_measure_day = latest_datetime = datetime.strptime('0001-01-01T00:00:01Z', '%Y-%m-%dT%H:%M:%SZ')

    for blank_ix in range(dates_back):
        last_pills.appendleft(0)

    test_list = []
    for ix in range(len(dates.list)):
        stripped_datetime = datetime.strptime(dates.list[ix].start_datetime, '%Y-%m-%dT%H:%M:%SZ')
        if stripped_datetime > latest_datetime:
            if stripped_datetime <= datetime.now():
                if "Blood Level" in dates.list[ix].summary:
                    last_measure_day = stripped_datetime
                    days_since_last_measure_day = 0
                    last_measure = float(str(dates.list[ix].summary).split()[2])
                elif "Sintrom Amount" in dates.list[ix].summary:
                    last_pills.appendleft(int(str(dates.list[ix].summary).split()[2]))
                    if len(last_pills) > dates_back:
                        last_pills.pop()
                    days_since_last_measure_day = stripped_datetime - last_measure_day
                latest_datetime = stripped_datetime
                #print(str(last_pills) + " - " + str(last_measure) + " - " + str(days_since_last_measure_day))
                test_case = []
                for last_pills_ix in range(len(last_pills)):
                    test_case.append(last_pills[last_pills_ix])
                test_case.append(last_measure)
                test_case.append(days_since_last_measure_day)
                test_list.append(test_case)
        else:
            print("ERROR! your dataset is not ordered chronologically")
            print("  Please, sort your CSV file by start_datetime before using this script")
            break
    return test_list




if __name__ == '__main__':
    dates = Dates('../Calendar.csv')
    #four = dates.select(7, 4, 'end')
#    generate_sequence(1.7142857142857142, 56)
##     last_four_days = dates.select(4, 4, 'end')
##     four_days_ago = dates.select(4, 1, 'end')
##     prev_sequence = []
##     prev_start_datetimes = []
##     for day in last_four_days:
##         sintrom = int(str(day.summary).split()[2])
##         prev_sequence.append(sintrom)
##         prev_start_datetimes.append(day.start_datetime)

##    dates.add(generate_sequence(1.7142857142857142, 7, prev_sequence), prev_start_datetimes)

    rnn.model(get_datasamples())

