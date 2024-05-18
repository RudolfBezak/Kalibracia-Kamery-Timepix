
from globals import MAX_TOT

inputFile = f"calibrationData.rudolf"
outputFile = f"summedCalibrationData.rudolf"

# inputFile = f"calibrationDataWithGaussMoved2.rudolf"
# outputFile = f"summedMovedDataWithGauss2.rudolf"

# spocita vsetky riadky a vrati array 1xMAX_TOT
def sumCalibrationData(input, pole = False):
  print("start")

  if pole:
    result = [0]*len(input[0])
    for i in range(len(input[0])):
      for j in range(len(input[i])):
        result[i] += int(input[j][i])

  else: 
    file = open(input, 'r', encoding='utf-8')

    result = [0]*MAX_TOT
    

    # pre kazdy riadok
    for riadok in file:
      riadok = riadok.strip()
      riadok = riadok.split(" ")
      indexDat = 0
      for data in riadok:
        result[indexDat] += int(data)
        indexDat += 1

    file.close()

  return result

#zapise pole do suboru
def writeToFile(array):

  file = open(outputFile, 'w', encoding='utf-8')
  
  for data in array:
    file.write(str(data))
    file.write(" ")

  return

# writeToFile(sumCalibrationData(inputFile))
# print("done")