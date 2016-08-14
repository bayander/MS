import os, sys, pylab, Magic

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
    No = file2read.replace('Om', '')[-9:-7]
    try:
        U, I = Magic.getData(file2read)
        with open(sys.argv[2] + str(No) +'_MS.txt', 'w') as file2write:
            save2file([U, I],                file2write, 'U, V\tI, A')
    
        fluxProcessing = Magic.relFlux(U, I)
        fluxes = fluxProcessing.peaks
        with open(sys.argv[2] + str(No) +'_Magic.txt', 'w') as file2write:
            save2file(fluxes, file2write, 'U, V\tInt\tRelInt')
    except:
        print file2read
        pass
