import matplotlib.pyplot as plt
import numpy as np
from astropy import modeling
from globals import MAX_TOT

middle = 22
low = 15
high = 35

inputFile = f"calibrationDataWithGauss.rudolf"
outputFile = f"calibrationDataWithGaussMoved.rudolf"

riadokNaProgress = 0
patpercent = round((256*256)/20)
progress = 0

file = open(inputFile, 'r', encoding='utf-8')
outputFile = open(outputFile, 'w', encoding='utf-8')
print("start")
for riadok in file:
  index = 0
  parametre = []
  #str to int
  riadok = riadok.strip()
  riadok = riadok.split(" ")
  arrayRiadok = riadok
  for i in range(len(arrayRiadok)):
    arrayRiadok[i] = round(float(arrayRiadok[i]))

  pocetParametrov = int(arrayRiadok[i])
  stred = int(arrayRiadok[2])

  #najdeny 1. peak
  if ((stred > low) and (stred < high)):
    posunOPocetDoprava = (middle - stred)
    riadokNaZapis = [0]*MAX_TOT
    #posun doprava
    if posunOPocetDoprava >= 0:
      for index in range(MAX_TOT - posunOPocetDoprava):
        riadokNaZapis[index + posunOPocetDoprava] = arrayRiadok[index + 4]
        

    #posun dolava
    if posunOPocetDoprava < 0:
      for index in range(MAX_TOT - (-posunOPocetDoprava)):
        riadokNaZapis[index] = arrayRiadok[index + posunOPocetDoprava + 4]


    #zapis do suboru
    for data in riadokNaZapis:
      outputFile.write(str(data))
      outputFile.write(" ")
    outputFile.write("\n")


file.close()
outputFile.close()

print("end")
