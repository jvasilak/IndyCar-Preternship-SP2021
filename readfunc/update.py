#!/usr/bin/env python3
# Above is the shebang needed to run the program on Notre Dame student machines

import json
import sys


'''
    initialize_passings
    Parameters:
        driver_list - a data structure containing the transponder numbers of participating drivers
        data - the dictionary that is being initialized in this function
'''
def initialize_passings(driver_list, data):
    
    return data

def update_passings(passing_driver, passed_driver, data):

    return data




'''
    initialize_racePasses
    Parameters:
        data - the dictionary that is being initialized in this function
        driver_list - a data structure containing the transponder numbers of participating drivers
    This function will initialize the data dictionary, putting it in the formatt used by the update_racePasses function.
    Within the dictionary, there are multiple nested dictionaries.
    The keys of the dictionary are:
        Overtaker - contains data regarding instances when this driver is the one doing the overtaking
        Overtaken - contains data regarding instances when this driver is the one being overtaken
        P2P - situations, either where the driver is overtaking another driver or is being overtaken, where Push to Pass is active for this driver
        ~P2P - situations where Push to Pass is not active for this driver
        OppP2P - situations where Push to Pass is active for the other driver involved in the overtake
        ~OppP2P - situations where Push to Pass is not active for the other driver involved in the overtake
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

'''
    initialize_overtakes
    Parameters:
        data - the dictionary that will be initialized and returned from the function
        driver_list - a data structure containing the transponder number of all the drivers
    The keys in the "data" dictionary will be the transponder numbers of the drivers.
'''
def initialize_overtakes(data, driver_list):
    for Transponder_Number in driver_list:
        if Transponder_Number not in data:
            data[Transponder_Number] = {}

    return data

'''
    update_overtakes
    Parameters:
        driver_number - the number of the driver whose information is being updated
        data - he dictionary containing data on overtake statistics which is being updated and returned in this function
        input_data - the data, in the form of a dictionary, that is being added to data
        overtake_num - the number of times the driver has used the overtake button

    The data dictionary will need to be in the following format to work properly:
        overtake_data{
            Transponder_Number: {input_data},
            Transponder_Number: {input_data}
            ...,
            Transponder_Number: {input_data}
        }

'''
def update_overtakes(driver_number, data, input_data, overtake_num):
    if driver_number not in data:
        data[driver_number] = {}
        #TODO: Properly format the input data so it contains all the information needed
    data[driver_number][overtake_num] = input_data
    return data


# This function is only being used to test my other functions
def main():
    driver_list = [1, 2, 3]
    data = {}
    #data = initialize_racePasses(data, driver_list)
    #data = update_racePasses(driver_list[0], driver_list[2], data, True, False)
    #print(data)
    d = {'a', 'b', 'c'}
    e = {'d', 'g', 'e'}
    data = update_overtakes(2123123, data, d, 1)
    data = update_overtakes(2123123, data, e, 2)
    print(data)

if __name__ == '__main__':
    main()
