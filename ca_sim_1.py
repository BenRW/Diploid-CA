import numpy as np


cells = np.random.randint(0, 2, 10)

def ECA1(arr):
    """Applies null rule to cells"""

    # input doesn't matter, applies state 0 to any configuration
    arr = np.zeros(len(arr))

    return arr

def ECA22(arr):
    """Applying rule 22"""
    new_arr = np.zeros(len(arr))

    # local configurations associated with outcome: 1
    one_if = np.array([[0,0,1],[0,1,0],[1,0,0]])

    for i in range(len(arr)):
        # define neighbourhood
        if i>0 and i<len(arr)-2:
            nhood = arr[i-1:i+2]
        elif i<len(arr)-2:
            nhood = np.array([arr[-1], arr[i], arr[i+1]])
        else:
            nhood = arr[i:i+2-len(arr)]

        # check that exactly one cell in the neighbourhood = 1 (rule 22)
        if np.count_nonzero(nhood==1)==1:
            new_arr[i] = 1
        else:
            new_arr[i] = 0

    return new_arr

cells2 = ECA22(cells)

def get_neighbourhood(arr, i):
    if i>0 and i<len(arr)-2:
            nhood = arr[i-1:i+2]
    elif i<len(arr)-2:
        nhood = np.array([arr[-1], arr[i], arr[i+1]])
    else:
        nhood = arr[i:i+2-len(arr)]

    return nhood

def f1(nhood):
    return 0

def f2(nhood):
    # implementing ECA rule 22
    if np.count_nonzero(nhood==1)==1:
        new_val = 1
    else:
        new_val = 0
    
    return new_val

def iterate_dCA(arr, n, l):
    new_arr = np.zeros(n)

    # generate array of length n determining whether f2 will be followed
    follow_f2 = np.random.random(n)>l

    for i in range(n):
        nhood = get_neighbourhood(arr, i)

        # if this entry in follow_f2 is True, then follow rule f2
        if follow_f2[i]:
            new_arr[i] = f2(nhood)
        else:
            new_arr[i] = f1(nhood)
    
    return new_arr

cells2prime = iterate_dCA(cells, len(cells), 0.7)






