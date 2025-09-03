#Name: Michael Durkan
# Test code for vehicles

from DSALinkedList import DSALinkedList, ListEmptyError
from DSAsorts import selectionSort
from DSAQueue import DSAQueue, QueueUnderflowError
from DSAStack import DSAStack, StackUnderflowError
from DSARoadGraph import DSAGraph, _DSAGraphEdge, _DSAGraphVertex, VertexNotFoundError, DuplicateVertexError, DuplicateEdgeError
from Vehicle import Vehicle
from VehicleHashTable import VehicleHashTable, KeyNotFoundError
from VehicleSort import find_nearest_vehicle, find_vehicle_with_highest_battery, heapSortDistanceAsc, quickSortBattery, heapSortDistanceTo

def main():
    # Testing Vertex Class
    v1 = _DSAGraphVertex("Rockingham")
    print("Testing vertex A creation: " + str(v1))
    print()

    v2 = _DSAGraphVertex("Perth")

    # Testing Edges Class
    e1 = _DSAGraphEdge(v1, v2, "Read St", 50)
    print("Testing 'Read St' Rockingham to Perth road creation\n" + str(e1))
    print()

    # Testing Graph Vertex
    g1 = DSAGraph()
    g1.addVertex("Mandurah")
    g1.addVertex("Fremantle")
    g1.addVertex("Serpentine")
    g1.addVertex("Rockingham")
    g1.addVertex("Perth")
    g1.addVertex("Midland")
    g1.addVertex("Subiaco")
    g1.addVertex("Z")
    print("Testing Graph Mandurah, Fremantle, Serpentine... creation: ", end= '')
    g1.vertices.printList()

    # Testing Get Vertex
    print("Testing find Mandurah: " + str(g1.getVertex("Mandurah")))
    print() 
    
    # Testing Graph Edges
    print("Testing Road add Mandurah, Fremantle: ")
    g1.addEdge("Mandurah","Fremantle","Stock Rd", 80)
    g1.addEdge("Fremantle","Perth", "Ocean Beach Rd", 40)
    g1.addEdge("Perth","Rockingham", "Southern Fwy", 100)
    g1.addEdge("Rockingham","Serpentine", "Mundijong Rd", 30)
    g1.addEdge("Perth","Midland","Northern Fwy", 30)
    g1.addEdge("Fremantle","Z","Narnia Rd",1000)

    # Testing Graph Display function
    print("Testing Graph Display function")
    g1.displayAsList()

    # Testing Retrieve Neighbours
    print("Testing Retrieve Neighbours")
    g1.getAdjacent("Perth").printList()

    #Testing is_path function
    print("Testing is_path function")
    print(g1.is_path("Mandurah","Fremantle"))
    print(g1.is_path("Fremantle","Mandurah"))
    print(g1.is_path("Subiaco","Fremantle"))
    print(g1.is_path("Fremantle","Subiaco"))
    print(g1.is_path("Mandurah","Perth"))
    print(g1.is_path("Z","Fremantle"))

    g1 = DSAGraph()
    g1.addVertex("Mandurah")
    g1.addVertex("Fremantle")
    g1.addVertex("Serpentine")
    g1.addVertex("Rockingham")
    g1.addVertex("Perth")
    g1.addVertex("Midland")
    g1.addVertex("Subiaco")
    g1.addEdge("Mandurah","Fremantle","Stock Rd", 80)
    g1.addEdge("Fremantle","Perth", "Ocean Beach Rd", 40)
    g1.addEdge("Perth","Rockingham", "Southern Fwy", 100)
    g1.addEdge("Rockingham","Serpentine", "Mundijong Rd", 30)
    g1.addEdge("Perth","Midland","Northern Fwy", 30)
    
    car1 = Vehicle("V001","Rockingham","Perth",120,99,g1)
    car2 = Vehicle("V002","Rockingham","Mandurah",60,44,g1)
    car3 = Vehicle("V003","Subiaco","Midland",20,54,g1)
    
    vTable = VehicleHashTable(5)
    vTable.insert(car1)
    vTable.insert(car2)
    vTable.insert(car3)
    vTable.printVehicles()
    print("\nSearch Test V001: " + str(vTable.search("V001")))
    vTable.delete("V003")
    try:
        print("\nSearch Test V003: " + str(vTable.search("V003")))
    except KeyNotFoundError as err:
        print(err)
        print("Test PASSED")

    vehicleList = vTable.getVehicleList()

    nearest = find_nearest_vehicle(vehicleList)
    print("nearest: " + str(nearest))
    vehicleList.printList()
    sortedList = heapSortDistanceTo(vehicleList)
    for vehicle in sortedList:
        print(vehicle)
    ascSortedList = heapSortDistanceAsc(vehicleList)
    for vehicle in ascSortedList:
        print(vehicle)

    batterySorted = quickSortBattery(vehicleList)
    print("battery sorted")
    for vehicle in batterySorted:
        print(vehicle)
    
    highestBattery = find_vehicle_with_highest_battery(vehicleList)
    print(highestBattery)


main()
