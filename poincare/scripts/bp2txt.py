import adios2
import sys
import numpy as np

if len(sys.argv) != 4 :
    print('usage: ', sys.argv[0], ' infile outfile particle_skip')
    sys.exit()


inFile = sys.argv[1]
out = sys.argv[2]
particle_skip = int(sys.argv[3])

outRZ = out + '.txt'
outTP = out + '.TP.txt'

f=adios2.open(inFile, 'r')
ID=f.read('ID')

def ParseArrays(data, ids, skip, maxPunc) :
    out = []

    id0 = -1
    pCnt = 0
    n = int(len(data) / 2)
    for i in range(0, n, skip) :
        id = ids[i]
        if id < 0 : continue

        if id0 == id :
            pCnt = pCnt+1
        else :
            id0 = id
            pCnt = 0
        if pCnt < maxPunc :
            out.append( (id, data[i*2+0], data[i*2+1], pCnt) )

    return out


rz=f.read('RZ')

pRZ = ParseArrays(rz, ID, particle_skip, 1000)
print('saving ', outRZ)
np.savetxt(outRZ, pRZ, delimiter=",", fmt='%d, %lf, %lf, %d', header='ID, R, Z, PUNC')
print('Done.')
pRZ = []

tp=f.read('ThetaPsi')

pTP = ParseArrays(tp, ID, particle_skip, 1000)
print('saving ', outTP)
np.savetxt(outTP, pTP, delimiter=",", fmt='%d, %lf, %lf, %d', header='ID, THETA, PSI, PUNC')
print('Done.')
pTP = []
