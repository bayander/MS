import os, sys
import pylab
import scipy.signal as ss
import numpy as np

def getData(path):
    result = {'U': [], 'I': []}
    with open(path, 'r') as file:
        for line in file:
            result['U'].append(float(line.split('\t')[0].replace(',', '.')))
            I = -float(line.split('\t')[1].replace(',', '.'))
            if (I >= 0):
                result['I'].append(I)
            else:
                result['I'].append(0)
    Imax = max(result['I'])
    result['I'] = [I/Imax for I in result['I']]            
    return result

def fileList(folderPath):
    list = []
    for file in os.listdir(folderPath):
        if file.endswith(".txt"):
            list.append(folderPath + file)
    return list        

def peakInt(index, U, I):
    Imax = I[index]
    Imin = Imax/5.0
    
    Icur = Imax
    i = index
    while (Icur > Imin):
        i -= 1
        Icur = I[i]
    i_left = i    
    
    Icur = Imax
    i = index
    while (Icur > Imin):
        i += 1
        Icur = I[i]
    i_right = i

    index = np.arange(i_left, i_right+1)
    integral = 0
    for i in range(len(index)-1):
        integral += 0.5*abs(I[index[i+1]] - I[index[i]])*abs(U[index[i+1]] - U[index[i]])
    return integral    

def peaksInt(peaks, data):
    ints = []
    for peak in peaks:
        ints.append(peakInt(peak, data['U'], data['I']))
    integral = 0
    for i in range(len(data['U']) - 1):
        integral += 0.5*abs(data['I'][i+1] - data['I'][i])*abs(data['U'][i+1] - data['U'][i])
    ints = [_int/integral for _int in ints]
    return ints

def getPeaks(data):
    widths = np.arange(1, int(len(data['U'])/10.0))
    peaks = ss.find_peaks_cwt(data['I'], widths)
    ints = peaksInt(peaks, data)
    result = {'index': [], 'int': []}
    for i in range(len(peaks)):
        if (ints[i] >= 0.01):
            result['index'].append(peaks[i])
            result['int'].append(ints[i])
    return result        

def action(file):
    data  = getData(file)
    peaks = getPeaks(data)

    pylab.plot(data['U'], data['I'])
    for i in peaks['index']:
        pylab.plot(data['U'][i], data['I'][i], '.', color = 'red')
    print (peaks)
    #pylab.gca().invert_xaxis()

for file in fileList(sys.argv[1]):
    action(file)

#pylab.show()
