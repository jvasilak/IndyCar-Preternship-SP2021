#!/usr/bin/env python3
#
# IndyCar Preternship Project
# University of Notre Dame - CSE 20312
# Creators: Emma Fredin, Aidan Gordon, Jonathon Vasilak, and Mark Schermerhorn
#
# This program gathers race results in real-time and compiles statistics in a convenient way, particularly concerning the use of Push to Pass and passes occurring on-track

import json
import sys
import operator
import os
import time

'''
    displayScreen
    This function calls the get functions to display all of the information to the terminal.
    PARAMETERS:
        race - complete dictionary containing dictionaries of all events occurring in the race.  It also contains information concerning drivers and timelines.
        combined_data - nested dictionaries containing many of the calculations
        newEntry - current entry that is being recorded
        P2PBool - value from checkOvertakes function to determine use of P2P
        driver_list - list containing all car numbers
    The terminal is cleared before every new event and continually updated
'''

def displayScreen(race, combined_data, newEntry, P2PBool, driver_list):
    os.system('clear')
    print('NTT INDYCAR SERIES')
    print()
    print(f'LATEST EVENTS - LAP {race["Passings"][-1]["LeaderLap"]}')
    race = mostRecentEvent(race, newEntry, P2PBool)
    print()
    print()

    # Most Passes using Push to Pass
    max_P2P = max_position_P2P(combined_data["Passes"], driver_list)
    for key, value in max_P2P.items():
        if value != 0:
            print(f'MOST P2P PASSES: {race["CarNotoName"][str(key)]} - {value}')
        else:
            print(f'MOST P2P PASSES: NONE')
    print()

    # Most Passes not using Push to Pass
    max_notP2P = max_position_nonP2P(combined_data["Passes"], driver_list)
    for key, value in max_notP2P.items():
        if value != 0:
            print(f'MOST NON-P2P Passes: {race["CarNotoName"][str(key)]} - {value}')
        else:
            print(f'MOST NON-P2P PASSES: NONE')

    print()

    # Most Lapped Passes using Push to Pass
    maxLappedP2P = max_lapped_P2P(combined_data["Lapped Passes"], driver_list)
    for key, value in maxLappedP2P.items():
        if value != 0:
            print(f'MOST P2P LAPPED PASSES: {race["CarNotoName"][str(key)]} - {value}')
        else:
            print(f'MOST P2P LAPPED PASSES: NONE')
    print()

    # Most Lapped Passes using Push to Pass
    maxLappednonP2P = max_lapped_nonP2P(combined_data["Lapped Passes"], driver_list)
    for key, value in maxLappednonP2P.items():
        if value != 0:
            print(f'MOST NON-P2P LAPPED PASSES: {race["CarNotoName"][str(key)]} - {value}')
        else:
            print(f'MOST NON-P2P LAPPED PASSES: NONE')
    print()
    print()

    # Percentage of Passes for Position, Total Number of Passes, and Avg Lab use of P2P
    print(f'INDIVIDUAL DRIVER STATISTICS')
    print(f'                           % PASSES FOR POSITION')
    print(f'                   DRIVER:   P2P       NON-P2P        TOTAL PASSES        AVG LAP # USE OF P2P           P2P LEFT           BEST TIMELINE')
    for i in driver_list:
        percent = calc_percentage(combined_data["Passes"][i]["Overtaker"]["P2P"], combined_data["Passes"][i]["Overtaker"]["~P2P"], True)
        percentNonP2P = calc_percentage(combined_data["Passes"][i]["Overtaker"]["P2P"], combined_data["Passes"][i]["Overtaker"]["~P2P"], False)
        average = averageLap(combined_data["Overtake Mode"], i)
        secP2PLeft = P2PLeft(race, i)
        maxTimeValDict = best_timeline_passes_func(race, i)
        for timeline, val in maxTimeValDict.items():    
            if val == 1 and timeline != 0:
                print(f'{race["CarNotoName"][str(i)]:>25}:{round(percent):>5}%{round(percentNonP2P):>11}%{race["TotalPasses"][str(i)]:>17}{round(average):>23}{secP2PLeft:>26}{timeline:>16} - {val} pass')
            elif timeline != 0:
                print(f'{race["CarNotoName"][str(i)]:>25}:{round(percent):>5}%{round(percentNonP2P):>11}%{race["TotalPasses"][str(i)]:>17}{round(average):>23}{secP2PLeft:>26}{timeline:>16} - {val} passes')
            else:
                print(f'{race["CarNotoName"][str(i)]:>25}:{round(percent):>5}%{round(percentNonP2P):>11}%{race["TotalPasses"][str(i)]:>17}{round(average):>23}{secP2PLeft:>26}                  N/A')
    print(f'                                                    TOTAL: {len(race["RacePasses"])}')
    print()

    # Display Number of Passes occurring at each timeline
    print("TIMELINE STATISTICS")
    print("                 TIMELINE :   # PASSES     %       PASSES WITH P2P      PASSES WITHOUT P2P              BEST DRIVER                     DRIVER USING MOST P2P")
    maxTimelinePasses(race, combined_data, driver_list)
    print()
    # time.sleep(0.2)

