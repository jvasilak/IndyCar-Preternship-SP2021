#!/usr/bin/env python3

#IndyCar Preternship
#Percentage P2P Func
#This function is for calculating percentage of Push to Pass uses
#This reads in data from our dictionaries and returns a percentage
#Initialize variables: perP2P, P2P, noP2P, and total Passes.
#First we sum the passes that used P2P and ones that didnt
#If this total is 0, print error message

import json
import sys

P2P = 0
noP2P = 0
perP2P = True

def percentFunc(P2P, noP2P, perP2P):

    totalPasses = noP2P + P2P

    if perP2P == False:
        return (P2P/totalPasses) * 100
    return (noP2P/totalPasses) * 100

    if totalPasses == 0:
        print("Error: No pass data available")
        return 0
