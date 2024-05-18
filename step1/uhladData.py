from globals import MAX_TOT, RESOLUTION

kolkoPozeram = 2

def funkcia(): 

  inputFile = f"calibrationData.rudolf"
  outputFile = f"calibrationDataUhladene"+str(kolkoPozeram)+".rudolf"

  if kolkoPozeram <= 0:
    print("zle cislo")
    return

  print("alokacia",RESOLUTION*RESOLUTION,"x",MAX_TOT,"pola")
  result = [[0]*MAX_TOT for i in range(RESOLUTION*RESOLUTION)]

  file = open(inputFile, 'r', encoding='utf-8')

  riadokCislo = 0

  print("start")

  for riadok in file:
    riadok = riadok.strip()
    riadok = riadok.split(" ")
    arrayRiadok = riadok

    for i in range(len(arrayRiadok)):
      arrayRiadok[i] = int(arrayRiadok[i])

    for i in range(len(arrayRiadok)):
      sum = 0
      if i >= kolkoPozeram and i+kolkoPozeram < MAX_TOT:
        for y in range((kolkoPozeram*2)+1):
          sum += arrayRiadok[-kolkoPozeram+y+i]
        result[riadokCislo][i] = round(sum/((kolkoPozeram*2)+1))
    
    riadokCislo += 1
        
  outputFile = open(outputFile, 'w', encoding='utf-8')

  
  for riadok in result:
    for hodnota in riadok:
      outputFile.write(str(hodnota))
      outputFile.write(" ")
    outputFile.write("\n")

  file.close()
  outputFile.close()

  print("done")

funkcia()