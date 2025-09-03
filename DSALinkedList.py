# FILE: DSALinkedList
# AUTHOR: Michael Durkan
# PURPOSE: Class files for a doubly linked, double ended linked list

class Error(Exception):
    pass

# NAME: ListEmptyError
# PURPOSE: Provide error message when List is empty
class ListEmptyError(Exception):
    def __init__(self, message):
        self.message = message

# NAME: _DSAListNode
# PURPOSE: Provide node functionality for the linked list
class _DSAListNode:
    
    # CONSTRUCTOR
    def __init__(self, inData):
        self.data = inData
        self.prev = None
        self.next = None

    # ACCESSOR: getData
    def getData(self):
        return self.data

    # ACCESSOR: getNext
    def getNext(self):
        return self.next

    # ACCESSOR: getPrev
    def getPrev(self):
        return self.prev

    # MUTATOR: setValue
    def setValue(self, data):
        self.data = data

    # MUTATOR: setNext
    def setNext(self, newNext):
        self.next = newNext

    # MUTATOR: setPrev
    def setPrev(self, newPrev):
        self.prev = newPrev

class DSALinkedList:

    # Constructor
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # ACCESSOR: isEmpty
    def isEmpty(self):
        return self.head is None
    
    # ACCESSOR: peekFirst
    def peekFirst(self):
        nodeData = None

        # If not an empty list return the head data, otherwise return None
        if not self.isEmpty():
            nodeData = self.head.getData()
    
        return nodeData

    # ACCESSOR: peekLast
    def peekLast(self):
        nodeData = None

        # If not an empty list return the tail data, otherwise return None
        if not self.isEmpty():
            nodeData = self.tail.getData()
            
        return nodeData

    # MUTATOR: insertFirst
    def insertFirst(self, newData):
        newNd = _DSAListNode(newData)
        # If list is empty head and tail are both the new data
        if self.isEmpty():
            self.head = newNd
            self.tail = newNd
        else:
            # New nodes next is set to old head
            newNd.setNext(self.head)
            # Old heads previous is set to new node
            self.head.setPrev(newNd)
            # New node is set to head
            self.head = newNd
        
        self.size += 1

    # MUTATOR: insertLast
    def insertLast(self, newData):
        newNd = _DSAListNode(newData)
        # if list is empty head and tail are both new data
        if self.isEmpty():
            self.head = newNd
            self.tail = newNd
        else:
            # Old tails next is set to new node
            self.tail.setNext(newNd)
            # New nodes prev is set to old tail
            newNd.setPrev(self.tail)
            # tail is set to new node
            self.tail = newNd
        
        self.size += 1

    # MUTATOR: removeFirst
    def removeFirst(self):
        # Raise error if already empty
        if self.isEmpty():
            raise ListEmptyError("Cannot remove first node as list is empty")
        else:
            # Store head data in nodeData variable
            nodeData = self.head.getData()
            # Set head to old heads next
            self.head = self.head.getNext()
            if self.head is not None:
                # If head isnt now empty set its previous to None
                self.head.setPrev(None)
            else:
                # If head is now empty set tail to None as list is empty
                self.tail = None
            
            self.size -= 1
        return nodeData

    # MUTATOR: removeLast
    def removeLast(self):
        # Raise error if already empty
        if self.isEmpty():
            raise ListEmptyError("Cannot remove node as list is empty")
        elif self.head.getNext() is None:
            # Store head data in nodeData if list has 1 element
            # Set head and tail to none
            nodeData = self.head.getData()
            self.head = None
            self.tail = None
        else:
            # Store tail in nodeData if list has more than 1 element
            nodeData = self.tail.getData()
            # Set new tail to old tails previous and its next to none
            self.tail = self.tail.getPrev()
            self.tail.setNext(None)
        
        self.size -= 1

        return nodeData

    def printList(self):
        print("List Contents: ")
        currNd = self.head
        if self.isEmpty():
            print("List is empty")
        else:
            while currNd:
                print(str(currNd.data) + " ", end='')
                currNd = currNd.next
            print()