'''
    mostRecentEvent
    This function compiles the race['RaceEvents'] dictionary that is a dictionary of strings containing all of the Passes and Uses of Overtake in the race. The function also prints the latest 5 events to the terminal
    PARAMETERS:
        race - dictionary containing all data read in from the timelines. It is needed to store the string descriptions.
        newEntry - most recent entry detected from timelines
        P2PBool - boolean value determining if the car is using Push to Pass
        Return Value - This function then returns the race dictionary
'''

def mostRecentEvent(race, newEntry, P2PBool):
    if 'ForPosition' in newEntry:
        if P2PBool:
            if newEntry['Position'] != 0:
                race['RaceEvents'].append(f'{race["CarNotoName"][newEntry["CarNo"]]} (#{newEntry["CarNo"]}) passed {race["CarNotoName"][newEntry["CarPassed"]]} (#{newEntry["CarPassed"]}) WITH P2P for P{newEntry["Position"]} at Timeline {newEntry["TimelineID"]}.')
            else:
                race['RaceEvents'].append(f'{race["CarNotoName"][newEntry["CarNo"]]} (#{newEntry["CarNo"]}) lapped {race["CarNotoName"][newEntry["CarPassed"]]} (#{newEntry["CarPassed"]}) WITH P2P at Timeline {newEntry["TimelineID"]}.')
        else:
            if newEntry['Position'] != 0:
                race['RaceEvents'].append(f'{race["CarNotoName"][newEntry["CarNo"]]} (#{newEntry["CarNo"]}) passed {race["CarNotoName"][newEntry["CarPassed"]]} (#{newEntry["CarPassed"]}) WITHOUT P2P for P{newEntry["Position"]} at Timeline {newEntry["TimelineID"]}.')
            else:
                race['RaceEvents'].append(f'{race["CarNotoName"][newEntry["CarNo"]]} (#{newEntry["CarNo"]}) lapped {race["CarNotoName"][newEntry["CarPassed"]]} (#{newEntry["CarPassed"]}) WITHOUT P2P at Timeline {newEntry["TimelineID"]}.')
    elif 'OvertakeNo' in newEntry:
        carNo = transponder_to_carNo(race['Competitors'], int(newEntry['TranNr']))
        if newEntry["SecondsOfPush"] != 1:
            race['RaceEvents'].append(f'{race["CarNotoName"][str(carNo)]} (#{str(carNo)}) has used {newEntry["SecondsOfPush"]} seconds of P2P at Timeline {newEntry["TimelineID"]}.')
        else:
            race['RaceEvents'].append(f'{race["CarNotoName"][str(carNo)]} (#{str(carNo)}) has used {newEntry["SecondsOfPush"]} second of P2P at Timeline {newEntry["TimelineID"]}.')


    if len(race['RaceEvents']) >= 5:
        for i in range(-1,-6,-1):
            print(race['RaceEvents'][i])
    else:
        print(race['RaceEvents'][-1])

    return race


'''
    best_timeline
    Parameters:
        overtake_data - the dictionary containing information on overtake presses for all drivers
        TimelineID - the number of the checkpoint being checked
    Return Value - this function returns a dictionary containg a driver number and the number of overtakes completed by the driver at the checkpoint number passed to this function
    This function will compare all drivers' statistics regarding overtake presses at a certain timeline to determine which driver has used it the most at a specific timeline
                                                        
'''
def best_timeline(overtake_data, TimelineID):
    return_dictionary = {}
    max_val = 0
    driver_numbers = []
    for driver in overtake_data:
        if TimelineID in overtake_data[driver]["TimelineIDs"]:
            if(max_val <= overtake_data[driver]["TimelineIDs"][TimelineID]):
                max_val = overtake_data[driver]["TimelineIDs"][TimelineID]
                driver_numbers.append(driver)

    for driver in driver_numbers:
        return_dictionary[driver] = max_val
    return return_dictionary


'''
    best_timeline_passes_func
    This function returns a dictionary containing the timeline and passes for the best timeline of a specific driver.
    PARAMETERS:
        race - dictionary containing the passes-by-timeline data for each car
        CarNo - specific car we want to find the best timeline for
'''
def best_timeline_passes_func(race, CarNo):
    maxTimeVal = {}
    tmpTimeline = 0
    tmpMax = 0
    for timeline, value in race['best_timeline_passes'][CarNo].items():
        if value > tmpMax:
            tmpMax = value
            tmpTimeline = timeline

    maxTimeVal[tmpTimeline] = tmpMax
    return maxTimeVal

'''
    most_passes_by_timeline
    This function returns a dictionary containing the car number and the number of passes for the car that has passed the most people at a specific timeline
    PARAMETERS:
        race - dictionary containing the passes-by-timeline data for each car
        TimelineID - specific timeline we are referencing
        driver_info - list containing all of the driver numbers
'''
def most_passes_by_timeline(race, TimelineID, driver_info):
    maxTimeVal = {}
    tmpCarNo = 0
    tmpMax = 0
    for CarNo in driver_info:
        if race['best_timeline_passes'][CarNo][TimelineID] > tmpMax:
            tmpCarNo = CarNo
            tmpMax = race['best_timeline_passes'][CarNo][TimelineID]

    maxTimeVal[tmpCarNo] = tmpMax
    return maxTimeVal


