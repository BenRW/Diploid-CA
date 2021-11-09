import numpy as np
import matplotlib.pyplot as plt
import DCA
import time
import glob, os

def vary_lambda(size, n_iterations, save=True, is_22=True):
    l = 0
    threshold = 0.01
    density = []
    l_array = []
    n = 0
    large_step = False

    while l <= 1.3:
        if is_22:
            DCA_i = DCA.DiploidCA(n=size, nt=n_iterations, l=l)
        else:
            DCA_i = DCA.DiploidCA(n=size, nt=n_iterations, l=l, rule=254)
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
        if is_22:
            np.savetxt("data/vary_lambda_"+str(size)+"_"+str(n_iterations)+"_"+str(time.time())+".txt",
                        (l_array, density), delimiter=", " )
        else:
            np.savetxt("data/vary_lambda_254_"+str(size)+"_"+str(n_iterations)+"_"+str(time.time())+".txt",
                        (l_array, density), delimiter=", " )
    else:
        plt.plot(l_array, density)
        plt.show()

    return l_array, density

def vary_lambda_analysis(size, n_iterations, is_22=True):
    """Plots all saved runs of the same system size and number of iterations
    on a single figure"""
    l_arrays = []
    densities = []
    os.chdir("data/")
    for file in glob.glob("*.txt"):
        if is_22:
            # finding system size from filename (number after 2nd '_')
            u = file.find('_')+1
            u += file[u:].find('_')+1
            u2 = file[u:].find('_') + u
            s = int(file[u:u2])
        else:
            # finding system size from filename (number after 3rd '_')
            u = file.find('_')+1
            u += file[u:].find('_')+1
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

    # compute mean and std of "averaged run"
    l_av = np.arange(0, 0.99, 0.01)
    rho_matrix = np.zeros((len(l_arrays), len(l_av)))
    for i in range(len(l_arrays)):
        rho_matrix[i, :] = np.interp(l_av, l_arrays[i], densities[i])
    rho_av = rho_matrix.mean(axis=0)
    rho_std = rho_matrix.std(axis=0)
        
    # plot all runs in a single figure
    plt.figure(1)
    for i in range(len(l_arrays)):
        plt.plot(l_arrays[i], densities[i], alpha=0.75)
    plt.ylabel(r"$\rho$")
    plt.xlabel(r"$\lambda$")

    # plot averaged run with estimated uncertainties
    plt.figure(2)
    plt.fill_between(l_av, rho_av-2*rho_std, rho_av+2*rho_std, facecolor="r", alpha=0.4, label="2$\sigma$")
    plt.plot(l_av, rho_av, "r-", label="mean")
    plt.ylabel(r"$\rho$")
    plt.xlabel(r"$\lambda$")
    plt.legend()

    # plot together
    fig3, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(9,3))
    if is_22:
        ax1.axvspan(0.72, 0.73, facecolor='blue', alpha=0.4)
    for i in range(len(l_arrays)):
        ax1.plot(l_arrays[i], densities[i], alpha=0.75)
    ax1.set_ylabel(r"$\rho$")
    ax2.set_xlabel(r"$\lambda$")
    if is_22:
        ax2.axvspan(0.72, 0.73, facecolor='blue', alpha=0.4)
    ax2.fill_between(l_av, rho_av-2*rho_std, rho_av+2*rho_std, facecolor="#ffa1a1", label="2$\sigma$")
    ax2.plot(l_av, rho_av, "r-", label="mean")
    ax2.set_xlabel(r"$\lambda$")
    ax2.legend()

    # subfigure labels
    ax1.text(0.94, 0.02, "a)", fontsize=13, backgroundcolor="#ededed")
    ax2.text(0.94, 0.02, "b)", fontsize=13, backgroundcolor="#ededed")

    fig3.tight_layout()

    os.chdir("..")
    if is_22:
        plt.savefig("figs\\density_lambda.pdf")
    # else:
        #  plt.savefig("figs\\density_lambda254.pdf")

    plt.show()

    
    
            
    return 0

def st_diagram_DCA(size, n_iterations):
    eca22 = DCA.DiploidCA(n=size, nt=n_iterations, l=1)
    eca22.run(history=True)
    fig, ax = eca22.get_diagram()

    # fig.savefig("figs\\ECA22_"+str(size)+"_"+str(n_iterations)+".pdf")
    plt.show()



start = time.time()

<<<<<<< HEAD
for _ in range(5):
=======
for _ in range(7):
>>>>>>> bd19edd88f5b523e3ab09714e81681ba3e854755
    larray, density = vary_lambda(10000, 5000, is_22=False)

speed = time.time() - start
print('Simulation time: '+str(speed))

# vary_lambda_analysis(500, 100, is_22=False)
# vary_lambda_analysis(10000, 5000, is_22=False)