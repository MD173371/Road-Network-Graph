#Name: Michael Durkan
# Interactive Menu for automated vehicle system

from DSARoadGraph import DSAGraph, VertexNotFoundError, DuplicateVertexError, DuplicateEdgeError
from VehicleHashTable import VehicleHashTable, KeyNotFoundError
from DSALinkedList import DSALinkedList, ListEmptyError
from Vehicle import Vehicle, IncorrectParameterError
from fileioNetwork import readLocationCSV, readRoadsCSV, readVehiclesCSV
from VehicleSort import find_nearest_vehicle, find_vehicle_with_highest_battery, heapSortDistanceAsc, quickSortBattery

def main():
    network = DSAGraph()
    vTable = VehicleHashTable(5)
    close = False
    
    addLocationsCSV(network)
    addRoadsCSV(network)
    addVehiclesCSV(network, vTable)

    while not close:
        showMenu()
        option = input("\nEnter integer 1-9 per option: ")
        
        # Add Location
        if option == '1':
            label = input("Enter the name of new location: ")
            try:
                network.addVertex(label)
                print("Location: " + label + " added\n")
            except DuplicateVertexError as err:
                print(err)

        # Delete Location
        elif option == '2':
            label = input("Enter the name of location to delete: ")
            try:
                network.deleteVertex(label)
                print("Location: deleted")
            except VertexNotFoundError as err:
                print(err)

        # Add Road
        elif option == '3':
            label1 = input("Enter the name of starting location: ")
            label2 = input("Enter the name of the destination: : ")
            roadName = input("Enter the name of the road: ")
            inDistance = input("Enter the road length: ")

            try:
                distance = int(inDistance)
                network.addEdge(label1, label2, roadName, distance)
                print("Road added \n")
            except VertexNotFoundError as err:
                print(err)
            except DuplicateEdgeError as err:
                print(err)
            except TypeError as err:
                print(err)
            except ValueError:
                print("Road Length must be an integer")
        
        # Delete Road
        elif option == '4':
            label1 = input("Enter name of starting location: ")
            label2 = input("Enter name of destination: ")
            try:
                network.deleteEdge(label1, label2)
            except VertexNotFoundError as err:
                print(err) 
        
        # Display Network
        elif option == '5':
            network.displayAsList()            
        
        # Check Path Existence
        elif option == '6':
            location1 = input("Enter first location: ")
            location2 = input("Enter second location: ")
            try:
                isPath = network.is_path(location1, location2)
                print("\nPath Exists:",isPath)
            except VertexNotFoundError as err:
                print("Location does not exist",err)
       
        # Add Vehicle
        elif option == '7':
            vehicleID = input("enter vehicle identification: ")
            location = input("Enter vehicle location: ")
            dest = input("Enter vehicle destination: ")
            inDistDest = input("Enter vehicle distance to destination: ")
            inBattery = input("Enter battery percentage: ")
            inVehicle = Vehicle(vehicleID,"","","","" ,network)
            try:
                battery = int(inBattery)
                distDest = int(inDistDest)
                inVehicle.setLocation(location)
                inVehicle.setDestination(dest)
                inVehicle.setDistanceToDestination(distDest)
                inVehicle.setBatteryLevel(battery)
                vTable.insert(inVehicle)
                print("Vehicle Added")            
            except VertexNotFoundError as err:
                print("\nLocation does not exist:", err)
            except IncorrectParameterError as err:
                print("Not added: Incorrect parameter for vehicle details:", err)
            except ValueError:
                print("Not added: Distances and battery levels must be integer")
             
        # Delete Vehicle
        elif option == '8':
            vehicleID = input("Enter ID of vehicle to delete: ")
            
            try:
                vTable.delete(vehicleID)
                print("Vehicle deleted successfully")
            except KeyNotFoundError as err:
                print("\nVehicle Id doest not exist.",err)     

        # Print Vehicles
        elif option == '9':
            vTable.printVehicles()

        # Find Nearest Vehicle
        elif option == '10':
            print("Nearest Vehicle: ")
            vehicleList = vTable.getVehicleList()
            print(find_nearest_vehicle(vehicleList))

        # Find Highest Battery Vehicle
        elif option == '11':
            print("Highest Battery Vehicle")
            vehicleList = vTable.getVehicleList()
            print(find_vehicle_with_highest_battery(vehicleList))
        
        # Sorted by Distance To Destination Ascending
        elif option == '12':
            vehicleList = vTable.getVehicleList()
            sortedList = heapSortDistanceAsc(vehicleList)
            for vehicle in sortedList:
                print(vehicle)
        
        # Sort by battery descending
        elif option == '13':
            vehicleList = vTable.getVehicleList()
            sortedList = quickSortBattery(vehicleList)
            for vehicle in sortedList:
                print(vehicle)
        
        # Search for vehicle
        elif option == '14':
            searchFor = input("Enter Vehicle ID to find: ")
            print(vTable.search(searchFor))

        elif option == '0':
            close = True
        else:
            print("\nIncorrect menu option\n")

def addLocationsCSV(network):
    try:
        readLocationCSV("locations.csv", network)
    except DuplicateVertexError as err:
        print("Files already added.")
    except IndexError as err:
        print("Csv file is incorrectly formatted.",err)

def addRoadsCSV(network):
    try:    
        readRoadsCSV("roads.csv", network)
    except DuplicateVertexError as err:
        print("Files already added.")
    except VertexNotFoundError as err:
        print("Location for road vertices doesnt exist, incomplete adding of roads", err)
    except IndexError as err:
        print("Csv file contains incorrect number of columns", err)
    except DuplicateEdgeError as err:
        print("Files already added.")

def addVehiclesCSV(network, vTable):
    try:
        readVehiclesCSV("vehicles.csv", network, vTable)
    except TypeError as err:
        print(err, "Vehicles not added")
    except ValueError as err:
        print("Incorrect value for integer parameter",err)
        print("Adding Vehicles incomplete")
    except VertexNotFoundError as err:
        print("Incorrect value for destination or location", err)
        print("Adding Vehicles incomplete")
    except IndexError:
        print("Incorrect formatting of CSV File")
        print("Vehicles add incomplete")

def showMenu():
    print("\n 1) Add Location Manually")
    print(" 2) Delete Location")
    print(" 3) Add Road Manually")
    print(" 4) Delete Road")
    print(" 5) Display Road Network")
    print(" 6) Check Path Existence")
    print(" 7) Add Vehicle")
    print(" 8) Delete a Vehicle")
    print(" 9) Display all Vehicles")
    print("10) Find Nearest Vehicle")
    print("11) Find Highest Battery Vehicle")
    print("12) Display Vehicles by Distance to destination, ascending")
    print("13) Display Vehicles by Battery Level, descending")
    print("14) Search for a vehicle")
    print("0) Exit")

main()
