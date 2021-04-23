#!/usr/bin/env python3
#
# IndyCar Preternship Project
# University of Notre Dame - CSE 20312
# Creators: Emma Fredin, Aidan Gordon, Jonathon Vasilak, and Mark Schermerhorn
#
# This program gathers race results in real-time and compiles statistics in a convenient way, particularly concerning the use of Push to Pass and passes occurring on-track

import json
import sys

'''
    readEntries
    This function is a Python generator that takes in the live data.  For creation purposes, we set stream to sys.stdin and read the data from there.
    PARAMETERS:
        stream = sys.stdin or other place that data should be read from in a JSONL format
        line = inidividual line taken from input

    The data must be in the following JSONL format to work properly:
        {"PassingID": 187739, "PassingTime": 424841964, "TranNr": 5596122, "TimelineID": 4, "Pit": false, "Flag": 8, "ElapsedTime": 0, "LapCount": 0, "LeaderLap": 0}

'''
def readEntries(stream):

    for line in stream:
        yield line

def checkOvertake(race, PassingID, driverOvertakes):
    for entry in race["Passings"]:
        if PassingID == entry["PassingID"]:
            if entry["ElapsedTime"] < driverOvertakes[entry["TranNr"]]:
                # Update Pass Made with Push 2 Pass Dictionary
                # Update Pass made with certain timeline
                print(f"Pass Made With P2P at Timeline " + str(entry["TimelineID"]))
            else:
                # Update Pass Made without Push 2 Pass Dictionary
                # Update Pass made with certain timeline
                print(f"Pass Made WITHOUT P2P at Timeline " + str(entry["TimelineID"]));

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
        # This If Statement takes in any newEntry that contains data from cars passing timelines.
        if 'ElapsedTime' in newEntry:

            # Conditional Statement to Avoid Appending Unnecessary Data to Dictionary
            if newEntry['ElapsedTime'] >= 0 and newEntry['Flag'] == 1 and not newEntry['Pit']:
                race['Passings'].append(newEntry)

        # This Elif Statement appends any data associated with Overtakes.
        elif 'OvertakeNo' in newEntry:
            race['Overtakes'].append(newEntry)

            # This For Loop checks to find the corresponding Timeline Pass for a car when they use Push to Pass and logs that time with an added 30 seconds into a dictionary.
            for Passing in race['Passings']:
                if newEntry['PassingTime'] == Passing['PassingTime']:
                    driverOvertakes[newEntry['TranNr']] = Passing['ElapsedTime'] + 300000 - (newEntry['SecondsBeforeTimeline'] * 10000)
                    break

        # This Elif Statement appends any data associated with Passes
        elif 'CarPassed' in newEntry:
            race['RacePasses'].append(newEntry)
            checkOvertake(race, newEntry["PassingID"], driverOvertakes);

    #print(driverOvertakes)

if __name__ == "__main__":
    main()

