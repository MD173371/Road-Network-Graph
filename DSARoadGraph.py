#FILE: RoadGraph
#AUTHOR: Michael Durkan
#PURPOSE: Class files for Graph representation for raod network

from DSALinkedList import DSALinkedList, ListEmptyError
from DSAsorts import selectionSort
from DSAQueue import DSAQueue, QueueUnderflowError
from DSAStack import DSAStack, StackUnderflowError

import numpy as np

class Error(Exception):
    pass

class VertexNotFoundError(Exception):
    def __init__(self, message):
        self.message = message

class DuplicateVertexError(Exception):
    def __init__(self, message):
        self.message = message

class DuplicateEdgeError(Exception):
    def __init__(self, message):
        self.message = message

class _DSAGraphVertex:

    # CONSTRUCTOR
    def __init__(self, inLabel):
        self._label = inLabel
        self._visited = False
    
    # To String
    def __str__(self):
        return ("Label: " + str(self._label) +
                ", Vertex Visited State: " + str(self._visited))
    
class _DSAGraphEdge:

    # CONSTRUCTOR
    def __init__(self, inVertex1, inVertex2, roadName, distance):
        self._vertex1 = inVertex1
        self._vertex2 = inVertex2
        # Weight used for storing distances between locations
        self._distance = distance
        self._roadName = roadName
        self._visited = False

    # To String
    def __str__(self):
        return ("Location 1: " + str(self._vertex1) + "\nLocation 2: " + 
                str(self._vertex2) + "\nEdge Visited State: " 
                + str(self._visited) + "\n" + "Road Name: " + 
                str(self._roadName) + "\n" + "Road Distance: " + str(self._distance))

