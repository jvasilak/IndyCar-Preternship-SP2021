#!/usr/bin/env python3

'''
    calcP2PPosition
    Parameters:
        racePasses - a dictionary containing information on lapped Passes
        isP2P - a boolean variable, denotes if the values for P2P or nonP2P needs to be calculated
    Return value: this function will return the number of P2P or nonP2P passes for overtaken cars
    This function assumes the racePasses dictionary will be in the same form as the dictionary built in
        the initialize_racePasses function
'''

def calcP2PPosition(racesPasses, isP2P):

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
	
