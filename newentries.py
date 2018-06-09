#/usr/bin/env python3                                                                                                                                                                                 
"""
Creates a list of entries to be copied to the CSV

TODO: 
    - cleaner datetime code
    - accept a series as parameter (1,2,2,1,2,2,2)
"""

import sys
import datetime
import time


def generate_sequence(amount, days):
    sequence = [1]
    current_amount = sum(i for i in sequence) / len(sequence)

    for day in range(days - 1):
        if current_amount < amount:
            sequence.append(2)
        else:
            sequence.append(1)
        current_amount = sum(i for i in sequence) / len(sequence)
    return sequence


def csv_print(values, start_date):
    if start_date == "today":
        real_date = datetime.date.today()
    elif start_date == "tomorrow":
        delta = 1
        real_date = datetime.date.today() + datetime.timedelta(days=delta)
    else:
        real_date = datetime.datetime.strptime(start_date, "%Y%m%d")
    days_in = 0
    for value in values:
        #real_date = datetime.date.today().strftime("%Y-%m-%d %H:%M:%S")
        current_date = real_date + datetime.timedelta(days=days_in)

        testtime = str(datetime.datetime.fromtimestamp(int(time.mktime(current_date.timetuple()))).strftime("%Y-%m-%d"))
        printable_time = testtime + "T19:00:00Z," + testtime + "T20:00:00Z" 
        sintrom_text = "Sintrom Amount: " + str(value)

        print(sintrom_text + "," + sintrom_text + "," + printable_time)
        days_in += 1


def show_error():
    print("Syntax:")
    print("  python3 newentries.py <start_date> <average_amount_you_need> <number_of_days_to_generate>")
    print("")
    print("  E.g.: python3 newentries.py today 1.7142857142857142 28")
    print("  E.g.: python3 newentries.py tomorrow 1.75 56")
    print("  E.g.: python3 newentries.py 20180614 1.75 56")


if __name__ == '__main__':
    try:
        start_date = sys.argv[1]
        average_value = float(sys.argv[2])
        days = int(sys.argv[3])
    except IndexError:
        show_error()
        sys.exit(2)

    csv_print(generate_sequence(average_value, days), start_date)

