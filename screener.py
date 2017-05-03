import os
import quandl

def readRuss():
    ticks = []  
    
    try:
        russ = open('russ3.csv', 'r').read()
        split = russ.split('\n')
        for tick in split:
            ticks.append('WIKI/' + tick.rstrip())

    except Exception as e:
        print('Failed to read Russell 3000:', str(e))

    return ticks

def getData(ticks):
    try: 
        data = quandl.get(ticks, start_date='2017-05-01')

    except Exception as e:
        print('Failed to get stock data:', str(e))

    return data

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
