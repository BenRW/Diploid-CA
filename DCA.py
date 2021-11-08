import numpy as np
import matplotlib.pyplot as plt

class DiploidCA:
    def __init__(self, n, nt, l, rule=22):
        self._n = n
        self._l = l
        self._nt = nt

        if rule==22:
            self._f2_choice = 22
        else:
            self._f2_choice = 254

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

    def f1(self):
        return 0

    def rule22(self):
        """Implements ECA rule 22"""
        if np.count_nonzero(self._nhood)==1:
            new_val = 1
        else:
            new_val = 0
        
        return new_val

    def rule254(self):
        """Implements ECA rule 254. Note that rule 254=11111110, yields 
        1 for all neighbourhoods but 000."""
        if self._nhood[0]==1:
            new_val = 1
        else:
            if self._nhood[1]==1:
                new_val=1
            else:
                if self._nhood[2]==1:
                    new_val=1
                else:
                    # only the case if self._nhood=[0,0,0]
                    new_val=0
        
        return new_val

    def iterate_dCA22(self, t, history):
        """Iterates the DCA, where f2 is rule 22. Saves configuration of 
        domain if history is true."""
        new_arr = np.zeros(self._n)

        # generate array of length n determining whether f2 will be followed
        follow_f2 = np.random.random(self._n)<self._l

        for i in range(self._n):
            self.get_neighbourhood(i)

            # if this entry in follow_f2 is True, then follow rule f2
            if follow_f2[i]:
                new_arr[i] = self.rule22()
            else:
                new_arr[i] = self.f1()
        
        self._arr = new_arr.copy()
        if history:
            self._history[t] = new_arr.copy()

    def iterate_dCA254(self, t, history):
        """Iterates the DCA, where f2 is rule 254. Saves configuration of 
        domain if history is true."""
        new_arr = np.zeros(self._n)

        # generate array of length n determining whether f2 will be followed
        follow_f2 = np.random.random(self._n)<self._l

        for i in range(self._n):
            nhood = self.get_neighbourhood(i)

            # if this entry in follow_f2 is True, then follow rule f2
            if follow_f2[i]:
                new_arr[i] = self.rule254()
            else:
                new_arr[i] = self.f1()
        
        self._arr = new_arr.copy()
        if history:
            self._history[t] = new_arr.copy()
    
    def run(self, history=False):
        if self._f2_choice==22:
            for t in range(1, self._nt):
                self.iterate_dCA22(t, history)
        else:
            for t in range(1, self._nt):
                self.iterate_dCA254(t, history)
        
        if history:
            return self._arr, self._history
        else:
            return self._arr

    def get_density(self):
        d = np.mean(self._arr)

        return d

    def get_diagram(self):
        fig, ax = plt.subplots()
        im = ax.imshow(self._history, cmap="binary")
        ax.set_xlabel("x")
        ax.set_ylabel("Time")

        return fig, ax



