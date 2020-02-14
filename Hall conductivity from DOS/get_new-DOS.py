#!/usr/bin/env python
# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
def get0(filename):
    file = np.loadtxt(filename)
    energies = file[:,0]
    dos = file[:,1]
    counts = dict(zip(energies,dos))
    lst = list()
    for key,val in counts.items():
        if -5<key<5: 
            newtup = (val,key)
            lst.append(newtup)
            lst = sorted(lst,reverse=False)
    for val, key in lst[:1]:
        print(key,val)
        return key
def get_newtxt(filename,shift):
    DOS = np.loadtxt(filename)
    a0 = DOS[:,0]-shift
    a1 = DOS[:,1]
    fig = plt.plot(a0,a1)
    plt.show()
    np.savetxt('%s-2.txt'%filename[:-4],np.column_stack((a0,a1)))

def get_fermi(filename):
    dos = np.loadtxt(filename)
    x = np.array(dos[:,0])
    y = np.array(dos[:,1])
    I = integrate.simps(y,x) 
    print(I)
    for i in range(len(x)):
        sumdos = integrate.simps(y[:i+1],x[:i+1])
        while abs(sumdos - 0.5*I ) <= 1e-4:
            print(x[i])
            mu = x[i]
            return mu
mu = get_fermi('DOS_new.dat')
get_newtxt('DOS_new.dat',mu)
