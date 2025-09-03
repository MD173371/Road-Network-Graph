# File: DSAStack.py
# Author: Michael Durkan
# PURPOSE: DSA Stack implementation using a DSA linkedlist as storage

from DSALinkedList import DSALinkedList, ListEmptyError

class Error(Exception):
    pass

# Exception raised if stack is already empty
class StackUnderflowError(Error):
    def __init__(self, message):
        self.message = message

class DSAStack:
    
    # Default Constructor 
    def __init__(self):
        self.linkedList = DSALinkedList()

    # ACCESSOR: isEmpty
    # PURPOSE: Return true or false depending on if stack count is zero or not
    def isEmpty(self):
        return self.linkedList.isEmpty()

    # MUTATOR: push
    # PURPOSE: Place some data on the top of the stack 
    def push(self, data):
        self.linkedList.insertFirst(data)

    # MUTATOR: pop
    # PURPOSE: Remove data from the top of the stack
    def pop(self):
        # Raise error if the stack is empty
        if self.isEmpty():
            raise StackUnderflowError("Stack is already empty")
        
        return self.linkedList.removeFirst()        

    # MUTATOR: top
    def top(self):
        # Raise error if stack is empty
        if self.isEmpty():
            raise StackUnderflowError("Stack is empty")

        return self.linkedList.peekFirst()