'''
    maxTimelinePasses
    This function is called from displayScreen and prints the timelines and the number of passes completed at each one, if any.  If there is not any passes completed, then it does not print that timeline for space conservation.  It also records the percentages of how many passes occurred at each specific timeline.
    PARAMETERS:
        race - The race dictionary contains the max_timelines dictionary that contains each timeline as a key and values as the number of passes completed at each one.
        combined_data - another dictionary containing information concerning timelines
        driver_info - list containing all car numbers
'''
def maxTimelinePasses(race, combined_data, driver_info):
    for timeline, num in race['max_timelines'].items():
        return_dictionary = best_timeline(combined_data["Overtake Mode"], int(timeline))
        timeline_driver_dict = most_passes_by_timeline(race, int(timeline), driver_info)
        for driver, p2pNum in return_dictionary.items():
            for carNum, passes in timeline_driver_dict.items():
                if num != 0:
                    if p2pNum != 1 and passes != 1:
                        print(f'{timeline:>25} :{num:>7}{round(num/len(race["RacePasses"])*100):>10}%{race["max_timelines_P2P"][timeline]:>15}{race["max_timelines_NonP2P"][timeline]:>22}{race["CarNotoName"][str(carNum)]:>29} - {passes} passes{race["CarNotoName"][str(driver)]:>29} - {p2pNum} uses')
                        break
                    elif p2pNum == 1 and passes != 1:
                        print(f'{timeline:>25} :{num:>7}{round(num/len(race["RacePasses"])*100):>10}%{race["max_timelines_P2P"][timeline]:>15}{race["max_timelines_NonP2P"][timeline]:>22}{race["CarNotoName"][str(carNum)]:>29} - {passes} passes{race["CarNotoName"][str(driver)]:>29} - {p2pNum} use')
                        break
                    elif p2pNum != 1 and passes == 1:
                        print(f'{timeline:>25} :{num:>7}{round(num/len(race["RacePasses"])*100):>10}%{race["max_timelines_P2P"][timeline]:>15}{race["max_timelines_NonP2P"][timeline]:>22}{race["CarNotoName"][str(carNum)]:>29} - {passes} pass{race["CarNotoName"][str(driver)]:>29} - {p2pNum} uses')
                        break
                    elif p2pNum == 1 and passes == 1:
                        print(f'{timeline:>25} :{num:>7}{round(num/len(race["RacePasses"])*100):>10}%{race["max_timelines_P2P"][timeline]:>15}{race["max_timelines_NonP2P"][timeline]:>22}{race["CarNotoName"][str(carNum)]:>29} - {passes} pass{race["CarNotoName"][str(driver)]:>29} - {p2pNum} use')
                        break

            break

'''
    averageLap
    Parameters:
        overtake_presses - a dictionary containing information on overtakes   
        driver_number - car number being searched for
    Return value: this function will return the average lap number a driver uses P2P
    This function assumes the overtake_presses dictionary will be in the same form as the dictionary built in
        the initialize_overtakes function
'''

def averageLap(overtake_presses, driver_number):

    totalLaps = 0
    keys = list(overtake_presses[driver_number]["Laps"].keys())
    iterator = 0
    for i in overtake_presses[driver_number]["Laps"]:
        totalLaps += (keys[iterator] + 1) * overtake_presses[driver_number]["Laps"][i]
        iterator += 1

    if overtake_presses[driver_number]["Overtake"] > 0:
        return totalLaps / overtake_presses[driver_number]["Overtake"]
    else:
        return 0

'''
    transponder_to_carNo
    Parameters:
        driver_info - a dictionary containing information separated by driver, this dictionary must contain "TranNr" and "CarNo" keys for this function to work
        search_number - the transponder number the function searches for in the dictionary
    Return value: function returns the Car Number of the car with the matching transponder number, if there is not car with a matching transponder number, the function returns NULL
    This function searches a dictionary containing driver information to determine the car number that corresponds with a transponder number passed to the function.
    If the value is found, then the Car Number is returned.

'''
def transponder_to_carNo(driver_info, search_number):
    for driver in driver_info:
        if driver["TranNr"] == search_number:
            return driver["CarNo"]

    return NULL
'''
    P2PLeft
    This function returns the number of seconds remaining of P2P for a certain driver
    PARAMETERS:
        race - dictionary containing all racing statistics
        driver_number - Car Number
    If a driver has used Push to Pass, his or her most recent entry will be found.  The number of seconds of Push to Pass remaining will be returned, or 200 will be returned if no entries are found for that driver
'''
def P2PLeft(race, driver_number):
    for entry in reversed(race["Overtakes"]):
        if driver_number == transponder_to_carNo(race["Competitors"], entry["TranNr"]):
            return entry["OvertakeRemain"]
    return 200

'''
    calcP2PPosition
    Parameters:
        racePasses - a dictionary containing information on lapped Passes
        isP2P - a boolean variable, denotes if the values for P2P or nonP2P needs to be calculated
    Return value: this function will return the number of P2P or nonP2P passes for overtaken cars
    This function assumes the racePasses dictionary will be in the same form as the dictionary built in
        the initialize_racePasses function
'''

