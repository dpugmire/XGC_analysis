import adios2
import sys
import numpy as np

if len(sys.argv) != 4 :
    print('usage: ', sys.argv[0], ' infile outfile particle_skip')
    sys.exit()


inFile = sys.argv[1]
out = sys.argv[2]
particle_skip = int(sys.argv[3])
MAXPUNC = 5000

outRZ = out + '.txt'
outTP = out + '.TP.txt'

f=adios2.open(inFile, 'r')

def ParseArrays(ids, x, y, psi, skip, maxPunc) :
    out = []

    id0 = -1
    pCnt = 0
    n = int(len(x))
    psi0 = -1
    for i in range(0, n, skip) :
        id = ids[i]
        if id < 0 : continue

        if id0 == id :
            pCnt = pCnt+1
        else :
            id0 = id
            pCnt = 0
            psi0 = psi[i]

        p = psi[i]
        if pCnt < maxPunc :
            out.append((id, x[i], y[i], p, psi0, pCnt))

    return out


ID=f.read('ID')

print('Reading RZ.')
r=f.read('R')
z=f.read('Z')
print('Reading TP.')
t=f.read('Theta')
p=f.read('Psi')

pRZ = ParseArrays(ID, r, z, p, particle_skip, MAXPUNC)
print('saving ', outRZ)
np.savetxt(outRZ, pRZ, delimiter=",", fmt='%d, %lf, %lf, %lf, %lf, %d', header='ID, R, Z, PSI, PSI0, PUNC', comments='')
print('Done.')
pRZ = []

pTP = ParseArrays(ID, t, p, p, particle_skip, MAXPUNC)
print('saving ', outTP)
np.savetxt(outTP, pTP, delimiter=",", fmt='%d, %lf, %lf, %lf, %lf, %d', header='ID, THETA, PSI, PSI, PSI0, PUNC', comments='')
print('Done.')
pTP = []
