#!/usr/bin/env python3

import sys
import json

race = []
newList = []
currentTime = 0
for line in sys.stdin:
    line = json.loads(line)
    race.append(line)

for i in range(0,len(race)):
    if 'ElapsedTime' in race[i]:
        if race[i]['ElapsedTime'] == time:
            newList.append(race[i])
            del race[i]
                
    elif 'OvertakeNo' in race[i]:
        for entry2 in race:
            try:
                if race[i]['PassingTime'] == entry2['PassingTime'] and entry2['ElapsedTime'] == time:
                    newList.append(race[i])
                    del race[i]
                    break
            except:
                continue
                        
    elif 'ForPosition' in race[i]:
        for entry2 in race:
            try:
                if entry['PassingID'] == entry2['PassingID'] and entry2['ElapsedTime'] == time:
                    newList.append(entry)
                    del race[i]
                    break
            except:
                continue
                        

for line in newList:
    print(line)
