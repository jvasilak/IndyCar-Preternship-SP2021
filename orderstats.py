#!/usr/bin/env python3
#
# IndyCar Preternship Team - CSE 20312
# Preternship Software Engineers: Mark Schermerhorn, Jonathon Vasilak, Emma Fredin, and Aidan Gordon
# May 12, 2021
#
# This program is meant to be used with past test cases to put JSON files into the correct chronological order and format to be read by IndyCarPreternshipFINAL.py
# The test case should be entered as the first command-line argument.

import sys
import json
import re

# Initialize data structures and variables
race = {}
newList = []
overtakePassingTime = []
racePassingID = []
currentTime = 0

# Exit if test case not given
if len(sys.argv) < 2:
    print("No test-case given. Program shut-down")
    exit(1)

if len(sys.argv) > 2:
    print("Too many arguments given. Program shut-down")
    exit(1)

# open JSON file
with open(sys.argv[1]) as json_file:
    race = json.load(json_file)

# Order entries by Elapsed Time
for newEntry in race['Overtakes']:
    overtakePassingTime.append(newEntry['PassingTime'])

for newEntry in race['RacePasses']:
    racePassingID.append(newEntry['PassingID'])
    
pastEntry = {'PassingTime':0}
for newEntry in race['Passings']:
    newList.append(newEntry)
    if newEntry['PassingID'] in racePassingID:
        for i in range(0, len(racePassingID)):
            if newEntry['PassingID'] == racePassingID[i]:
                newList.append(race['RacePasses'][i])
                break
    for i in range(0,len(overtakePassingTime)):
        if overtakePassingTime[i] < pastEntry['PassingTime']:
            continue
        elif overtakePassingTime[i] == newEntry['PassingTime']:
            newList.append(race['Overtakes'][i])
            break
        elif overtakePassingTime[i] > newEntry['PassingTime']:
            break

    pastEntry['PassingTime'] = newEntry['PassingTime']

# Execute string substitutions to convert lines to acceptable Python code for IndyCarPreternshipFINAL.py
for line in newList:
    entry = str(line)
    if "False" in entry:
        entry = re.sub("False", "false", entry)
    elif "True" in entry:
        entry = re.sub("True", "true", entry)

    entry = re.sub(r"\'", r'"', entry)

    print(entry)
