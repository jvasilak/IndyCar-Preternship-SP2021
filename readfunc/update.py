#!/usr/bin/env python3
# Above is the shebang needed to run the program on Notre Dame student machines

import json
import sys


def update_passings(passing_driver, passed_driver, data):
    return 0

'''
    initialize_racePasses
    Parameters:
        data - the dictionary that is being initialized in this function
        driver_list - a data structure containing the transponder numbers of participating drivers
'''
def initialize_racePasses(data, driver_list):

    for Transponder_Number in driver_list:
        if Transponder_Number not in data:
            data[Transponder_Number] = {}
            data[Transponder_Number]["Overtaker"] = {}
            data[Transponder_Number]["Overtaken"] = {}
            data[Transponder_Number]["Overtaker"]["P2P"] = 0
            data[Transponder_Number]["Overtaker"]["~P2P"] = 0
            data[Transponder_Number]["Overtaker"]["OppP2P"] = 0
            data[Transponder_Number]["Overtaker"]["~OppP2P"] = 0
            data[Transponder_Number]["Overtaken"]["P2P"] = 0
            data[Transponder_Number]["Overtaken"]["~P2P"] = 0
            data[Transponder_Number]["Overtaken"]["OppP2P"] = 0
            data[Transponder_Number]["Overtaken"]["~OppP2P"] = 0
    return data

'''
    update_racePasses
    Parameters:
        passing_driver - the transponder number of the driver who has completed the overtake
        passed_driver - the transponder number of the driver who has just been overtaken
        data - the dictionary containing data on pass statistics which is being updated and returned in this function
        passing_P2P - a boolean value that is true if passing_driver has Push to Pass active, default is false
        passed_P2P - a boolean value that is true if passed_driver has Push to Pass active, default is false
    The function update_racePasses returns an updated version of the dictionary "data", which is a parameter passed to this fuction.
    Which values in the dictionary are updated is determined by whether passing_P2P or passed_P2P is true.
    Since all values in the dictionary that may be updated are integers, they are updated by adding one to the value each time.

    This function assumes the dictionary "data" will be in the following format, where the '0's are the numbers being updated:
    data{
    Transponder_Number: {Overtaker{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}, Overtaken{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}},
    Transponder_Number: {Overtaker{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}, Overtaken{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}},
    ...,
    Transponder_Number: {Overtaker{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}, Overtaken{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}}
    }

'''
def update_racePasses(passing_driver, passed_driver, data, passing_P2P=False, passed_P2P=False):

    if(passing_P2P):
        data[passing_driver]["Overtaker"]["P2P"] += 1
        data[passed_driver]["Overtaken"]["OppP2P"] += 1
    else:
        data[passing_driver]["Overtaker"]["~P2P"] += 1
        data[passed_driver]["Overtaken"]["~OppP2P"] += 1

    if(passed_P2P):
        data[passing_driver]["Overtaker"]["OppP2P"] += 1
        data[passed_driver]["Overtaken"]["P2P"] += 1
    else:
        data[passing_driver]["Overtaker"]["~OppP2P"] += 1
        data[passed_driver]["Overtaken"]["~P2P"] += 1

    return data

def update_overtakes(data):
    return 0



def main():
    driver_list = [1, 2, 3]
    data = {}
    data = initialize_racePasses(data, driver_list)
    data = update_racePasses(driver_list[0], driver_list[2], data, True, False)
    print(data)

if __name__ == '__main__':
    main()
