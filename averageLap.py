#!/usr/bin/env python3

'''
    averageLap
    Parameters:
        overtake_presses - a dictionary containing information on overtakes        
    Return value: this function will return the average lap number a driver uses P2P
    This function assumes the overtake_presses dictionary will be in the same form as the dictionary built in
        the initialize_overtakes function
'''

def averageLap(overtake_presses):

	counter = 0
	avgLap = 0

	for car in overtake_presses:
		
		lapNumbers = list(car['Laps'].keys())
		numOvertakes = list(car['Laps'].values())

		for i in range(len(lapNumbers)):
			
			avglap += int(lapNumbers[i]) * numOvertakes[i]
			counter += numOvertakes[i]

	return float(avglLap) / counter
		
				
			
