#!/usr/local/bin/python3

import os
import quandl as ql
import pandas as pd

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

def getData(ticks, start):
    try: 
        return ql.get(ticks, start_date = start)

    except Exception as e:
        print('Failed to get stock data:', str(e))

def main():
    ql.ApiConfig.api_key = os.environ['QUANDL_KEY']

    ticks = readRuss()
    close = [ tick + '.4' for tick in ticks[:50] ] 
    vol   = [ tick + '.5' for tick in ticks[:50] ]

    print(getData(close + vol, '2017-01-01'))

if __name__ == "__main__":
    # execute only if run as a script
    main()
