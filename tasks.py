import numpy as np
import matplotlib.pyplot as plt
import DCA
import time


def vary_lambda():
    l = 0
    threshold = 0.01
    density = []
    l_array = []
    n = 0
    large_step = False

    while l < 1.:
        DCA_i = DCA.DiploidCA(n=2000, nt=1000, l=l)
        DCA_i.run(history=False)
        density.append(DCA_i.get_density())
        l_array.append(l)

        if n==0 or density[n] - density[n-1]>threshold:
            #threshold = 0.005
            if large_step:
                l = l_array[-2]
                del density[-1]
                del l_array[-1]
                n-=1
            l += 0.01
            large_step = False
        else:
            l += 0.05
            #threshold = 0.01
            large_step = True
        n+=1

    density = np.asarray(density)
    l_array = np.asarray(l_array)

    plt.plot(l_array, density)
    plt.show()

    return l_array, density

start = time.time()

larray, density = vary_lambda()

speed = time.time() - start
print('Simulation time: '+str(speed))