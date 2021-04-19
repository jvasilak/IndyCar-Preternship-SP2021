#!/usr/bin/env python3

import json

with open('2019RoadAmerica.json') as json_file:
    data = json.load(json_file);

for key in data['Timelines']:
    print(key)

