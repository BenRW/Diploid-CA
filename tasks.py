import numpy as np
import matplotlib.pyplot as plt
import DCA
import time
import glob, os


def vary_lambda(size, n_iterations, save=True):
    l = 0
    threshold = 0.01
    density = []
    l_array = []
    n = 0
    large_step = False

    while l < 1.:
        DCA_i = DCA.DiploidCA(n=size, nt=n_iterations, l=l)
        DCA_i.run(history=False)
        density.append(DCA_i.get_density())
        l_array.append(l)

        if n==0 or density[n] - density[n-1]>threshold:
            #threshold = 0.005
            if large_step:
                l = l_array[-2]
                density.pop()
                l_array.pop()
                n-=1
            l += 0.01
            large_step = False
        else:
            l += 0.05
            #threshold = 0.01
            large_step = True
        n+=1
        print(n, l)

    density = np.asarray(density)
    l_array = np.asarray(l_array)

    if save:
        # saving data to files with unique names so they won't overwrite
        np.savetxt("data/vary_lambda_"+str(size)+"_"+str(n_iterations)+"_"+str(time.time())+".txt",
                    (l_array, density), delimiter=", " )
    else:
        plt.plot(l_array, density)
        plt.show()

    return l_array, density

# start = time.time()

# for _  in range(50):
#     larray, density = vary_lambda(500, 100)

# speed = time.time() - start
# print('Simulation time: '+str(speed))

def vary_lambda_analysis(size, n_iterations):
    """Plots all saved runs of the same system size and number of iterations
    on a single figure"""
    l_arrays = []
    densities = []
    os.chdir("data/")
    for file in glob.glob("*.txt"):
        print(file)
        # finding system size from filename (number after 2nd '_')
        u = file.find('_')+1
        u += file[u:].find('_')+1
        u2 = file[u:].find('_') + u
        s = int(file[u:u2])
        if s==size:
            u += file[u:].find('_')+1
            u2 = file[u:].find('_') + u
            nt = int(file[u:u2])
            if nt==n_iterations:
                l, d = np.loadtxt(file, delimiter=", ")
                l_arrays.append(l)
                densities.append(d)
        
    # plot all runs in a single figure
    plt.figure()
    for i in range(len(l_arrays)):
        plt.plot(l_arrays[i], densities[i], alpha=0.75)
    plt.ylabel(r"$\rho$")
    plt.xlabel(r"$\lambda$")
    plt.show()
    
            
    return 0

vary_lambda_analysis(500, 100)