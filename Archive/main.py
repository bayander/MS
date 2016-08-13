import os, sys, pylab, relFlux 
import scipy.signal as ss

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
    result['I'] = ss.savgol_filter(result['I'], 15, 2)
    Imax = max(result['I'])
    result['I'] = [I/Imax for I in result['I']]            
    return result

def action(fileName):
    data  = getData(fileName)
    rf = relFlux.relFlux(data['U'], data['I'])
    print(fileName, rf.peaks['U'])
    print(fileName, file = results)
    for U, Int, Rel in zip(rf.peaks['U'], rf.peaks['int'], rf.peaks['rel']):
        print (U, Int, Rel, file=results)
    pylab.plot(data['U'], data['I'])
    for point in rf.peaks['U']:
        pylab.plot(point, 0, '.', color='red')
    pylab.show()

folderPath = sys.argv[1]

results = open(folderPath + 'results.txt', 'w')

for file in os.listdir(folderPath):
    if file.endswith(".txt"):
        try:
            action(folderPath + file)
        except:
            pass

results.close()            
