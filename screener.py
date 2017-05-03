#!/usr/local/bin/python3

import os
import quandl

def readRuss():
    try:
        ticks = [] 
        russ = open('russ3.csv', 'r').read()
        split = russ.split('\n')

        for tick in split:
            ticks.append('WIKI/' + tick.rstrip())
        return ticks
    except Exception as e:
        print('Failed to read Russell 3000:', str(e))

def getData(ticks):
    try: 
        return quandl.get(ticks, start_date='2017-05-01')
    except Exception as e:
        print('Failed to get stock data:', str(e))

def printClose(ticks, data):
    for tick in ticks:
        try:
            print(data[tick+' - '+'Close'])
        except KeyError:
            pass 

def main():
    quandl.ApiConfig.api_key = os.environ['QUANDL_KEY']

    ticks = readRuss()
    data = getData(ticks[:20])
    printClose(ticks[:20], data)

if __name__ == "__main__":
    # execute only if run as a script
    main()
