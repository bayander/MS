import os, sys, pylab, relFlux
from scipy import signal

def getData(path):
    U = []
    I = []
    with open(path, 'r') as file:
        for line in file:
            U.append(float(line.split('\t')[0].replace(',', '.')))
            _I = -float(line.split('\t')[1].replace(',', '.'))
            if (_I >= 0):
                I.append(_I)
            else:
                I.append(0)
    Imax = max(I)
    I = signal.savgol_filter([i/Imax for i in I], 15, 2)            
    return U, I

def fileList(folderPath):
    list = []
    for file in os.listdir(folderPath):
        if file.endswith(".txt"):
            list.append(folderPath + file)
    return list        

def save2file(data, file2write, titles):
    file2write.write(titles + '\n')
    for j in range(len(data[0])):
        string = ''
        for i in range(len(data)):
            string += str(data[i][j]) + '\t'
        file2write.write(string + '\n')    

for file2read in fileList(sys.argv[1]):
    U, I = getData(file2read)
    with open(sys.argv[2] + str(file2read[-11:-9]) +'_MS.txt', 'w') as file2write:
        save2file([U, I],                file2write, 'U, V\tI, A')
    
    fluxProcessing = relFlux.relFlux(U, I)
    fluxes = fluxProcessing.peaks
    with open(sys.argv[2] + str(file2read[-11:-9]) +'_Magic.txt', 'w') as file2write:
        save2file(fluxes, file2write, 'U, V\tInt\tRelInt')
