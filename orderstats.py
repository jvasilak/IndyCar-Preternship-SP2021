#!/usr/bin/env python3

import sys
import json

race = {}
newList = []
overtakePassingTime = []
racePassingID = []
currentTime = 0

with open('2019RoadAmerica.json') as json_file:
            race = json.load(json_file)

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
        elif overtakePassingTime[i] <= newEntry['PassingTime']:
            newList.append(race['Overtakes'][i])
        elif overtakePassingTime[i] > newEntry['PassingTime']:
            break

    pastEntry['PassingTime'] = newEntry['PassingTime']

for line in newList:
    print(line)
