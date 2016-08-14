import scipy.signal as ss
import numpy as np

def norm(data, mode = 'int'):
    if   (mode == 'int'):
        denominator = sum(data)
    elif (mode == 'amp'):
        denominator = max(data)
    return [value/denominator for value in data]

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
    return U, ss.savgol_filter(norm(I, 'amp'), 15, 2)
 
class relFlux():
    def __init__(self, U, I):
        self.peaks  = self.getPeaks(U, I)

    def getPeaks(self, U, I):
        widths = np.arange(1, int(len(I)/10.0))
        peaks = [peak for peak in ss.find_peaks_cwt(I, widths) if I[peak] > 0.10] 
        #Warning Hardcode!!! Setting a value of minimal "detected" mass...  

        Vol = []
        Int = []
        Rel = []
        for i in range(len(peaks)):
            Vol.append(U[peaks[i]])
            Int.append(self.peakInt(peaks[i], U, I))
            Rel.append(Int[-1]/Vol[-1])
        return Vol, norm(Int), norm(Rel)

    def peakInt(self, index, U, I):
        Imax = I[index]
        Imin = Imax/10.0 #Warning Hardcode!!! Setting a value of minimal integrated level of each peak.
    
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
