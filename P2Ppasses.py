#!/usr/bin/env python3

'''
    calcP2P
    Parameters:
        lappedPasses - a dictionary containing information on lapped Passes
        isP2P - a boolean variable, denotes if the values for P2P or nonP2P needs to be calculated
    Return value: this function will return the number of P2P or nonP2P passes for lapped cars
    This function assumes the lappedPasses dictionary will be in the same form as the dictionary built in
        the initialize_lappedPasses function
'''

def calcP2P(lappedPasses, isP2P):

	if isP2P:
		P2Psum = 0
		for car in lappedPass:
			P2Psum += lappedPass[car]['LeadCar']['P2P']

		return P2Psum
	
	else:
		P2Psum = 0
		for car in lappedPass:
			P2Psum += lappedPass[car]['LeadCar']['~P2P']

		return P2Psum
	
