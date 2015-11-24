#!/usr/bin/env python

# coding: utf-8

"""
Usage: (example)

ipython --pylab
run process_report.py
# play with the data, for example

report.plot(x='train', y='station', kind='scatter')
"""

import cPickle as pickle
import os

try:
    import xlrd
    import pandas as pd
    import bidi.algorithm as ba
except Exception as e:
    print("missing one of the dependencies ({})".format(e))
    print("install the environment via virtualenv:")
    print("virtualenv env")
    print(". env/bin/activate # (or for windows activate.bat)")
    print("pip install -r requirements.txt")

print("Welcome to a script to play with Open Train data made available by the Israeli government")

bd = ba.get_display
EXCEL_FILENAME = os.path.join('xl', '2014_08_09.xlsx')

if not os.path.exists(EXCEL_FILENAME):
    print("downloading {}".format(EXCEL_FILENAME))
    os.system("mkdir -p xl")
    os.chdir('xl')
    os.system("wget http://otrain.org/files/xl/2014_08_09.xlsx")
    os.chdir('..')

def get_unprocessed(cached=True, excel_filename=EXCEL_FILENAME):
    pickle_filename = '{}.pickle'.format(excel_filename)
    if not cached or not os.path.exists(pickle_filename):
        print("reading via pandas (long): {}".format(excel_filename))
        xl = pd.ExcelFile(excel_filename)
        report=xl.parse('Report 1', skiprows=[0, 1, 2])
        #print('\n'.join(map(bd, report.columns)))
        report.columns = ['ignore me', 'ride_date', 'train', 'planned', 'station', 'station_description', 'station_serial', 'line_description', 'station_features', 'planned_stop', 'stopped', 'leave_planned', 'leave_actual', 'arrive_planned', 'arrive_actual']
        # Planned column - make bool
        is_planned = list(set(xl.planned))[1]
        xl.planned = xl.planned == is_planned
        # Save preprocessed pandas version
        with open(pickle_filename, 'w+') as fd:
            pickle.dump(report, fd)
    with open(pickle_filename) as fd:
        return pickle.load(fd)

xl = get_unprocessed()

#report.plot(x='train', y='station', kind='scatter')
#report.hist('train')
#report.hist('station')
#report.hist('planned')

