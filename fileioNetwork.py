# Name: Michael Durkan
# File Io code for the graph and vehicle table 

from DSARoadGraph import DSAGraph, VertexNotFoundError, DuplicateVertexError
from DSALinkedList import ListEmptyError
from VehicleHashTable import VehicleHashTable, KeyNotFoundError
from Vehicle import Vehicle, IncorrectParameterError
import numpy as np

def readLocationCSV(filename, network):
    
    try:
        with open(filename, "r") as f:
            lines = f.readlines()

        for line in lines:
            var = line.strip().split(",")
            location= var[0]
            network.addVertex(location)
        
        print("\nLocations from CSV Added Succesfully.")

    except FileNotFoundError as err:
        print("Csv does not exist ",err)

def readRoadsCSV(filename, network):
    
    try:
        with open(filename, "r") as f:
            lines = f.readlines()

        for line in lines:
            var = line.strip().split(",")
            start = var[0]
            dest = var[1]
            roadName = var[2]
            try:
                distance = int(var[3])
            except ValueError:
                print(roadName, " - Road not added due to lack of integer value")
            try:
                network.addEdge(start, dest, roadName, distance)
            except VertexNotFoundError:
                print(roadName, " - Road not added due locations not existing")
        if network.getEdgeCount() == len(lines):
            print("\nRoads from CSV Added Succesfully.")
        else:
            print("All roads without errors added")

    except FileNotFoundError as err:
        print("Csv does not exist ",err)

def readVehiclesCSV(filename, network, vTable):
    
    try:
        with open(filename, "r") as f:
            lines = f.readlines()

        for line in lines:
            var = line.strip().split(",")
            vehicleID = var[0]
            location = var[1]
            dest = var[2]
            distDest = int(var[3])
            battery = int(var[4])
            if battery > 100 or battery < 0:
                raise TypeError("battery percentage must be below 0-100")
            inVehicle = Vehicle(vehicleID, "", "", distDest, battery, network)
            try:
                inVehicle.setDestination(dest)
                inVehicle.setLocation(location)
            except VertexNotFoundError:
                print(vehicleID,": vehicle not added, locations do not exist")

            vTable.insert(inVehicle)        
        print("\nVehicles from CSV Added Succesfully.")

    except FileNotFoundError as err:
        print("Csv does not exist ",err)