def calcP2PPosition(racePasses, isP2P):

	if isP2P:
		P2Psum = 0
		for car in racePasses:
			P2Psum += racePasses[car]['Overtaker']['P2P']

		return P2Psum
	
	else:
		nonP2Psum = 0
		for car in racePasses:
			nonP2Psum += racePasses[car]['Overtaker']['~P2P']

		return nonP2Psum


'''
    calc_lapped_P2P
    Parameters:
        lappedPasses - a dictionary containing information on lapped Passes
        isP2P - a boolean variable, denotes if the values for P2P or nonP2P needs to be calculated
    Return value: this function will return the number of P2P or nonP2P passes for lapped cars
    This function assumes the lappedPasses dictionary will be in the same form as the dictionary built in
        the initialize_lappedPasses function
'''
def calc_lapped_P2P(lappedPasses, isP2P):

	if isP2P:
		P2Psum = 0
		for car in lappedPasses:
			P2Psum += lappedPasses[car]['LeadCar']['P2P']

		return P2Psum
	
	else:
		notP2Psum = 0
		for car in lappedPasses:
			notP2Psum += lappedPasses[car]['LeadCar']['~P2P']

		return notP2Psum



'''
    max_position_P2P
    This function calculates and returns the car number and number of passes for positionof the driver that has passed the most cars using Push to Pass.
    Parameters:
        racePasses_data - a dictionary containing information on passes for position
        driver_list - list of car numbers

'''
def max_position_P2P(racePasses_data, driver_list):
    max_val = 0
    max_key = driver_list[0]
    for i in driver_list:
        if racePasses_data[i]["Overtaker"]["P2P"] > max_val:
            max_val = racePasses_data[i]["Overtaker"]["P2P"]
            max_key = i

    maximum = {}
    maximum[max_key] = max_val
    return maximum 

'''
    max_position_nonP2P
    This function calculates and returns the car number and number of passes for position of the driver that has passed the most cars not using Push to Pass.
    Parameters:
        racePasses_data - a dictionary containing information on passes for position
        driver_list - list of car numbers
'''
def max_position_nonP2P(racePasses_data, driver_list):
    max_val = 0
    max_key = driver_list[0]
    for i in driver_list:
        if racePasses_data[i]["Overtaker"]["~P2P"] > max_val:
            max_val = racePasses_data[i]["Overtaker"]["~P2P"]
            max_key = i

    maximum = {}
    maximum[max_key] = max_val
    return maximum 

'''
    max_lapped_P2P
    This function calculates and returns the car number and number of lapped passes of the driver that has lapped the most cars using P2P.
    Paramenters:
        lappedPasses_data - dictionary containing information on lapped passes
        driver_list - list of car numbers
'''
def max_lapped_P2P(lappedPasses_data, driver_list):
    max_val = 0
    max_key = driver_list[0]
    for i in driver_list:
        if lappedPasses_data[i]["LeadCar"]["P2P"] > max_val:
            max_val = lappedPasses_data[i]["LeadCar"]["P2P"]
            max_key = i

    maximum = {}
    maximum[max_key] = max_val
    return maximum 

'''
    max_lapped_nonP2P
    This function calculates and returns the car number and number of lapped passes of the driver that has lapped the most cars not using P2P.
        lappedPasses_data - dictionary containing information on lapped passes
        driver_list - list of car numbers
'''
def max_lapped_nonP2P(lappedPasses_data, driver_list):
    max_val = 0
    max_key = driver_list[0]
    for i in driver_list:
        if lappedPasses_data[i]["LeadCar"]["~P2P"] >= max_val:
            max_val = lappedPasses_data[i]["LeadCar"]["~P2P"]
            max_key = i

    maximum = {}
    maximum[max_key] = max_val
    return maximum 

'''
	max_timeline
	Parameters:
	    overtake_data - a dictionary passes to the function containing data concerning the number of times drivers used overtake mode at a checkpoint on track
	    driver_number - the transponder number referring to the driver's data the function will be checking
	Return value - this function returns a dictionary with single key, being the number corresponding to a checkpoint, and value, the number of times overtake mode is used at that checkpoint
	This function will calculate the maximum value in the overtake_data[driver_number]["TimelineIDs"] dictionary and return a dictionary with the max value and corresponding key
'''
def max_timeline(overtake_data, driver_number):
    
    max_val = max(overtake_data[driver_number]["TimelineIDs"].values())
    max_keys = []
    for i in overtake_data[driver_number]["TimelineIDs"]:
        if overtake_data[driver_number]["TimelineIDs"][i] == max_val:
            max_keys.append(i)
    max_dict = {}
    max_dict["Key(s)"] = max_keys
    max_dict["Value"] = max_val
    return max_dict


