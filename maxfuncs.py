'''
    max_position_P2P
    Parameters:
        racePasses_data - a dictionary containing information
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
        racePasses_data - a dictionary containing information
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
			overtake_data - a dictionary passes to the function containing data concerning the number of times drivers used 
				overtake mode at a checkpoint on track
			driver_number - the transponder number referring to the driver's data the function will be checking
	Return value - this function returns a dictionary with single key, being the number corresponding to a checkpoint, 
		and value, the number of times overtake mode is used at that checkpoint
	This function will calculate the maximum value in the overtake_data[driver_number]["TimelineIDs"] dictionary and 
		return a dictionary with the max value and corresponding key
'''
def max_timeline(overtake_data, driver_number):
    
    max_val = max(overtake_data[driver_number]["TimelineIDs"].values())
    max_keys = []
    for i in overtake_data[driver_number]["TimelineIDs"]:
        if overtake_data[driver_number]["TimelineIDs"][i] == max_val
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
	The lappedPasses dictionary is initialized in the following format:
		 

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


