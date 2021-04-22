#!/usr/bin/env python3
#
# IndyCar Preternship Project
# University of Notre Dame - CSE 20312
# Creators: Emma Fredin, Aidan Gordon, Jonathon Vasilak, and Mark Schermerhorn
#
# This program gathers race results in real-time and compiles statistics in a convenient way, particularly concerning the use of Push to Pass and passes occurring on-track

import json
import sys

def readEntries(stream):
    ''' Read in all data points from sys.stdin '''

    for line in sys.stdin:
        yield line

def main():
    # Initialize Dictionaries and stdin
    stream = sys.stdin
    race = {}
    driverOvertakes = {}

    # Read Initial Competitors and Timeline Dictionaries
    with open('initial.jsonl') as json_file:
        race = json.load(json_file)

    # Initialize Nested Dictionaries
    newEntry = {}
    race['Passings'] = []
    race['Overtakes'] = []
    race['RacePasses'] = []

    # Initialize Additional Overtakes Dictionary To Track 30 Seconds After Last Used Push To Pass For Each Driver
    for driverDict in race['Competitors']:
        driverOvertakes[driverDict['TranNr']] = 0

    # For Loop Receives One Entry Per Loop From The Generator And Parses It From JSON to a Python Dictionary
    for line in readEntries(stream):
        newEntry = json.loads(line)

        # If Statement Places newEntry in Correct Nested Dictionary with Additional Conditions
        if 'ElapsedTime' in newEntry:
            if newEntry['ElapsedTime'] > 0 and newEntry['Flag'] == 1 and not newEntry['Pit']:
                race['Passings'].append(newEntry)
        elif 'OvertakeNo' in newEntry:
            race['Overtakes'].append(newEntry)
            for Passing in race['Passings']:
                if newEntry['PassingTime'] == Passing['PassingTime']:
                    driverOvertakes[newEntry['TranNr']] = Passing['ElapsedTime'] + 300000 - (newEntry['SecondsBeforeTimeline'] * 10000)
                    break
        elif 'CarPassed' in newEntry:
            race['RacePasses'].append(newEntry)

if __name__ == "__main__":
    main()