'''
	initialize_lappedPasses
	Parameters:
	    lappedPasses - a dictionary that will be intitialized in this function
	    driver_list - a data structure containing the transponder numbers of participating drivers
	The function will return the "lappedPasses" dictionary after its is initialized.
	The lappedPasses dictionary is initialized in the following format.
'''
def initialize_lappedPasses(lappedPasses, driver_list):

    for Transponder_Number in driver_list:
        if Transponder_Number not in lappedPasses:
            lappedPasses[Transponder_Number] = {}
            lappedPasses[Transponder_Number]["LappedCar"] = {}
            lappedPasses[Transponder_Number]["LeadCar"] = {}
            lappedPasses[Transponder_Number]["LappedCar"]["OppP2P"] = 0
            lappedPasses[Transponder_Number]["LappedCar"]["~OppP2P"] = 0
            lappedPasses[Transponder_Number]["LeadCar"]["P2P"] = 0
            lappedPasses[Transponder_Number]["LeadCar"]["~P2P"] = 0

    return lappedPasses

'''
    update_lappedPasses
    Parameters:
        lapped_car - the number of the driver who is being lapped
        lead_car - the number of the driver who is passing the lapped car
        lappedPasses - a dictionary containing information on lapped Passes
        use_P2P - a boolean variable, denotes if the passing driver has push to pass enabled
    Return value: this function will return an updated version of the lappedPasses dictionary
    This function assumes the lappedPasses dictionary will be in the same form as the dictionary built in the initialize_lappedPasses function
'''
def update_lappedPasses(lapped_car, lead_car, lappedPasses, use_P2P):

    if use_P2P:
        lappedPasses[lapped_car]["LappedCar"]["OppP2P"] += 1
        lappedPasses[lead_car]["LeadCar"]["P2P"] += 1
    else:
        lappedPasses[lapped_car]["LappedCar"]["~OppP2P"] += 1
        lappedPasses[lead_car]["LeadCar"]["~P2P"] += 1

    return lappedPasses

'''
    calc_percentage
    Parameters:
        calc_P2P - a boolean variable passed to the function, determines whether the function will return the percentage of 
					Push to Pass overtakes completed or non Push to Pass overtakes completed, default value is false
        P2P - the number of passes completed by a driver using Push to Pass, default value is 0
        not_P2P - the number of passes completed by a driver not using Push to Pass, the default value is 0
        totalPasses - the total number of passes completed by the driver during the race
    The value returned by this function is the percentage of passes completed either using or not using Push to Pass, depending on the calc_P2P variable.
		The return value is a double value which should be between 0 and 100.
		
		DRIVER_P2P_Percentage = calc_percentage(True, P2P=data[TransponderNumber][Overtaker][P2P], total_passes=)
'''
def calc_percentage(P2P=0, not_P2P=0, calc_P2P=False):
    totalPasses = not_P2P + P2P
    if totalPasses == 0:
        return 0


    if calc_P2P == True:
        return (P2P/totalPasses) * 100
    return (not_P2P/totalPasses) * 100



'''
    initialize_racePasses
    Parameters:
        racePasses - the dictionary that is being initialized in this function
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
def initialize_racePasses(racePasses, driver_list):

    for Transponder_Number in driver_list:
        if Transponder_Number not in racePasses:
            racePasses[Transponder_Number] = {}
            racePasses[Transponder_Number]["Overtaker"] = {}
            racePasses[Transponder_Number]["Overtaken"] = {}
            racePasses[Transponder_Number]["Overtaker"]["P2P"] = 0
            racePasses[Transponder_Number]["Overtaker"]["~P2P"] = 0
            racePasses[Transponder_Number]["Overtaker"]["OppP2P"] = 0
            racePasses[Transponder_Number]["Overtaker"]["~OppP2P"] = 0
            racePasses[Transponder_Number]["Overtaken"]["P2P"] = 0
            racePasses[Transponder_Number]["Overtaken"]["~P2P"] = 0
            racePasses[Transponder_Number]["Overtaken"]["OppP2P"] = 0
            racePasses[Transponder_Number]["Overtaken"]["~OppP2P"] = 0
    return racePasses


'''
    update_racePasses
    Parameters:
        passing_driver - the transponder number of the driver who has completed the overtake
        passed_driver - the transponder number of the driver who has just been overtaken
        racePasses - the dictionary containing data on pass statistics which is being updated and returned in this function
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
def update_racePasses(passing_driver, passed_driver, racePasses, passing_P2P=False, passed_P2P=False):

    if(passing_P2P):
        racePasses[passing_driver]["Overtaker"]["P2P"] += 1
        racePasses[passed_driver]["Overtaken"]["OppP2P"] += 1
    else:
        racePasses[passing_driver]["Overtaker"]["~P2P"] += 1
        racePasses[passed_driver]["Overtaken"]["~OppP2P"] += 1

    if(passed_P2P):
        racePasses[passing_driver]["Overtaker"]["OppP2P"] += 1
        racePasses[passed_driver]["Overtaken"]["P2P"] += 1
    else:
        racePasses[passing_driver]["Overtaker"]["~OppP2P"] += 1
        racePasses[passed_driver]["Overtaken"]["~P2P"] += 1

    return racePasses


