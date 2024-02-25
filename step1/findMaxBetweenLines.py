from time import sleep


inputFile = f"calibrationData.rudolf"
outputFile = f"amMaxPeak2.rudolf"
start = 50
koniec = 200

riadokCislo=0

print("start")

file = open(inputFile, 'r', encoding='utf-8')
file2 = open(outputFile, 'w', encoding='utf-8')
for riadok in file:
    data = [int(x) for x in riadok.split()]
    sublist = data[start:koniec + 1]
    
    max_value = sublist.index(max(sublist)) + start
    file2.write(str(max_value))
    file2.write("\n")

file.close()
file2.close()

print("done")
