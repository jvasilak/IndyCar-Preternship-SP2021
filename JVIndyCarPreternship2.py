#!/usr/bin/env python3

import json
import sys
import operator

'''
    averageLap
    Parameters:
        overtake_presses - a dictionary containing information on overtakes 
        driver_number - the car number denoting the driver the function is getting information on     
    Return value: this function will return the average lap number a driver uses P2P
    This function assumes the overtake_presses dictionary will be in the same form as the dictionary built in
        the initialize_overtakes function
'''

def averageLap(overtake_presses, driver_number):

    totalLaps= 0
    keys = list(overtake_presses[driver_number]["Laps"].keys())
    iterator = 0
    for i in overtake_presses[driver_number]["Laps"]:
        totalLaps += (keys[iterator] + 1) * overtake_presses[driver_number]["Laps"][i]
        iterator += 1
    return_dictionary = {}
    return_dictionary["Car Number"] = driver_number
    return_dictionary["Average Lap"] = totalLaps / overtake_presses[driver_number]["Overtake Presses"]
    return return_dictionary

'''
    transponder_to_carNo
    Parameters:
        driver_info - a dictionary containing information separated by driver, this dictionary must contain "TranNr" and "CarNo" keys for this function to work
        search_number - the transponder number the function searches for in the dictionary
    Return value: function returns the Car Number of the car with the matching transponder number, if there is not car with a matching transponder number, the function returns NULL
    This function searches a dictionary containing driver information to determine the car number that corresponds with a transponder number passed to the function.
    If the value is found, then the Car Number is returned, if the search number does not exist, then the function will return NULL.
'''
def transponder_to_carNo(driver_info, search_number):
    for driver in driver_info:
        if driver["TranNr"] == search_number:
            return driver["CarNo"]

    return -1

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
    Parameters:
        racePasses_data - a dictionary containing information about driver overtakes for position
        driver_list - a list structure containing the car numbers of drivers
    Return value: the function will return a dictionary containing the driver number and number of overtakes completed
        using Push 2 Pass
    This function parses through the racePasses_data dictionary and records and returns the driver with the most Push 2
        Pass overtakes for position, as well as the number of overtakes completed by the driver
'''
def max_position_P2P(racePasses_data, driver_list):
    max_val = 0
    for i in driver_list:
        if racePasses_data[i]["Overtaker"]["P2P"] > max_val:
            max_val = racePasses_data[i]["Overtaker"]["P2P"]
            max_key = i

    maximum = {}
    maximum[max_key] = max_val
    return maximum 

'''
    max_position_nonP2P
    Parameters:
        racePasses_data - a dictionary containing information about driver overtakes for position
        driver_list - a list structure containing the car numbers of drivers
    Return value: the function will return a dictionary containing the driver number and number of overtakes completed
        without using Push 2 Pass
    This function parses through the racePasses_data dictionary and records and returns the driver with the most non 
        Push 2 Pass overtakes for position, as well as the number of overtakes completed by the driver
'''
def max_position_nonP2P(racePasses_data, driver_list):
    max_val = 0
    for i in driver_list:
        if racePasses_data[i]["Overtaker"]["~P2P"] > max_val:
            max_val = racePasses_data[i]["Overtaker"]["~P2P"]
            max_key = i

    maximum = {}
    maximum[max_key] = max_val
    return maximum 

'''
    max_lapped_P2P
    Parameters:
        lappedPasses_data - a dictionary containing information about lapped passes for each driver
        driver_list - a list structure containing the car numbers of drivers
    Return Value: this function returns a dictionary with the driver with the most lapped passes using P2P, the key is
        the driver's car number and the value is the number of lapped passes completed
    
'''
def max_lapped_P2P(lappedPasses_data, driver_list):
    max_val = 0
    for i in driver_list:
        if lappedPasses_data[i]["LeadCar"]["P2P"] > max_val:
            max_val = lappedPasses_data[i]["LeadCar"]["P2P"]
            max_key = i

    maximum = {}
    maximum[max_key] = max_val
    return maximum 

'''
    max_lapped_nonP2P
    Parameters:
        lappedPasses_data - a dictionary containing information about lapped passes for each driver
        driver_list - a list structure containing the car numbers of drivers
    Return Value: this function returns a dictionary with a single entry, where the key is the car number of the driver
        with the most lapped passes without using Push to Pass
    