'''
    initialize_overtakes
    Parameters:
        overtake_presses - the dictionary that will be initialized and returned from the function
        driver_list - a data structure containing the transponder number of all the drivers
    This function will build the dictionary needed by the update_overtakes function. The format of "data" in this function
    will be made to match the format of data in that function.
    The keys of the dictionary will be:
        Transponder_Number - the transponder number of the driver using the overtake button
        "Laps" - contains a dictionary containing lap numbers corresponding to the laps the driver used the overtake button
        "TimelineIDs" - a dictionary the next TimelineIDs passed by the driver after pushing the overtake button being the keys
        "Overtake" - contains a dictionary that will take contain keys for the beginning and end of the driver using overtake mode
        "Start" - the next TimelineID passed after a driver uses push to pass
        "End" - the final TimelineID passed while a driver is using push to pass
'''
def initialize_overtakes(overtake_presses, driver_list):
    for Transponder_Number in driver_list:
        if Transponder_Number not in overtake_presses:
            overtake_presses[Transponder_Number] = {}
            overtake_presses[Transponder_Number]["Laps"] = {}
            overtake_presses[Transponder_Number]["TimelineIDs"] = {}
            overtake_presses[Transponder_Number]["Overtake"] = 0

    return overtake_presses


'''
    update_overtakes
    Parameters:
        driver_number - the number of the driver whose information is being updated
        overtake_presses - dictionary containing various statistics about a driver's use of P2P
        lap_number - lap number that overtake is used
        TimelineID = specific timeline P2P was used
    This function will update "data" to contain information including, how many times does a driver use overtake mode on each lap,
    how many times does a driver use overtake mode at each TimelineID on the track, and where does the driver press and release the
    overtake button each time they use it.
    The data dictionary will need to be in the following format to work properly:
        data{
            Transponder_Number: {"Laps": {'0': 0, 1: 0, ...}, "TimelineIDs": {'1': 0, 2: 0, ...}, "Overtake" {1: {"Start": 1, "End": 3}, ...}},
            Transponder_Number: {"Laps": {'0': 0, 1: 0, ...}, "TimelineIDs": {'1': 0, 2: 0, ...}, "Overtake" {1: {"Start": 1, "End": 3}, ...}},
            ...,
            Transponder_Number: {"Laps": {0: 0, 1: 0, ...}, "TimelineIDs": {1: 0, 2: 0, ...}, "Overtake" {1: {"Start": 1, "End": 3}, ...}}
        }
'''
def update_overtakes(driver_number, overtake_presses, lap_number, Timeline_ID):
    if lap_number not in overtake_presses[driver_number]["Laps"]:
        overtake_presses[driver_number]["Laps"][lap_number] = 1
    else:
        overtake_presses[driver_number]["Laps"][lap_number] += 1
    
    if Timeline_ID not in overtake_presses[driver_number]["TimelineIDs"]:
        overtake_presses[driver_number]["TimelineIDs"][Timeline_ID] = 1
    else:
        overtake_presses[driver_number]["TimelineIDs"][Timeline_ID] += 1

    overtake_presses[driver_number]["Overtake"] += 1
    return overtake_presses


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


'''
    checkOvertake
    This function accesses the given dictionaries to match a certain pass occurring on-track and the time that it occurred to determine if the driver utilized Push to Pass to perform the pass. This function iterates through the race["Passings"] dictionary to find the timeline entry containing the same PassingID.  Then, a comparison is made to determine if the passing driver was aided by Push to Pass. From there, information will be sent to stdout and other statistics functions to provide the user.
    PARAMETERS:
        race = the dictionary containing all of the statistics and timeline-generated entries from the race
        PassingID = the current ID given to the pass that just occurred on-track that can be matched to a particular timeline and ElapsedTime entry in race
        driverOvertakes = the dictionary that uses the driver transponder numbers as keys and stores the last elapsed time value + 30 seconds of when the driver last used Push to Pass
'''
def checkOvertake(race, PassingID, driverOvertakes):
    for entry in race["Passings"]:
        if PassingID == entry["PassingID"]:
            if entry["ElapsedTime"] < driverOvertakes[entry["TranNr"]]:
                return True
            else:
                return False


'''
    initializeRaceDictionary
    This function creates the race dictionary that handles all of the input taken in from the timelines around the racetrack.  This function calls the initializeDriverInfo function to initialize the driver and timeline information before the race begins.  It then returns the race dictionary.
    PARAMETERS:
        race = the dictionary containing all of the statistics and timeline-generated entries from the race
'''
def initializeRaceDictionary():
    race = {}

    race = initializeDriverInfo(race)

    race = initializeCarNotoName(race)

    race['TotalPasses'] = {}
    race['max_timelines'] = {}
    race['max_timelines_P2P'] = {}
    race['max_timelines_NonP2P'] = {}
    race['best_timeline_passes'] = {}

    race['Passings'] = []
    race['Overtakes'] = []
    race['RacePasses'] = []
    race['RaceEvents'] = []
    return race


'''
    initializeCarNotoName
    This function creates a dictionary within the race dictionary that uses the car numbers as keys and formats the drivers' first and last names as values
    PARAMETERS:
        race = The race['CarNotoName'] dictionary is initialized
'''
def initializeCarNotoName(race):
    race['CarNotoName'] = {}
    for entry in race['Competitors']:
        race['CarNotoName'][entry['CarNo']] = f'{entry["FirstName"]} {entry["LastName"]}'
    return race


