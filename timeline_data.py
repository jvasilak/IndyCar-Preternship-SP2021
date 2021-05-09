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
