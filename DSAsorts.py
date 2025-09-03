# Python file to hold all sorting methods
# Michael Durkan

import numpy as np

def bubbleSort(A):
    n = len(A)
    done = False

    while not done:                             #loop until no swaps are made during pass
        done = True                             
        for i in range(n-1):                    #Compare every consecutive value
            if A[i] > A[i + 1]:
                A[i], A[i + 1] = A[i + 1], A[i] #swap when first is greater
                done = False
        n -= 1                                  #reduce range by 1 to save time on further comparisons

    return A

def insertionSort(A):
    n = len(A)

    for i in range(1, n):                       # Start at element 1
        ii = i                                  # Begin at the last item insert index
        while (ii > 0) and (A[ii - 1] > A[ii]): # Insert into sub array to left of ii
            A[ii], A[ii - 1] = A[ii - 1], A[ii] # Loop through sub array and move value at ii up by one
            ii -= 1
    
    return A

def selectionSort(A):
    n = len(A)

    for i in range(n):                          
        minIdx = i                              #Lowest value increase by 1 each pass
        for j in range(i + 1, n):               #Find lowest value in all other values
            if A[j] < A[minIdx]:
                minIdx = j 
        
        A[i], A[minIdx] = A[minIdx], A[i]       #Swap values after lowest is found

    return A