'''
    initializeDriverInfo
    This function is called within the initializeRaceDictionary function.  This function takes in a file called "initial.jsonl" and parses out the information about the competitors and the timelines around the racetrack.  Then, this function loads that data into the race dictionary and returns it to the other function.
    PARAMETERS:
        race = the dictionary containing all of the statistics and timeline-generated entries from the race

    The format of the initial.jsonl file must be as follows:
    {
        "Competitors" : [
            {"FirstName": "Felix", "LastName": "Rosenqvist", "CarNo": "10", "TranNr": 3463610},
            {"FirstName": "Will", "LastName": "Power", "CarNo": "12", "TranNr": 5596122},
            ...
        ],
        "Timelines" : [
            {"TimelineID": 1, "Name": "SF", "Order": 0},
            {"TimelineID": 2, "Name": "SFT", "Order": 1},
            ...
        ]
    }
'''
def initializeDriverInfo(race):
    with open('initial.jsonl') as json_file:
        race = json.load(json_file)

    return race


'''
    initializeDriverOvertakesDict
    This function takes in the race dictionary and initializes the driverOvertakes dictionary.  This dictionary will be used to store a value that is 30 seconds after the driver last used Push to Pass.  These values are stored under the corresponding key that is equal to the transponder number of each car.
    PARAMETERS: 
        race = the dictionary containing all of the statistics and timeline-generated entries from the race
        driverOvertakes = the dictionary that contains the transponder number of each car as keys.  Each key contains a value that is 30 seconds more than the last time each driver used Push to Pass.

        The driverOvertakes dictionary is formatted as follows:
        { 3463610 : 10035000, 5596122 : 25674978, ... }
'''
def initializeDriverOvertakesDict(race):
    driverOvertakes = {}
    for driverDict in race['Competitors']:
        driverOvertakes[driverDict['TranNr']] = 0

    return driverOvertakes


'''
    entryComparisons
    This function is called from the main function after every line is taken in from stdin.  It essentially sorts the newEntry dictionary to see if it is a "Passings" entry, a "Overtakes" entry, or a "RacePasses" entry.  Then it performs additional checks before appending that dictionary to the correct list.  It also updates the driverOvertakes dictionary every time a new "Overtakes" entry is detected.
    PARAMETERS:
        race = the dictionary containing all of the statistics and timeline-generated entries from the race
        newEntry = the dictionary taken in from stdin that is updated during every iteration
        driverOvertakes = the dictionary that contains the transponder number of each car as keys.  Each key contains a value that is 30 seconds more than the last time each driver used Push to Pass.
        combined_data = another dictionary containing various race statistics
        driver_list = list containing all car numbers
        
        The race dictionary will continue to be updated in the following format:
        {
            "Competitors" : [
                {"FirstName": "Felix", "LastName": "Rosenqvist", "CarNo": "10", "TranNr": 3463610},
                {"FirstName": "Will", "LastName": "Power", "CarNo": "12", "TranNr": 5596122},
                ...
            ],
            "Timelines" : [
                {"TimelineID": 1, "Name": "SF", "Order": 0},
                {"TimelineID": 2, "Name": "SFT", "Order": 1},
                ...
            ],
            "Passings" : [
                {"PassingID": 189954, "PassingTime": 428647957, "TranNr": 4718059, "TimelineID": 1, "Pit": false, "Flag": 1, "ElapsedTime": 2124557, "LapCount": 2, "LeaderLap": 2},
                ...
            ],
            "Overtakes": [
                {"TranNr": 8193597, "OvertakeNo": 3, "OvertakeRemain": 189, "SecondsOfPush": 3, "SecondsBeforeTimeline": 5, "TimelineID": 1, "Lap": 4, "PassingTime": 430842219},
                ...
            ],
            "RacePasses" : [
                {"CarNo": "26", "CarPassed": "9", "Lap": 0, "TimelineID": 8, "ForPosition": true, "PassingID": 188308, "Position": 14},
                ...
            ]
        }
'''
def entryComparisons(race, newEntry, driverOvertakes, combined_data, driver_list):
    P2P_check = False
    # If Statement Places newEntry in Correct Nested Dictionary with Additional Conditions
    # This If Statement takes in any newEntry that contains data from cars passing timelines.
    if 'ElapsedTime' in newEntry:

        # Conditional Statement to Avoid Appending Unnecessary Data to Dictionary
        if newEntry['ElapsedTime'] >= 0 and newEntry['Flag'] == 1 and not newEntry['Pit']:
            race['Passings'].append(newEntry)
        return combined_data

    # This Elif Statement appends any data associated with Overtakes.
    elif 'OvertakeNo' in newEntry:
        P2P_check = False
        race['Overtakes'].append(newEntry)
        update_overtakes(transponder_to_carNo(race["Competitors"], newEntry["TranNr"]), combined_data["Overtake Mode"], newEntry["Lap"], newEntry["TimelineID"])
        # This For Loop checks to find the corresponding Timeline Pass for a car when they use Push to Pass and logs that time with an added 30 seconds into a dictionary.
        for Passing in race['Passings']:
            if newEntry['PassingTime'] == Passing['PassingTime']:
                driverOvertakes[newEntry['TranNr']] = Passing['ElapsedTime'] + 300000 - (newEntry['SecondsBeforeTimeline'] * 10000)
                break


    # This Elif Statement appends any data associated with Passes
    elif 'CarPassed' in newEntry:
        for entry in race["Passings"]:
            if entry["PassingID"] == newEntry["PassingID"] and not entry["Pit"]:
                race['RacePasses'].append(newEntry)
                race['TotalPasses'][str(newEntry['CarNo'])] += 1
                race['max_timelines'][str(newEntry['TimelineID'])] += 1
                race['best_timeline_passes'][newEntry['CarNo']][newEntry['TimelineID']] += 1
                if newEntry["ForPosition"]:
                    P2P_check = checkOvertake(race, newEntry["PassingID"], driverOvertakes)
                    update_racePasses(newEntry['CarNo'], newEntry['CarPassed'], combined_data["Passes"], P2P_check, False)
                    if P2P_check and not entry["Pit"]:
                        race['max_timelines_P2P'][str(newEntry['TimelineID'])] += 1
                    elif not P2P_check and not entry["Pit"]:
                        race['max_timelines_NonP2P'][str(newEntry['TimelineID'])] += 1
                    break
                else:
                    P2P_check = checkOvertake(race, newEntry["PassingID"], driverOvertakes)
                    update_lappedPasses(newEntry['CarPassed'], newEntry['CarNo'], combined_data["Lapped Passes"], P2P_check)
                    if P2P_check and not entry["Pit"]:
                        race['max_timelines_P2P'][str(newEntry['TimelineID'])] += 1
                    elif not P2P_check and not entry["Pit"]:
                        race['max_timelines_NonP2P'][str(newEntry['TimelineID'])] += 1
                    break

    displayScreen(race, combined_data, newEntry, P2P_check, driver_list)
    return combined_data


