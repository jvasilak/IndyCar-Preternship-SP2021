#!/usr/bin/env python3

'''
    convertDict
    Parameters:
        convert - a dictionary to convert to a JSON        
    Return value: this function will return the same data as stored in dict in a JSON format    
'''

import json

def convertDict(convert):

	with open("convert.json", "w") as outfile:
		json.dump(convert, outfile)

dictionary = {
				"Competitors" : [
            {"FirstName": "Felix", "LastName": "Rosenqvist", "CarNo": "10", "TranNr": 3463610},
            {"FirstName": "Will", "LastName": "Power", "CarNo": "12", "TranNr": 5596122},
        ],
        "Timelines" : [
            {"TimelineID": 1, "Name": "SF", "Order": 0},
            {"TimelineID": 2, "Name": "SFT", "Order": 1},
        ]
    }

convertDict(dictionary)
