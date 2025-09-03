#Name: Michael Durkan
# Vehicle class implementation

import numpy as np
from DSALinkedList import DSALinkedList, ListEmptyError
from DSARoadGraph import DSAGraph, VertexNotFoundError, DuplicateVertexError, DuplicateEdgeError
from DSAHeap import DSAHeap, DSAHeapEntry

class Error(Exception):
    pass

class IncorrectParameterError(Exception):
    def __init__(self, message):
        self.message = message

class Vehicle:
    def __init__(self, vehicleID, location, dest, distDest, battery, network):
        self._vehicleID = vehicleID
        self._location = location
        self._dest = dest
        self._distDest = distDest
        self._battery = battery
        self._network = network
        
    def __str__(self):
        return f"VehicleID: {self._vehicleID}, location: {self._location}, Destination: {self._dest}, Distance To Destination: {self._distDest}, Battery: {self._battery}%\n\n"
    
    def setLocation(self, location):
        if self._network.hasVertex(location):
            self._location = location
        else:
            raise VertexNotFoundError("Vertex for set location does not exist")

    def setDestination(self, destination):
        if self._network.hasVertex(destination):
            self._dest = destination
        else:
            raise VertexNotFoundError("Vertex for set location does not exist")

    def setDistanceToDestination(self, distance):
        if isinstance(distance, int):
            self._distDest = distance
        else:
            raise IncorrectParameterError("Distance to destination must be integer")

    def setBatteryLevel(self, level):
        if int(level) <= 100 or int(level) >= 0:
            self._battery = level
        else:
            raise IncorrectParameterError("Battery percentage must be less than 100.")

    def getLocation(self):
        return self._location

    def getDestination(self):
        return self._dest

    def getDistanceToDestination(self):
        return self._distDest

    def getBatteryLevel(self):
        return self._battery
