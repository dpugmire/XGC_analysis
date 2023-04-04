import adios2
import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 4 :
    print('usage: ', sys.argv[0], ' infile skip <rz or tp>')
    sys.exit()

inFile = sys.argv[1]
skip = int(sys.argv[2])
whichCoords = sys.argv[3]
if whichCoords not in ['rz', 'tp'] :
    print('whichCoords must be "rz" or "tp": ', whichCoords, ' not valid')
    sys.exit()

##Read in data.
f = adios2.open(inFile, 'r')
ID = f.read('ID')
R = f.read('R')
Z = f.read('Z')
THETA = f.read('Theta')
PSI = f.read('Psi')
numPts = len(R)
numPuncs = len(R[0])

fig = plt.figure(figsize=[8,12])

print('numPts=', numPts)

for i in range(0,numPts, skip) :
    if whichCoords == 'rz' :
        x = R[i][np.where(ID[i] >= 0)]
        y = Z[i][np.where(ID[i] >= 0)]
    else:
        x = THETA[i][np.where(ID[i] >= 0)]
        y = PSI[i][np.where(ID[i] >= 0)]
    plt.scatter(x, y, s=1, marker='x', edgecolor='none')

plt.title('%s' % inFile)
plt.show()
