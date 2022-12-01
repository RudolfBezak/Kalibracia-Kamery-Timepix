
from globals import MAX_TOT

# inputFile = f"calibrationData2.rudolf"
# outputFile = f"summedCalibrationData2.rudolf"

inputFile = f"calibrationDataWithGaussMoved2.rudolf"
outputFile = f"summedMovedDataWithGauss2.rudolf"

# spocita vsetky riadky a vrati array 1xMAX_TOT
def sumCalibrationData(input):
  print("start")

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

writeToFile(sumCalibrationData(inputFile))
print("done")