class DSAGraph:

    # CONSTRUCTOR
    def __init__(self):
        self.vertices = DSALinkedList()
        self.edges = DSALinkedList()

    # MUTATOR: addVertex
    def addVertex(self, inLabel):
        # Create vertex only if one with same label doesnt exist already
        if not self.hasVertex(inLabel):
            # Create graph vertex with input label and value
            vertex = _DSAGraphVertex(inLabel)
            # Insert that vertex onto the end of the linkedlist
            self.vertices.insertLast(vertex)
        
        else:
            raise DuplicateVertexError("Vertex " + inLabel + " exists already")

    # MUTATOR: addEdge
    def addEdge(self, inVertex1, inVertex2, roadName, distance):
        # Get the vertexes input for edge to be between
        vertex1 = self.getVertex(inVertex1)
        vertex2 = self.getVertex(inVertex2)
        
        if not isinstance(distance, int):
            raise TypeError("Length of road must be an integer")

        # Raise error if either or both vertex dont exist
        if vertex1 is None:
            if vertex2 is None:
                raise VertexNotFoundError("Vertex: " + inVertex1 + 
                        " and " + inVertex2 + " don't exist")
            else:
                raise VertexNotFoundError("Vertex: " + inVertex1 + 
                        " doesn't exist")
        
        if vertex2 is None:
            raise VertexNotFoundError("Vertex: " + inVertex2 + 
                    " doesn't exist")
        
        if vertex1 == vertex2:
            raise VertexNotFoundError("Input locations match, road to nowhere")

        # Only create edge if Vertices aren't adjacent (edge exists already)
        # otherwise raise error
        if not self.isAdjacent(inVertex1, inVertex2):
            # Create edge object between input vertices and place on end
            # of edge list
            edge = _DSAGraphEdge(vertex1, vertex2, roadName, distance)
            self.edges.insertLast(edge)
            
            # add the reverse edge
            edgeRev = _DSAGraphEdge(vertex2, vertex1, roadName, distance)
            self.edges.insertLast(edgeRev)
        
        else:
            raise DuplicateEdgeError("Edge between vertices " + inVertex1 + 
                    " and " + inVertex2 + " exists already")
    
    # ACCESSOR: hasVertex
    def hasVertex(self, label):
        # Set current to vertice list head
        cur = self.vertices.head
        found = False

        # Iterate through vertice list and set found to true if label is found
        while cur is not None and found is False:
            vertex = cur.data
            
            if vertex._label == label:
                found = True
            
            cur = cur.next
        
        return found

    # ACCESSOR getVertexCount
    # PURPOSE: Return size of vertice list
    def getVertexCount(self):
        return self.vertices.size

    def getEdge(self, label1, label2):
        vertex1 = self.getVertex(label1)
        vertex2 = self.getVertex(label2)

        if vertex1 is None or vertex2 is None:
            raise VertexNotFoundError("Vertices doesnt exist")

        cur = self.edges.head
        found = None
        while cur is not None and found is None:
            edge = cur.data
            if (edge._vertex1 == vertex1 and edge._vertex2 == vertex2) or (edge._vertex1 == vertex2 and edge._vertex2 == vertex1):
                found = edge
            cur = cur.next

        return found

    # ACCESSOR getEdgeCount
    # PURPOSE: Return edge list size divided by 2 
    # ( as edges are added twice due to reverse edges )
    def getEdgeCount(self):
        return self.edges.size // 2

    # ACCESSOR: getVertex
    # PURPOSE: get the vertex object of a certain label
    def getVertex(self, label):
        # Set current to vertice list head
        cur = self.vertices.head 
        found = None

        # Iterate through vertices to find vertex with label input
        while cur is not None and found is None:
            vertex = cur.data

            if vertex._label == label:
                found = vertex
            
            cur = cur.next
        
        return found
    
    # ACCCESSOR: getAdjacent
    # PURPOSE: Return a sorted lsit of adjacent vertex to a certain vertex label
    def getAdjacent(self, label):
        # Get vertex of input label
        vertex = self.getVertex(label)
        
        # Raise error if vertex doesnt exist
        if vertex is None:
            raise VertexNotFoundError("Vertex " + label + " does not exist")

        # Create list for adjacent vertexes
        adjacentList = DSALinkedList()
        
        # Iterate through Edges to find those adjacent to label
        cur = self.edges.head
        
        while cur is not None:
            edge = cur.data
            
            # If edges first vertex is input vertex, add second vertex to list
            if edge._vertex1 == vertex:
                adjacentList.insertLast(edge._vertex2)
            
            cur = cur.next
        
        # Create array for adjacent arrays to be sorted in, size of the amount
        # adjacent
        numAdjacent = adjacentList.size
        labelArray = np.zeros(numAdjacent, dtype = object)
        
        # Place labels into the array
        cur = adjacentList.head
        for i in range(numAdjacent):        
            labelArray[i] = cur.data._label
            cur = cur.next

        # Sort the Labels with selection Sort and place in linked list
        sortedLabels = selectionSort(labelArray)
        sortedAdjacentList = DSALinkedList()

        # Place sorted labels into a new linked list
        for i in range(numAdjacent):
            adjVertex = self.getVertex(sortedLabels[i])
            sortedAdjacentList.insertLast(adjVertex)

        return sortedAdjacentList

    # ACCESSOR: isAdjacent
    # PURPOSE: Determine if two input labels of vertices are adjacent
    def isAdjacent(self, label1, label2):
        # Get the vertex ojects of two input labels
        vertex1 = self.getVertex(label1)
        vertex2 = self.getVertex(label2)
        result = False

        # Return error if either vertices don't exist
        if vertex1 is None:
            if vertex2 is None:
                raise VertexNotFoundError("Vertices: " + label1 + " and "
                        + label2 + " do not exist.")
            else:
                raise VertexNotFoundError("Vertex: " + label1 + " doesn't exist.")
            
        if vertex2 is None:
            raise VertexNotFoundError("Vertex: " + label2 + " doesn't exist.")


        # Iterate through edges and return true when vertices it is between 
        # are equal to given labels
        else: 
            cur = self.edges.head
            
            while cur is not None:
                edge = cur.data
                
                if edge._vertex1 == vertex1 and edge._vertex2 == vertex2:
                    result = True
                
                cur = cur.next
        
        return result

    # ACCESSOR: displayAsList
    # PURPOSE: display graph as an adjacency list
    def displayAsList(self):
        print("\nList of Locations and there neighboring places:\n")

        # Get number of vertices and create an array for labels of vertex
        numVertex = self.getVertexCount()
        labelArray = np.zeros(numVertex, dtype = object)

        # Place all vertex labels into the array
        cur = self.vertices.head
        
        for i in range(numVertex):
            labelArray[i] = cur.data._label
            cur = cur.next 
        
        # Sort the label array
        sortedLabels = selectionSort(labelArray)

        # Print the Adjaceny List
        for i in range(numVertex):
            # Print vertice listing for each line
            print("Location " + str(i + 1) + "\n" + sortedLabels[i] + ":")
            
            # Get a list of adjacent Vertices to label printing on this line
            adjacent = self.getAdjacent(sortedLabels[i])
           
            # Iterate through each label of adjacent vertices in list and print
            hasAdjacent = False
            curAdj = adjacent.head
            while curAdj is not None:
                road = self.getEdge(sortedLabels[i], curAdj.data._label)
                hasAdjacent = True
                print("  Adjacent City: " + str(curAdj.data._label) + 
                        "\n    Connecting Road: " + 
                            str(road._roadName) + "\n    Distance: " + 
                            str(road._distance) + "\n")
                curAdj = curAdj.next

            if not hasAdjacent:
                print("No adjacent Towns")

            print()

    # MUTATOR: clearVisited
    # PURPOSE: clear all vertices in list to univisted status
    def clearVisited(self):
        cur = self.vertices.head
        while cur is not None:
            vertex = cur.data
            vertex._visited = False
            cur = cur.next

    # ACCESSOR: getLowestLabel
    # PURPOSE: get the label of the lowest alphebetical vertex in list
    def getLowestLabel(self):
        # Raise error if no vertices in graph
        if self.vertices.head is None:
            lowest = None
        
        else:
            # Set first vertex to lowest
            cur = self.vertices.head
            lowest = cur.data
            cur = cur.next
            
            # Iterate through vertices list to find lowest alphabetically
            while cur is not None:
                vertex = cur.data

                if vertex._label < lowest._label:
                    lowest = vertex

                cur = cur.next

        return lowest

    # ACCESSOR: breadthFirstSearch
    # PURPOSE: Search through all entries of graph BFS
    def breadthFirstSearch(self):
        T = DSAQueue()
        Q = DSAQueue()

        # Clear the visited values
        self.clearVisited()

        # Reference the starting vertex
        v = self.getLowestLabel()
        if v is None:
            raise VertexNotFoundError("No vertices in list to search")
        v._visited = True
        
        Q.enqueue(v)

        while not Q.isEmpty():
            v = Q.dequeue()
            adjacent = self.getAdjacent(v._label)
            curAdj = adjacent.head
            
            while curAdj is not None:
                w = curAdj.data
                
                # Enqueue v and w and set visited for adjacent that are unvisited
                if not w._visited:
                    T.enqueue(v)
                    T.enqueue(w)
                    w._visited = True
                    Q.enqueue(w)
                
                curAdj = curAdj.next
        
        # Print the traversal
        print("Breadth-First Traversal: ")
        while not T.isEmpty():
            v = T.dequeue()
            w = T.dequeue()
            print("(" + v._label + ", " + w._label + ")")
    
    # ACCESSOR: depthFirstSearch
    # PURPOSE: Search through all entries of graph DFS
    def depthFirstSearch(self):
        T = DSAQueue()
        S = DSAStack()

        # Clear the visited values of vertices
        self.clearVisited()

        # Reference starting vertex from vertice list
        v = self.getLowestLabel()
        if v is None:
            raise VertexNotFoundError("Graph has no vertices to search")
        v._visited = True
        
        S.push(v)

        while not S.isEmpty():
            v = S.pop()
            w = self.getUnvisitedAdjacent(v)
            if w is not None:
                T.enqueue(v)
                T.enqueue(w)
                w._visited = True
                S.push(v)
                S.push(w)

        # Print Traversal
        print("Depth-First Search Traversal: ")
        while not T.isEmpty():
            v = T.dequeue()
            w = T.dequeue()
            print("(" + v._label + ", " + w._label + ")")

    def is_path(self, source, destination):
        S = DSAStack()
        
        pathFound = False

        sourceVertex = self.getVertex(source)
        destVertex = self.getVertex(destination)
        
        if sourceVertex is None and destVertex is None:
            raise VertexNotFoundError(source + "does not exist" +
                    "and " + destination + "does not exist")
        elif sourceVertex is None:
            raise VertexNotFoundError(source + "does not exist")
        elif destVertex is None:
            raise VertexNotFoundError(destination + "does not exist")
        

        # Clear the visited values of vertices
        cur = self.vertices.head
        while cur is not None:
            vertex = cur.data
            vertex._visited = False
            cur = cur.next

        # Reference starting vertex from vertice list
        sourceVertex._visited = True
        
        S.push(sourceVertex)

        while not S.isEmpty():
            v = S.pop()

            if v._label == destination:
                pathFound = True

            w = self.getUnvisitedAdjacent(v)
            if w is not None:
                w._visited = True
                S.push(v)
                S.push(w)

        return pathFound

    def getUnvisitedAdjacent(self, vertex):
        # Get list of adjacent vertex
        adjacent = self.getAdjacent(vertex._label)
       
        # Iterate through adjacent and find next unvisited
        curAdj = adjacent.head
        unvisitedVertex = None
        while curAdj is not None:
            w = curAdj.data
            if not w._visited and unvisitedVertex is None:
                unvisitedVertex = w
            curAdj = curAdj.next

        return unvisitedVertex
                
    def deleteVertex(self, label):
        vertex = self.getVertex(label)
        vertexDeleted = False

        if vertex is None:
            raise VertexNotFoundError("Location: " + label + " does not exist")

        # Iterate through Edges and delete those connected to the vertex
        curEdge = self.edges.head
        
        while curEdge is not None:
            nextEdge = curEdge.next
            edge = curEdge.data
            
            # If current edge is connected to vertex
            if edge._vertex1 == vertex or edge._vertex2 == vertex:
                
                # If edge to delete is first edge in list update head to next
                if curEdge.prev is None:
                    self.edges.head = curEdge.next
                
                    # If list is not empty set heads previous to none
                    if self.edges.head:
                        self.edges.head.prev = None
                    # If list is empty update tail to be none
                    else:
                        self.edges.tail = None
                
                # If edge to delete is at middle or end of list
                else:
                    # Update previous edge to skip over cur edge
                    curEdge.prev.next = curEdge.next

                    # If deleting a middle node update next nodes previous
                    if curEdge.next:
                        curEdge.next.prev = curEdge.prev
                    # If deleting the tail node update the tail pointer
                    else:
                        self.edges.tail = curEdge.prev

                # Reduce edge list size upon deletion
                self.edges.size -= 1
                
            curEdge = nextEdge

        # Iterate through Vertex Linked List to delete Vertex
        curVertex = self.vertices.head

        while curVertex is not None:
            nextVertex = curVertex.next
            # See if current Vertex is vertex to delete
            if curVertex.data == vertex and not vertexDeleted:
                
                # If vertex is the head of list update head
                if curVertex.prev is None:
                    self.vertices.head = curVertex.next
                    # If vertex list is not now empty update prev
                    if self.vertices.head:
                        self.vertices.head.prev = None
                    # If it is empty also update tail to none
                    else:
                        self.vertices.tail = None
                # If vertex is middle or end of list update previous nodes next pointer
                else:
                    # update previous nodes next to skip over deleted
                    curVertex.prev.next = curVertex.next
                    
                    # If deleting a middle node update previous of next
                    if curVertex.next:
                        curVertex.next.prev = curVertex.prev
                    # If deleting the tail set tail to point to vertex
                    else:
                        self.vertices.tail = curVertex.prev

                # Reduce vertex list size
                self.vertices.size -= 1
                vertexDeleted = True
                
                # Progress to next Vertice
            curVertex = nextVertex

    #ACCESSOR: deleteEdge
    #PURPOSE: delete the edge between input labels
    def deleteEdge(self, label1, label2):
        # Get the two vertex objects of input labels
        vertex1 = self.getVertex(label1)
        vertex2 = self.getVertex(label2)
        edgeDeleted = False
            
        # Raise error if either input vertex doesnt exist
        if vertex1 is None:
            if vertex2 is None:
                raise VertexNotFoundError("Vertex " + label1 + " and " + 
                        label2 + " do not exist")

            raise VertexNotFoundError("Vertex " + label1+ " does not exist")
        
        if vertex2 is None:
            raise VertexNotFoundError("Vertex " + label2 + " does not exist")


        # Iterate through edges of the graph
        curEdge = self.edges.head
        
        while curEdge is not None:
            nextEdge = curEdge.next
            edge = curEdge.data
            

            # Check if cur is between label1 and label2
            if (edge._vertex1 == vertex1 and edge._vertex2 == vertex2) or (edge._vertex1 
                    == vertex2 and edge._vertex2 == vertex1):
                # If edge is first in the list update head to point to next
                if curEdge.prev is None:
                    self.edges.head = curEdge.next
                    
                    # If list isnt empty update new heads prev to none
                    if self.edges.head:
                        self.edges.head.prev = None

                    # If list is empty update the tail to none
                    else:
                        self.edges.tail = None

                # If edge is in the middle or end of list set previous edge
                # to to cur edge next
                else:
                    curEdge.prev.next = curEdge.next
                    
                    # If not the tail update prev to skip over edge to delete
                    if curEdge.next:
                        curEdge.next.prev = curEdge.prev
                    # if deleting tail update tail to be previous node
                    else:
                        self.edges.tail = curEdge.prev

                # Reduce edge list size
                self.edges.size -= 1
                edgeDeleted = True
           
            curEdge = nextEdge

        if edgeDeleted:
            print("Road Deleted\n")
        else:
            print("Road does not exist\n")
