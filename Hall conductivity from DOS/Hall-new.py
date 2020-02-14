#!/usr/bin/env python
# coding=utf-8
import matplotlib
import matplotlib.pyplot as plt 
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks
import numpy as np 
from scipy import integrate 
data = np.loadtxt('DOS_new.dat')
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

x = np.array(data[:,0])-mu     #10-degree:0.9256 30-degree:0.9247 #5-degree:0.9382
y = data[:,1]
dicts= dict(zip(x,y))
x_zoom= []
y_zoom = []
for key,val in dicts.items():
    if -0.3<key<0.3:
        x_zoom.append(key)
        y_zoom.append(val) 
peaks,_ = find_peaks(y_zoom,prominence=0.002)
x_new = np.array(x_zoom)
y_new = np.array(y_zoom)
E0 = 0 #min(abs(x_new[peaks]))
Eb = max(x_new[peaks])
Ea = min(x_new[peaks])
#####
"""
Ex_0b = [x for x in x_new if x>= E0 ]
Ex_0a = [x for x in x_new if x<=E0 ]
x_peak_positive = [x for x in x_new[peaks] if x >= E0]
x_peak_negative = [x for x in x_new[peaks] if x <=E0]
"""
dict2 = dict(zip(x_new,y_new))

#right_cne = [get_right_cne(i) for i in range(10)]
#print(right_cne)
#left_cne = [get_left_cne(i) for i in range(10)]
#print(left_cne)

##### Deal with the units
#ConducUnits = 1. #finall in units of 2e^2/h if ConducUnits = 2
#ConducFactor1 = 1577882.2/B #B = Magnetic field in Telsa in units of e^2/h
#ConducFactor1 = ConducFactor1*Nlayer/ConducUnits
#ConducFactor1 = ConducFactor1/(CarbonCarbonDIstance/0.142)**2
CC_dist = 0.1418
B = 20
ConducFactor = (157882.2/B)*2/(CC_dist/0.1420)**2

def get_cne():
    Energy = []
    DOS = []
    sum_DOS = []
    for key, val in dict2.items():
        Energy.append(key)
        DOS.append(val)
        sumne = integrate.simps(DOS,Energy)
        sum_DOS.append(sumne)
    #print(sum_DOS)
    return sum_DOS
#dict3 = dict(zip(x_new,np.array(get_cne())))
def get_zero():
    Energy = []
    DOS = []
    sum_DOS = []
    for key,val in dict2.items():
        if key <= E0:
            Energy.append(key)
            DOS.append(val)
            sumne = integrate.simps(DOS,Energy)
            sum_DOS.append(sumne)
    return  sum_DOS

a = np.array(get_zero())
b = a[-1]
print(b)
Hall = (np.array(get_cne())-b)*ConducFactor
fig,ax = plt.subplots()
ax.plot(x_new,Hall)
plt.minorticks_on()
ax.grid(which='both',axis='y',linestyle='--')
np.savetxt('Hall.dat',np.column_stack((x_new,Hall)))
ax.set(xlabel='Energy(eV)',ylabel=r'$\frac{e^2}{h}$',
           title="TBG-5-20T-Hall Conductivity from DOS")
plt.show()

