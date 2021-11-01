import numpy as np
import matplotlib.pyplot as plt

class ECA172:
    def __init__(self, n, nt):
        self._n = n
        self._nt = nt

        # initial configuration
        self._arr = np.random.randint(0, 2, self._n)

        # defining 2D array that will store all previous values
        self._history = np.zeros((self._nt, self._n))
        self._history[0, :] = self._arr
    
    def get_neighbourhood(self, i):
        # note that the boundaries are periodic
        if i>0 and i<len(self._arr)-2:
            # if entry somewhere in middle of array
            self._nhood = self._arr[i-1:i+2]
        elif i<len(self._arr)-2:
            # if entry at start of array
            self._nhood = np.array([self._arr[-1], self._arr[0], self._arr[1]])
        else:
            # if entry at end of array
            self._nhood = np.array([self._arr[-2], self._arr[-1], self._arr[0]])

    def f172(self):
        # implementing ECA rule 172
        if self._nhood[0]==1:
            new_val = self._nhood[-1]
        elif self._nhood[0]==0 and self._nhood[1]==0:
            new_val = 0
        else:
            new_val = 1
        
        return new_val

    def iterate_dCA(self, t):
        new_arr = np.zeros(self._n)

        for i in range(self._n):
            self.get_neighbourhood(i)
            new_arr[i] = self.f172()
        
        self._arr = new_arr.copy()
        self._history[t] = new_arr.copy()
    
    def run(self):
        for t in range(1, self._nt):
            self.iterate_dCA(t)
        
        return self._history
    
    def get_diagram(self):
        fig, ax = plt.subplots()
        im = ax.imshow(self._history, cmap="binary")
        ax.set_xlabel("x")
        ax.set_ylabel("Time")

        plt.show()

eca1 = ECA172(100, 100)
arr = eca1.run()
eca1.get_diagram()