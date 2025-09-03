#Name: Michael Durkan
# Hash Table implemntation for vehicles

import math
import numpy as np
from DSALinkedList import DSALinkedList, ListEmptyError
from DSARoadGraph import DSAGraph, VertexNotFoundError, DuplicateVertexError, DuplicateEdgeError
from Vehicle import Vehicle

class Error(Exception):
    pass

class KeyNotFoundError(Exception):
    def __init__(self, message):
        self.message = message

class DSAHashEntry:
    def __init__(self, key = None, value = None):
        # Set key to input otherwise set key to empty string if not input
        if key is not None:
            self.key = key
        else:
            self.key = ""

        self.value = value

        # States: 0 = never used, 1 = used, -1 = formerly-used
        # Set state to 1 if key input otherwise set it to 0
        if key is not None:
            self.state = 1
        else:
            self.state = 0

# Based on DSA Hash Table From Prac 7 Submission
class VehicleHashTable: 
    def __init__(self, tableSize):
        if tableSize < 5:
            tableSize = 5
        # Set actual size to nextPrime of table size
        actualSize = self._nextPrime(tableSize)


        # Allocate hash array size of actual size with hash entries
        self.hashArray = np.empty(actualSize, dtype = object)
        for i in range(actualSize):
            self.hashArray[i] = DSAHashEntry()

        self.count = 0
        
        # Upper and lower threshold values for load factor - resizing
        self.lowerThreshold = 0.2
        self.upperThreshold = 0.7

    # Shift-Add-XOR Hash from lecture slides
    def _hash(self, vehicleID):
        hashIdx = 0
        for char in vehicleID:
            code = ord(char)
            hashIdx = hashIdx ^ ((hashIdx << 5) + (hashIdx << 2) + code)

        return abs(hashIdx) % len(self.hashArray)

    # stepHash function for calculating the step size in double hashing
    # based of lecture slides
    def _stepHash(self, vehicleID):
        hashVal = self._hash(vehicleID)
        stepHash = 5 - (hashVal % 5)
        if stepHash == 0:
            stepHash = 1
        return stepHash

    # Next prime improved from lecture slides
    def _nextPrime(self, startVal):
        if startVal % 2 == 0:
            primeVal = startVal - 1
        else:
            primeVal = startVal

        isPrime = False

        while not isPrime:
            primeVal += 2
            ii = 3
            isPrime = True
            rootVal = math.isqrt(primeVal)
            
            while ii <= rootVal and isPrime:
                if primeVal % ii == 0:
                    isPrime = False
                else:
                    ii += 2
            
        return primeVal
    
    def getLoadFactor(self):
        return self.count / len(self.hashArray)

    def insert(self, vehicle):
        vehicleID = vehicle._vehicleID
        loadFactor = self.getLoadFactor()
        if loadFactor >= self.upperThreshold:
            self._resize(len(self.hashArray) * 2)

        # Get hash value for the input key
        hashIdx = self._hash(vehicleID)
        stepSize = self._stepHash(vehicleID) # For double hashing of step size

        origIdx = hashIdx # Store in case hashtable is full
        found = False
        giveUp = False

        # Probe for slot to put in
        while not found and not giveUp:
            # Get entry at hash index
            entry = self.hashArray[hashIdx]

            # Check if slots empty or previously used
            if entry.state == 0 or entry.state == -1:
                # Insert key and value into the slot and incremment count
                self.hashArray[hashIdx] = DSAHashEntry(vehicleID, vehicle)
                self.count += 1
                found = True
            
            # Check if slot contains the same key and is used
            elif entry.key == vehicleID and entry.state == 1:
                self.hashArray[hashIdx].value = vehicle
                found = True
            
            # Move to next slot with double hashing
            else:
                hashIdx = (hashIdx + stepSize) % len(self.hashArray)
                # Table is full
                if hashIdx == origIdx:
                    giveUp = True

        # Resize table if the table is full
        if not found:
            self._resize(len(self.hashArray) * 2)
            self.insert(vehicle)

    def _findKey(self, vehicleID):
        # Get hash value for the input key
        hashIdx = self._hash(vehicleID)
        origIdx = hashIdx # Store in case hash table is full
        stepSize = self._stepHash(vehicleID) # Calculate stepsize - double hashing

        found = False
        giveUp = False

        # Probe for key location
        while not found and not giveUp:
            # Get entry at hash index
            entry = self.hashArray[hashIdx]

            if entry.state == 0: # Stop if at a never used entry
                giveUp = True

            elif entry.key == vehicleID and entry.state == 1: # Key is found
                found = True

            else: # Probe to next slot using double hashing
                hashIdx = (hashIdx + stepSize) % len(self.hashArray)
                if hashIdx == origIdx: # Stop if checked all nodes
                    giveUp = True

        if not found:
            hashIdx = -1 
        
        return hashIdx

    def search(self, vehicleID):
        idx = self._findKey(vehicleID) # Find the index of key
        if idx == -1:
            raise KeyNotFoundError("Key not found in hash table")
        else:
            return self.hashArray[idx].value # Return value of key input

    def delete(self, vehicleID):
        idx = self._findKey(vehicleID) # Find index of key
        if idx == -1:
            raise KeyNotFoundError("Key not found in hash table")
        else:
            self.hashArray[idx].state = -1 # Set state as previously used
            self.count -= 1 

            # Resize after removal when needed, confirm table size more than 5
            loadFactor = self.getLoadFactor()
            
            if loadFactor < self.lowerThreshold and len(self.hashArray) > 5:
                newSize = max(len(self.hashArray) // 2, 5)
                self._resize(newSize)

    def hasKey(self, inKey):
        return self._findKey(inKey) != -1 # Return true if key exists

    def export(self):
        linkedList = DSALinkedList()
        for i in range(len(self.hashArray)):
            entry = self.hashArray[i]
            if entry.state == 1:
                linkedList.insertLast(f"{entry.key},{entry.value}\n")
        
        return linkedList

    def _resize(self, newSize):
        # Recalculate new prime after doubling/halving
        newSize = self._nextPrime(newSize)

        # Create new array
        oldHashArr = self.hashArray
        self.hashArray = np.empty(newSize, dtype = object)
        for i in range(newSize):
            self.hashArray[i] = DSAHashEntry()

        # Reinsert the entries
        self.count = 0
        for entry in oldHashArr:
            if entry.state == 1:
                self.insert(entry.value)

    def printVehicles(self):
        for i in range(len(self.hashArray)):
            entry = self.hashArray[i]
            
            if entry.state == 1:
                print(entry.value, end="")

    def getVehicleList(self):
        vehicleList = DSALinkedList()
        arrLen = len(self.hashArray)
        ii = 0
        while ii < arrLen:
            entry = self.hashArray[ii]
            if entry.state == 1:
                vehicleList.insertLast(entry.value)
            ii += 1
        return vehicleList
