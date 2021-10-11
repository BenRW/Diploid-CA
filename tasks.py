import numpy as np
import matplotlib.pyplot as plt
import DCA
import time


def vary_lambda():
    l = 0
    threshold = 0.02
    density = []
    l_array = []
    n = 0

    while l < 1.:
        DCA_i = DCA.DiploidCA(n=1000, nt=500, l=l)
        DCA_i.run()
        density.append(DCA_i.get_density())
        l_array.append(l)

        if n==0 or density[n] - density[n-1]>threshold:
            l += 0.01
            # threshold = 0.2
        else:
            l += 0.05
            # threshold = 0.1
        # l += 0.05

        n+=1

    density = np.asarray(density)
    l_array = np.asarray(l_array)

    plt.plot(l_array, density)
    plt.show()

    return l_array, density

start = time.time()

l, d = vary_lambda()

print(time.time()-start)
