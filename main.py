import sys, pylab, getInf
from sepFunc import *

def No(string):
    index = string.index('#')
    return int(string.replace('Om', '')[index+1:index+3])

strings2write = []
for file2read in fileList(sys.argv[1]):
    try:
        U, I = getData(file2read)
        with open(sys.argv[2] + str(No(file2read)) +'_MS.txt', 'w') as file2write:
            save2file([U, I], file2write, 'U, V\tI, A')
        fluxProcessing = getInf.relFlux(U, I)
        fluxes = fluxProcessing.peaks
        if (len(fluxes[0]) == 3):
            string  = str(No(file2read)) + '\t'
            for i in norm([f*m**0.5 for f, m in zip(fluxes[-1], [3, 2, 1])]):
                string += str(i) + '\t'
            MSProcessing = getInf.fromMS()
            B, Upl = MSProcessing.BUpl(fluxes[0], str(No))
            string += str(B) + '\t' + str(Upl) + '\n'
            strings2write.append(string)
    except:
        print file2read, '. FUCK OFF!'
        pass

with open(sys.argv[2] + 'Magic.txt', 'w') as file2write:
    title = 'No\tRel_H3+\tRel_H2+\tRel_H+\tB, T\tUpl, V\n'
    file2write.write(title)
    for string in strings2write:
        file2write.write(string)
