#!/usr/bin/env python3

import json
import sys
import operator


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