'''
    initializeTotalPasses
    This function is called from the main function and initializes the TotalPasses and max_timelines dictionaries to zero.  The TotalPasses dictionary records how many passes each driver makes.  The max_timelines dictionary records how many passes occur at each timeline.
    PARAMETERS:
        race = dictionary that contains these two nested dictionaries and others
        driver_list = list containing the car numbers
    The race dictionary is returned
'''
def initializeTotalPasses(race, driver_list):
    for num in driver_list:
        race['TotalPasses'][str(num)] = 0
        race['best_timeline_passes'][num] = {}
    for timeline in race['Timelines']:
        race['max_timelines'][str(timeline['TimelineID'])] = 0
        race['max_timelines_P2P'][str(timeline['TimelineID'])] = 0
        race['max_timelines_NonP2P'][str(timeline['TimelineID'])] = 0
        for num2 in driver_list:
            race['best_timeline_passes'][num2][timeline['TimelineID']] = 0
    return race

'''
    print_to_stream
    This function is called from the main function at the end of program execution to create a txt file containing the final results of the race that can be analyzed by IndyCar and distributed to racing teams and other stakeholders
    PARAMETERS:
        NONE
    A text file (completerace.txt) will be created by calling the displayScreen function.
'''
def print_to_stream(race, combined_data, newEntry, P2P_check, driver_list):
    original_stdout = sys.stdout
    with open('completerace.txt', 'w') as f:
        sys.stdout = f
        displayScreen(race, combined_data, newEntry, P2P_check, driver_list)
        sys.stdout = original_stdout
        displayScreen(race, combined_data, newEntry, P2P_check, driver_list)


'''
    print_to_json
    This function prints the collected dictionaries to an external JSON file that can be accessed after the race.
    PARAMETERS:
        race - dictionary to be printed
        combined_data - dictionary to be printed
    A JSON file called "currentRaceDictionaries.json" will be created.
'''
def print_to_json(race, combined_data):
    outfile = open("currentRaceDictionaries.json", "w")
    json.dump(race, outfile, indent=4)
    json.dump(combined_data, outfile, indent=4)
    outfile.close()

def main():
    # Initialize stdin and dictionaries
    stream = sys.stdin
    race = initializeRaceDictionary()

    driver_list = []
    for i in race["Competitors"]:
        driver_list.append(i["CarNo"])

    newEntry = {}
    driverOvertakes = initializeDriverOvertakesDict(race)

    race = initializeTotalPasses(race, driver_list)

    overtake_data = {}
    overtake_data = initialize_overtakes(overtake_data, driver_list)

    racePasses_data = {}
    racePasses_data = initialize_racePasses(racePasses_data, driver_list)


    lappedPasses_data = {}
    lappedPasses_data = initialize_lappedPasses(lappedPasses_data, driver_list)

    combined_data = {}
    combined_data["Passes"] = racePasses_data
    combined_data["Overtake Mode"] = overtake_data
    combined_data["Lapped Passes"] = lappedPasses_data
    
    # For Loop Receives One Entry Per Loop From The Generator And Parses It From JSON to a Python Dictionary
    for line in readEntries(stream):
        newEntry = json.loads(line)
        combined_data = entryComparisons(race, newEntry, driverOvertakes, combined_data, driver_list)

    print_to_stream(race, combined_data, {}, False, driver_list)
    print_to_json(race, combined_data)


if __name__ == '__main__':
    main()

