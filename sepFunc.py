import os, scipy.signal as ss

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
