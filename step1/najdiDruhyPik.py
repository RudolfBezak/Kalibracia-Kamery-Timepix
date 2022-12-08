

inputFile = f"calibrationDataUhladene1.rudolf"
outputFile = f"calibrationData2ndPeak.rudolf"

maxPokles = 5


print("start")
file = open(inputFile, 'r', encoding='utf-8')

maximum = [-1]*(256*256)
maxIndex = [-1]*(256*256)

pixel = -1

for riadok in file:

  pixel += 1

  riadok = riadok.strip()
  riadok = riadok.split(" ")
  arrayRiadok = riadok

  for i in range(len(arrayRiadok)):
    arrayRiadok[i] = int(arrayRiadok[i])

  for i in range(len(arrayRiadok)):

    #chod z lava
    #ak klesne aspon o "maxPokles" tak skonci
    if (maxIndex[pixel] != -1 and (arrayRiadok[maxIndex[pixel]]) > (arrayRiadok[len(arrayRiadok) - i - 1]) + maxPokles):
      break

    
    if (arrayRiadok[len(arrayRiadok) - i - 1] > maximum[pixel]):
        maximum[pixel] = (arrayRiadok[len(arrayRiadok) - i - 1])
        maxIndex[pixel] = len(arrayRiadok) - i - 1

  #odsekni o pocetDolava vlavo hodnotu
  #TODO

  #fit gauss
  #TODO

print(maxIndex)