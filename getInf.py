import scipy.signal as ss
import numpy as np
from sepFunc import norm

class fromMS():
    def __init__(self, R = 3.5e-2):
        self.R = R

    def _BUpl(self, MZ1, U1, MZ2, U2):
        K = MZ1*MZ2*((U2 - U1)/(MZ1 - MZ2))
        B = (K/4.8e7)**0.5/self.R
        Upl = (MZ2*U2 - MZ1*U1)/(MZ1 - MZ2)
        return B, -Upl
     
    def BUpl(self, U, tag):
        if (len(U) == 3):
            B_Upl = []
            B_Upl.append(self._BUpl(3.0, U[0], 2.0, U[1]))
            B_Upl.append(self._BUpl(3.0, U[0], 1.0, U[2]))
            B_Upl.append(self._BUpl(2.0, U[1], 1.0, U[2]))
            B   = np.mean([_B_Upl[0] for _B_Upl in B_Upl])
            Upl = np.mean([_B_Upl[1] for _B_Upl in B_Upl])
        return B, Upl    

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
