# DSAHeap.py
# Michael Durkan

import numpy as np

class Error(Exception):
    pass

class HeapEmptyError(Exception):
    def __init__(self, message):
        self.message = message

class DSAHeapEntry:
    def __init__(self, inPriority, inValue):
        self._priority = inPriority
        self._value = inValue

    def getPriority(self):
        return self._priority

    def setPriority(self, inPriority):
        self._priority = inPriority

    def getValue(self):
        return self._value

    def setValue(self, inValue):
        self._value = inValue

class DSAHeap:
    def __init__(self, inSize = 200):
        self.count = 0
        self.heapArr = np.empty(inSize, dtype = object)
        self.size = inSize
    
    def add(self, inPriority, inValue):
        # Resize when heap full
        if self.count >= self.size:
            self._resizeHeap()
       
        self.count += 1

        # Create heap entry and enter at bottom of heap
        entry = DSAHeapEntry(inPriority, inValue)
        self.heapArr[self.count - 1] = entry
        
        # Move new entry to correct position through trickle up function
        self._trickleUp(self.count - 1)
        
    
    def _trickleUp(self, inIdx):
        parentIdx = (inIdx - 1) // 2

        # While cur not root and cur priority > parent priority
        while inIdx > 0 and self.heapArr[inIdx].getPriority() > self.heapArr[parentIdx].getPriority():
            temp = self.heapArr[parentIdx]
            self.heapArr[parentIdx] = self.heapArr[inIdx]
            self.heapArr[inIdx] = temp
            inIdx = parentIdx
            parentIdx = (inIdx - 1) // 2

    def remove(self):
        if self.count == 0:
            raise HeapEmptyError("Heap has no entries")

        # Reduce count and store the root
        self.count -= 1
        root = self.heapArr[0]

        if self.count > 0:
            # Set the root to the last node and clear last node
            self.heapArr[0] = self.heapArr[self.count]
            self.heapArr[self.count] = None
            
            # Trickle Down the moved node
            self._trickleDown(0, self.count)
        else:
            self.heapArr[0] = None

        return root

    def _trickleDown(self, inIdx, heapSize):
        lChildIdx = inIdx * 2 + 1
        rChildIdx = lChildIdx + 1
        keepGoing = True

        while keepGoing and lChildIdx < heapSize:
            keepGoing = False
            largeIdx = lChildIdx
            
            if rChildIdx < heapSize:
                if self.heapArr[lChildIdx].getPriority() < self.heapArr[rChildIdx].getPriority():
                    largeIdx = rChildIdx

            if self.heapArr[largeIdx].getPriority() > self.heapArr[inIdx].getPriority():    
                temp = self.heapArr[largeIdx]
                self.heapArr[largeIdx] = self.heapArr[inIdx]
                self.heapArr[inIdx] = temp
                keepGoing = True
            
            inIdx = largeIdx
            lChildIdx = (inIdx * 2) + 1
            rChildIdx = lChildIdx + 1

    def _resizeHeap(self):
        newSize = self.size * 2
        newHeap = np.empty(newSize, dtype = object)
        for i in range(self.count):
            newHeap[i] = self.heapArr[i]
        self.heapArr = newHeap
        self.size = newSize

    def display(self):
        for i in range(self.count):
            entry = self.heapArr[i]
            print(f"Priority: {entry.getPriority()}, Value: {entry.getValue()}\n")

    def heapify(self, inSize):
        for ii in range((inSize // 2) - 1, -1, -1):
            self._trickleDown(ii, inSize)

    def heapSort(self):
        size = self.count

        self.heapify(size)

        for ii in range(size - 1, 0, - 1):
            temp = self.heapArr[0]
            self.heapArr[0] = self.heapArr[ii]
            self.heapArr[ii] = temp

            self._trickleDown(0, ii)

    def loadEntries(self, inEntries):
        size = np.size(inEntries)

        if size > self.size:
            self.size = size
            self.heapArr = np.empty(self.size, dtype = object)

        self.count = size

        for i in range(size):
            self.heapArr[i] = inEntries[i]

if __name__ == "__main__":
    heap = DSAHeap()
    heap.add(5, "A")
    heap.add(3, "B")
    heap.add(7, "C")
    heap.add(2, "D")
    heap.add(10, "E")
    heap.add(20, "F")
    heap.add(9, "G")
    
    print("Print heap test")
    heap.display()

    print("Heap after remove test")
    removed = heap.remove()
    heap.display()
