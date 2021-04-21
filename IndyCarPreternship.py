#!/usr/bin/env python3

import json
import sys

def readEntries(stream):
    ''' Read in all data points from sys.stdin '''

    for line in sys.stdin:
        yield line

def main():
    stream = sys.stdin
    race = {}

    with open('initial.jsonl') as json_file:
        race = json.load(json_file)

    newEntry = {}
    race['Passings'] = []
    race['Overtakes'] = []
    race['RacePasses'] = []

    for line in readEntries(stream):
        newEntry = json.loads(line)
        if 'ElapsedTime' in newEntry:
            if newEntry['Flag'] == 1 and newEntry['ElapsedTime'] > 0 and not newEntry['Pit']:
                race['Passings'].append(newEntry)
        else if 'OvertakeNo' in newEntry:
            race['Overtakes'].append(newEntry)
        else if 'CarPassed' in newEntry:
            race['RacePasses'].append(newEntry)

    print(race)

if __name__ == "__main__":
    main()

