# File: DSAQueue.py
# Author: Michael Durkan
# PURPOSE: Queue implementation w DSA Linkedlist storage

from DSALinkedList import DSALinkedList, ListEmptyError

class Error(Exception):
    pass

# Exception raised if queue is already empty
class QueueUnderflowError(Error):
    def __init__(self, message):
        self.message = message

class DSAQueue:
    
    # Default Constructor
    def __init__(self):
        self.linkedList = DSALinkedList()

    # ACCESSOR: isEmpty
    # PURPOSE: Return true or false depending on if queue is empty or not
    def isEmpty(self):
        return self.linkedList.isEmpty()

    # MUTATOR: enqueue
    def enqueue(self, data):
        self.linkedList.insertLast(data)

    # MUTATOR: dequeue
    def dequeue(self):
        if self.isEmpty():
            raise QueueUnderflowError("Queue is empty")
        return self.linkedList.removeFirst()

    # MUTATOR: peek
    def peek(self):
        if self.isEmpty():
            raise QueueUnderflowError("Queue is empty")
        return self.linkedList.peekFirst()
