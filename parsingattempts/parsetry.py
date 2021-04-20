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

    #print(race)

    newEntry = {}

    for line in readEntries(stream):
        print(line)

if __name__ == "__main__":
    main()