'''
def max_lapped_nonP2P(lappedPasses_data, driver_list):
    max_val = 0
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
			overtake_data - a dictionary passed to the function containing data on the number of times drivers used 
				overtake mode at a checkpoint on track
			driver_number - the car number referring to the driver's data the function will be checking
	Return value - this function returns a dictionary with single key, being the number corresponding to a checkpoint, 
		and value, the number of times overtake mode is used at that checkpoint
	This function will calculate the maximum value in the overtake_data[driver_number]["TimelineIDs"] dictionary and 
		return a dictionary with the max value and corresponding key
'''
def max_timeline(overtake_data, driver_number):
    
    max_val = max(overtake_data[driver_number]["TimelineIDs"].values())
    max_keys = []
    for i in overtake_data[driver_number]["TimelineIDs"]:
        if overtake_data[driver_number]["TimelineIDs"][i] == max_val:
            max_keys.append(i)
    max_dict = {}
    max_dict["Car Number"] = driver_number
    for i in max_keys:
        max_dict[i] = max_val
    return max_dict

'''
    best_timeline
    Parameters:
        overtake_data - the dictionary containing information on overtake presses for all drivers
        TimelineID - the number of the checkpoint being checked
    Return Value - this function returns a dictionary containg a driver number and the number of overtakes completed by the
        driver at the checkpoint number passed to this function
    This function will compare all drivers' statistics regarding overtake presses at a certain timeline to determine
        which driver has used it the most at a specific timeline
    
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

    if(max_val == 0):
        print(f"No overtake presses recorded at checkpoint {TimelineID}")

    for driver in driver_numbers:
        return_dictionary[driver] = max_val
    return return_dictionary



'''
	initialize_lappedPasses
	Parameters:
		lappedPasses - a dictionary that will be intitialized in this function
		driver_list - a data structure containing the transponder numbers of participating drivers
	The function will return the "lappedPasses" dictionary after its is initialized.
	The lappedPasses dictionary is initialized in the following format:
		 lappedPasses{
             Car_Number: {"LappedCar": {"OppP2P": 0, "~OppP2P": 0}, "LeadCar": {"P2P": 0, "~P2P": 0}},
             Car_Number: {"LappedCar": {"OppP2P": 0, "~OppP2P": 0}, "LeadCar": {"P2P": 0, "~P2P": 0}},
            ... 
             Car_Number: {"LappedCar": {"OppP2P": 0, "~OppP2P": 0}, "LeadCar": {"P2P": 0, "~P2P": 0}}
         }
    The keys of the lappedPasses dictionary are:
        Car_Number - the number assigned to the car
        LappedCar - denotes situations where Car_Number is the car is being passed
        LeadCar - denotes situations where Car_Number is the car passing the other car
        OppP2P - occurences when the other car is using P2P
        ~OppP2P - occurences when the other car is not using P2P
        P2P - occurences when Car_Number is using P2P
        ~P2P - occurences when Car_Number is not using P2P
'''
def initialize_lappedPasses(lappedPasses, driver_list):

    for Car_Number in driver_list:
        if Car_Number not in lappedPasses:
            lappedPasses[Car_Number] = {}
            lappedPasses[Car_Number]["LappedCar"] = {}
            lappedPasses[Car_Number]["LeadCar"] = {}
            lappedPasses[Car_Number]["LappedCar"]["OppP2P"] = 0
            lappedPasses[Car_Number]["LappedCar"]["~OppP2P"] = 0
            lappedPasses[Car_Number]["LeadCar"]["P2P"] = 0
            lappedPasses[Car_Number]["LeadCar"]["~P2P"] = 0

    return lappedPasses

'''
    update_lappedPasses
    Parameters:
        lapped_car - the car number of the driver who is being lapped
        lead_car - the transponder number of the driver who is passing the lapped car
        lappedPasses - a dictionary containing information on lapped Passes
        use_P2P - a boolean variable, denotes if the passing driver has push to pass enabled
    Return value: this function will return an updated version of the lappedPasses dictionary
    The values and keys updated in the dictionary will be determined by values passed to the function.
    This function assumes the lappedPasses dictionary will be in the same form as the dictionary built in
        the initialize_lappedPasses function
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
        total_passes - the total number of passes completed by the driver during the race
    The value returned by this function is the percentage of passes completed either using or not using Push to Pass, depending on the calc_P2P variable.
		The return value is a double value which should be between 0 and 100.
		
