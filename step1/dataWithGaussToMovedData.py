from globals import MAX_TOT

middle = 22
low = 15
high = 60

inputFile = f"calibrationDataWithGauss2.rudolf"
outputFile = f"calibrationDataWithGaussMoved2.rudolf"

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

  pocetParametrov = int(arrayRiadok[0])
  stred = int(arrayRiadok[2])

  #najdeny 1. peak
  if ((stred > low) and (stred < high)):
    posunOPocetDoprava = (middle - stred)
    riadokNaZapis = [0]*MAX_TOT
    #posun doprava
    if posunOPocetDoprava >= 0:
      for index in range(MAX_TOT - posunOPocetDoprava):
        riadokNaZapis[index + posunOPocetDoprava] = arrayRiadok[index + 1 + pocetParametrov]
        

    #posun dolava
    if posunOPocetDoprava < 0:
      for index in range(MAX_TOT - (-posunOPocetDoprava)):
        riadokNaZapis[index] = arrayRiadok[index - posunOPocetDoprava + 1 + pocetParametrov]


    #zapis do suboru
    for data in riadokNaZapis:
      outputFile.write(str(data))
      outputFile.write(" ")
    outputFile.write("\n")


file.close()
outputFile.close()

print("end")
