import numpy as np


class DiploidCA:
    def __init__(self, n, nt, l):
        self._n = n
        self._l = l
        self._nt = nt

        # initial configuration
        self._arr = np.random.randint(0, 2, self._n)

        # defining 2D array that will store all previous values
        self._history = np.zeros((self._nt, self._n))
        self._history[0, :] = self._arr
    
    def get_neighbourhood(self, i):
        # note that the boundaries are periodic
        if i>0 and i<len(self._arr)-2:
            self._nhood = self._arr[i-1:i+2]
        elif i<len(self._arr)-2:
            self._nhood = np.array([self._arr[-1], self._arr[i], self._arr[i+1]])
        else:
            self._nhood = self._arr[i:i+2-len(self._arr)]

    def f1(self):
        return 0

    def f2(self):
        # implementing ECA rule 22
        if np.count_nonzero(self._nhood==1)==1:
            new_val = 1
        else:
            new_val = 0
        
        return new_val

    def iterate_dCA(self, t):
        new_arr = np.zeros(self._n)

        # generate array of length n determining whether f2 will be followed
        follow_f2 = np.random.random(self._n)<self._l

        for i in range(self._n):
            nhood = self.get_neighbourhood(i)

            # if this entry in follow_f2 is True, then follow rule f2
            if follow_f2[i]:
                new_arr[i] = self.f2()
            else:
                new_arr[i] = self.f1()
        
        self._arr = new_arr.copy()
        self._history[t] = new_arr.copy()
    
    def run(self, history = False):
        for t in range(1, self._nt):
            self.iterate_dCA(t)
        
        if history:
            return self._arr, self._history
        else:
            return self._arr


DCA1 = DiploidCA(n=20, nt=20, l=0.7)
final_arr1, history1 = DCA1.run(history=True)

print(history1)





    