'''


def calc_percentage(P2P=0, not_P2P=0, calc_P2P=False):
    totalPasses = not_P2P + P2P
    if totalPasses == 0:
        print("Error: No pass data available")
        return 0


    if calc_P2P == True:
        return (P2P/totalPasses) * 100
    return (not_P2P/totalPasses) * 100



'''
    initialize_racePasses
    Parameters:
        racePasses - the dictionary that is being initialized in this function
        driver_list - a data structure containing the transponder numbers of participating drivers
    This function will initialize the racePasses dictionary, putting it in the format used by the update_racePasses function.
    Within this dictionary, there are multiple nested dictionaries.
    The keys of the racePasses are:
        Car_Number - the dictionary is initially divided by car number to separate data from each driver
        Overtaker - contains data regarding instances when this driver is the one doing the overtaking
        Overtaken - contains data regarding instances when this driver is the one being overtaken
        P2P - situations, either where the driver is overtaking another driver or is being overtaken, where Push to Pass is active for this driver
        ~P2P - situations where Push to Pass is not active for this driver
        OppP2P - situations where Push to Pass is active for the other driver involved in the overtake
        ~OppP2P - situations where Push to Pass is not active for the other driver involved in the overtake
'''
def initialize_racePasses(racePasses, driver_list):

    for Car_Number in driver_list:
        if Car_Number not in racePasses:
            racePasses[Car_Number] = {}
            racePasses[Car_Number]["Overtaker"] = {}
            racePasses[Car_Number]["Overtaken"] = {}
            racePasses[Car_Number]["Overtaker"]["P2P"] = 0
            racePasses[Car_Number]["Overtaker"]["~P2P"] = 0
            racePasses[Car_Number]["Overtaker"]["OppP2P"] = 0
            racePasses[Car_Number]["Overtaker"]["~OppP2P"] = 0
            racePasses[Car_Number]["Overtaken"]["P2P"] = 0
            racePasses[Car_Number]["Overtaken"]["~P2P"] = 0
            racePasses[Car_Number]["Overtaken"]["OppP2P"] = 0
            racePasses[Car_Number]["Overtaken"]["~OppP2P"] = 0
    return racePasses

'''
    update_racePasses
    Parameters:
        passing_driver - the car number of the driver who has completed the overtake
        passed_driver - the car number of the driver who has just been overtaken
        racePasses - the dictionary containing data on pass statistics which is being updated and returned in this function
        passing_P2P - a boolean value that is true if passing_driver has Push to Pass active, default is false
        passed_P2P - a boolean value that is true if passed_driver has Push to Pass active, default is false
    The function update_racePasses returns an updated version of the dictionary "data", which is a parameter passed to this fuction.
    Which values in the dictionary are updated is determined by whether passing_P2P or passed_P2P is true.
    Since all values in the dictionary that may be updated are integers, they are updated by adding one to the value each time.

    This function assumes the dictionary will be in the following format, where the '0's are the numbers being updated:
    data{
    Car_Number: {Overtaker{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}, Overtaken{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}},
    Car_Number: {Overtaker{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}, Overtaken{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}},
    ...,
    Car_Number: {Overtaker{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}, Overtaken{"P2P": 0, "~P2P": 0, "OppP2P": 0, "~OppP2P": 0}}
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
        Transponder_Number - the transponder number of the driver using the overtake button, contains a nested dictionary
        "Laps" - contains a dictionary containing lap numbers corresponding to the laps the driver used the overtake button
        "TimelineIDs" - a dictionary the next TimelineIDs passed by the driver after pushing the overtake button being the keys
        "Overtake Presses" - the total number of times a driver has used Push 2 Pass mode
'''
def initialize_overtakes(overtake_presses, driver_list):
    for Car_Number in driver_list:
        if Car_Number not in overtake_presses:
            overtake_presses[Car_Number] = {}
            overtake_presses[Car_Number]["Laps"] = {}
            overtake_presses[Car_Number]["TimelineIDs"] = {}
            overtake_presses[Car_Number]["Overtake Presses"] = 0
        
        if Car_Number not in overtake_presses:
            print("Error inserting driver number.")
            return NULL

    return overtake_presses

'''
    update_overtakes
    Parameters:
        driver_number - the number of the driver whose information is being updated
        overtake_presses - the dictionary containing data on overtake press statistics which is being updated and returned in this function
        lap_number - the current lap driver_number's car is on
        Timeline_ID - the most recent on track checkpoint passed by the car
    This function will update the dictionary to contain information including, how many times does a driver use overtake mode on each lap,
    how many times does a driver use overtake mode at each TimelineID on the track, and how many time the driver has used the overtake button.
    The data dictionary will need to be in the following format to work properly:
        data{
            Car_Number: {"Laps": {0: 0, 1: 0, ...}, "TimelineIDs": {1: 0, 2: 0, ...}, "Overtake Presses": 1},
            Car_Number: {"Laps": {0: 0, 1: 0, ...}, "TimelineIDs": {1: 0, 2: 0, ...}, "Overtake Presses": 1},
            ...,
            Car_Number: {"Laps": {0: 0, 1: 0, ...}, "TimelineIDs": {1: 0, 2: 0, ...}, "Overtake Presses": 1}
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

    overtake_presses[driver_number]["Overtake Presses"] += 1
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
                # Update Pass Made with Push 2 Pass Dictionary
                # Update Pass made with certain timeline
                print(f"Pass Made With P2P at Timeline " + str(entry["TimelineID"]))
                return True
            else:
                # Update Pass Made without Push 2 Pass Dictionary
                # Update Pass made with certain timeline
                print(f"Pass Made WITHOUT P2P at Timeline " + str(entry["TimelineID"]));
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

    race['Passings'] = []
    race['Overtakes'] = []
    race['RacePasses'] = []
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
def entryComparisons(race, newEntry, driverOvertakes, combined_data):
    # If Statement Places newEntry in Correct Nested Dictionary with Additional Conditions
    # This If Statement takes in any newEntry that contains data from cars passing timelines.
    if 'ElapsedTime' in newEntry:

        # Conditional Statement to Avoid Appending Unnecessary Data to Dictionary
        if newEntry['ElapsedTime'] >= 0 and newEntry['Flag'] == 1 and not newEntry['Pit']:
            race['Passings'].append(newEntry)

    # This Elif Statement appends any data associated with Overtakes.
    elif 'OvertakeNo' in newEntry:
        race['Overtakes'].append(newEntry)
        update_overtakes(transponder_to_carNo(race["Competitors"], newEntry["TranNr"]), combined_data["Overtake Mode"], newEntry["Lap"], newEntry["TimelineID"])
        # This For Loop checks to find the corresponding Timeline Pass for a car when they use Push to Pass and logs that time with an added 30 seconds into a dictionary.
        for Passing in race['Passings']:
            if newEntry['PassingTime'] == Passing['PassingTime']:
                driverOvertakes[newEntry['TranNr']] = Passing['ElapsedTime'] + 300000 - (newEntry['SecondsBeforeTimeline'] * 10000)
                break

    # This Elif Statement appends any data associated with Passes
    elif 'CarPassed' in newEntry:
        race['RacePasses'].append(newEntry)
        if newEntry["ForPosition"]:
            P2P_check = checkOvertake(race, newEntry["PassingID"], driverOvertakes)
            update_racePasses(newEntry['CarNo'], newEntry['CarPassed'], combined_data["Passes"], P2P_check, False)
        else:
            P2P_check = checkOvertake(race, newEntry["PassingID"], driverOvertakes)
            update_lappedPasses(newEntry['CarPassed'], newEntry['CarNo'], combined_data["Lapped Passes"], P2P_check)
    
    return combined_data

def run_tests(combined_data):
    print()
    print("Check passes data: ")
    print(combined_data["Passes"])
    print()
    
    print("Check lapped passes data: ")
    print(combined_data["Lapped Passes"])
    print()

    print("Check overtake presses data:")
    print(combined_data["Overtake Mode"])
    print()

    print("Check calc_percentage true:")
    for i in driver_list:
        percent = calc_percentage(combined_data["Passes"][i]["Overtaker"]["P2P"], combined_data["Passes"][i]["Overtaker"]["~P2P"], True)
        print(f"Car Number {i}: {percent}%")
    print()

    print("Check calc_percentage false:")
    for i in driver_list:
        percent = calc_percentage(combined_data["Passes"][i]["Overtaker"]["P2P"], combined_data["Passes"][i]["Overtaker"]["~P2P"], False)
        print(f"Car Number {i}: {percent}%")
    print()

    max_P2P = max_position_P2P(combined_data["Passes"], driver_list)
    print(f"The highest number of P2P passes made by a driver is {max_P2P}")
    print()

    max_notP2P = max_position_nonP2P(combined_data["Passes"], driver_list)
    print(f"The highest number of non P2P passes made by a driver is {max_notP2P}")
    print()

    maxLappedP2P = max_lapped_P2P(combined_data["Lapped Passes"], driver_list)
    print(f"The highest number of lapped passes made by a driver using P2P is {maxLappedP2P}")
    print()

    maxLappednonP2P = max_lapped_nonP2P(combined_data["Lapped Passes"], driver_list)
    print(f"The highest number of lapped passes made by a driver without using P2P is {maxLappednonP2P}")
    print()

    print("Aidan's Functions Tested:")
    print()
    lapped_P2P_total = calc_lapped_P2P(combined_data["Lapped Passes"], True)
    print(f"Total Number of P2P lapped passes = {lapped_P2P_total}")
    print()

    lapped_notP2P_total = calc_lapped_P2P(combined_data["Lapped Passes"], False)
    print(f"Total Number of non P2P lapped passes = {lapped_notP2P_total}")
    print()

    position_P2P_total = calcP2PPosition(combined_data["Passes"], True)
    print(f"Total number of P2P passes for position = {position_P2P_total}")
    print()

    position_nonP2P_total = calcP2PPosition(combined_data["Passes"], False)
    print(f"Total number of non P2P passes for position = {position_nonP2P_total}")
    print()

    average = averageLap(combined_data["Overtake Mode"], '10')
    print(f"Average lap overtake pressed by drivers: {average}")
    print()
    
def week_3_tests(combined_data, race):
    #average = averageLap(combined_data["Overtake Mode"], '10')
    #print()
    #print(f"Average lap overtake pressed by car number 10: {average}")
    #print()

    print("Check overtake presses data:")
    print(combined_data["Overtake Mode"])
    print()

    #print("Testing Transponder to CarNo conversion:")
    #print(transponder_to_carNo(race["Competitors"], 5596122))
    #print()

    #print("Testing Transponder to CarNo failure:")
    #print(transponder_to_carNo(race["Competitors"], 100))
    #print()

    #print("Testing Max timeline:")
    #print(max_timeline(combined_data["Overtake Mode"], '10'))
    #print()
    

def main():
    # Initialize stdin and dictionaries
    stream = sys.stdin
    race = initializeRaceDictionary()

    driver_list = []
    for i in race["Competitors"]:
        driver_list.append(i["CarNo"])

    newEntry = {}
    driverOvertakes = initializeDriverOvertakesDict(race)

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
        combined_data = entryComparisons(race, newEntry, driverOvertakes, combined_data)

    #run_tests(combined_data)
    week_3_tests(combined_data, race)
    data = {}
    data = best_timeline(combined_data["Overtake Mode"], 5)
    print(data)


if __name__ == '__main__':
    main()

