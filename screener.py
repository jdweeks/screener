#!/usr/local/bin/python3

import os, sys, getopt
import quandl as ql
import pandas as pd
import numpy  as np

# read Russell 3000 constituents from a csv
def readRuss():
    try:
        ticks = [] 
        russ  = open('russ3.csv', 'r').read()
        split = russ.split('\n')

        for tick in split:
            ticks.append('WIKI/' + tick.rstrip())
        return ticks

    except Exception as e:
        print('Failed to read Russell 3000:', str(e))

# retrieve stock data from Quandl
def getData(query, date):
    try: 
        return ql.get(query, start_date = date)

    except Exception as e:
        print('Failed to get stock data:', str(e))

# fit a first-degree polynomial (i.e. a line) to the data
def calcTrend(data):
    coeffs = np.polyfit(data.index.values, list(data), 1)
    slope  = coeffs[-2]
    return float(slope)

def main(argv):
    tick = 'WIKI/'      # ticker will be appended
    date = '2017/01/01' # default start date

    ql.ApiConfig.api_key = os.environ['QUANDL_KEY']
    usage = 'usage: screener.py -t <ticker> -d <start_date>'

    if len(argv) == 0:
        print(usage)
        sys.exit(2)

    # parse command-line args
    try:
        opts, args = getopt.getopt(argv, 'ht:d', ['ticker=', 'date='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit(0)        
        elif opt in ('-t', '--ticker'):
            tick += arg
        elif opt in ('-d', '--date'):
            date = arg

    # retrieve the 4th & 5th cols (Close & Volume)
    close  = getData(tick + '.4', date)      
    vol    = getData(tick + '.5', date)
    data   = pd.concat([close, vol], axis=1)
    print(data)

    # calculate trends on price and volume
    print('Price trend:',  calcTrend(data['Close'].reset_index(drop=True)))
    print('Volume trend:', calcTrend(data['Volume'].reset_index(drop=True)))

#   ticks = readRuss()
#   q_close = [ tick + '.4' for tick in ticks[:5] ] 
#   q_vol   = [ tick + '.5' for tick in ticks[:5] ]
#   data = getData(q_close + q_vol, '2017-01-01')

if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
