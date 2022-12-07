
from countLines import countLines
from riadoknaPole import riadokNaPole
from globals import MAX_TOT

VELKOST_CLUSTERA = 1
PERCENT_VYPIS = 5

inputFile = f"./SiCTPX3/SiCTPX3L06-GeRTG40kV100uA.clog"
# inputFile = f"./SiCTPX3/SiCTPX3L06-InRTG40kV100uA.clog"
outputFile = f"calibrationData.rudolf"
# fileAdress = f"input.clog"

print("start")

pocetRiadkov = countLines(inputFile)
print("subor ma",pocetRiadkov,"riadkov")
pocetRiadkovNaPercenta = round(pocetRiadkov/(100/PERCENT_VYPIS))

#funkcia vezme raw data a premeni to na 65k x 300 subor s datami s velkostou clustera 1
def toCalibration(fileAdress):
  file = open(fileAdress, 'r', encoding='utf-8')

  print("alokacia",256*256,"x",MAX_TOT,"pola")
  result = [[0]*MAX_TOT for i in range(256*256)]

  riadokNaProgress = 0 
  percenta = 0
  # prejdi vsetky riadky
  print("start raw -> array")
  for line in file:
    # print(line)
    if (riadokNaProgress == pocetRiadkovNaPercenta):
      riadokNaProgress = 0
      percenta = percenta + 5
      print(percenta,"%")
    riadokNaProgress += 1

    #ak je to riadok s datami 
    if (line[0] == "["):
      line = riadokNaPole(line)
      if (len(line) == VELKOST_CLUSTERA):
        #pre kazdy zaznam v riadku (tu by to mal byt vzdy 1)
        for zaznam in line:
          #da prec "," a rozdeli na array
          zaznam = zaznam.replace(",", "")
          zaznam = zaznam.split(" ")
          #vypocita suradnicu
          x = int(zaznam[0])
          y = 256 * int(zaznam[1])
          riadok = x + y
          stlpec = int(zaznam[2])
          #ak ma mensie ToT ako mnou stanovene maximalne
          if stlpec-1 < MAX_TOT:
            #zapise do vysledneho pola
            result[riadok][stlpec-1] += 1

  file.close()
  print("end raw -> array")
  return result

  #kalibracne data do suboru
def calibrationToFile(calibrationData):
  print("zapisujem vystup do suboru")
  file = open(outputFile, 'w', encoding='utf-8')

  for riadok in calibrationData:
    for data in riadok:
      file.write(str(data))
      file.write(" ")
    file.write("\n")

  file.close()
  print("zapisane do suboru")
  return

calibrationToFile(toCalibration(inputFile))
print("done")
