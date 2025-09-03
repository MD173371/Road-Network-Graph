#Name: Michael Durkan
# Heapsort and quicksort implementations

import numpy as np
from DSAHeap import DSAHeap, HeapEmptyError
from DSALinkedList import DSALinkedList, ListEmptyError


def quickSortVehicles(array, leftIdx, rightIdx):
    if rightIdx > leftIdx:
        pivotIdx = (leftIdx + rightIdx) // 2
        newPivotIdx = doPartitioning(array, leftIdx, rightIdx, pivotIdx)
        quickSortVehicles(array, leftIdx, newPivotIdx - 1)
        quickSortVehicles(array, newPivotIdx + 1, rightIdx)


def doPartitioning(array, leftIdx, rightIdx, pivIdx):
    pivotVal = array[pivIdx].getBatteryLevel()
    array[pivIdx], array[rightIdx] = array[rightIdx], array[pivIdx]

    currIdx = leftIdx

    for ii in range(leftIdx, rightIdx):
        if array[ii].getBatteryLevel() > pivotVal:
            array[ii], array[currIdx] = array[currIdx], array[ii]
            currIdx += 1
    newPivIdx = currIdx

    array[rightIdx], array[newPivIdx] = array[newPivIdx], array[rightIdx]
    return newPivIdx
    
def heapSortDistanceTo(vehicleList):
    heapLen = vehicleList.size
    heap = DSAHeap(heapLen)

    cur = vehicleList.head
    while cur is not None:
        vehicle = cur.data 
        distanceTo = vehicle.getDistanceToDestination()
        priority = distanceTo
        heap.add(priority, vehicle)
        cur = cur.next

    heap.heapSort()

    distanceToSorted = np.empty(heapLen, dtype = object)
    for ii in range(heapLen):
        distanceToSorted[ii] = heap.heapArr[ii].getValue()

    return distanceToSorted

def find_nearest_vehicle(vehicleList):
    distanceToSorted = heapSortDistanceTo(vehicleList)

    if len(distanceToSorted) == 0:
        nearest = None
    else:
        nearest = distanceToSorted[0]
    
    return nearest

def heapSortDistanceAsc(vehicleList):
    heapLen = vehicleList.size
    heap = DSAHeap(heapLen)

    cur = vehicleList.head
    while cur is not None:
        vehicle = cur.data 
        distanceTo = vehicle.getDistanceToDestination()
        priority = -distanceTo
        heap.add(priority, vehicle)
        cur = cur.next

    heap.heapSort()

    distanceToSorted = np.empty(heapLen, dtype = object)
    for ii in range(heapLen):
        distanceToSorted[ii] = heap.heapArr[ii].getValue()

    return distanceToSorted

def llToArr(linkedList):
    arrLen = linkedList.size
    vehicleArr = np.empty(arrLen, dtype = object)
    ii = 0
    cur = linkedList.head
    while cur is not None:
        vehicleArr[ii] = cur.data
        cur = cur.next
        ii += 1
    return vehicleArr

def quickSortBattery(vehicleList):
    vehicleArr = llToArr(vehicleList)
    if len(vehicleArr) > 0:
        quickSortVehicles(vehicleArr, 0, len(vehicleArr) - 1)
    
    return vehicleArr

def find_vehicle_with_highest_battery(vehicleList):
    batterySorted = quickSortBattery(vehicleList)
    highestBattery = None
    if len(batterySorted) > 0:
        highestBattery = batterySorted[0]
    return highestBattery
