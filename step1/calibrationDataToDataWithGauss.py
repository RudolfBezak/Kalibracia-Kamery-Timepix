import matplotlib.pyplot as plt
import numpy as np
from astropy import modeling
from globals import MAX_TOT

# inputFile = f"summedCalibrationData.rudolf"
inputFile = f"calibrationData.rudolf"
outputFile = f"calibrationDataWithGauss.rudolf"

riadokNaProgress = 0
patpercent = round((256*256)/20)
progress = 0

file = open(inputFile, 'r', encoding='utf-8')
outputFile = open(outputFile, 'w', encoding='utf-8')
print("start")
for riadok in file:
  riadok = riadok.strip()
  riadok = riadok.split(" ")
  arrayRiadok = riadok
  #str to int
  for i in range(len(arrayRiadok)):
    arrayRiadok[i] = int(arrayRiadok[i])

  riadokNaProgress += 1
  if (riadokNaProgress == patpercent):
    progress += 5
    print(progress,"%")
    riadokNaProgress = 0
#najdi gausa (hopefully)
  x = np.linspace(0, MAX_TOT, MAX_TOT)
  y = np.array(arrayRiadok)


  fitter = modeling.fitting.LevMarLSQFitter()
  model = modeling.models.Gaussian1D()   # depending on the data you need to give some initial values
  fitted_model = fitter(model, x, arrayRiadok)

  outputFile.write("3 ")
  outputFile.write(str(round(fitted_model.parameters[0], 2)))
  outputFile.write(" ")
  outputFile.write(str(round((fitted_model.parameters[1]), 2)))
  outputFile.write(" ")
  outputFile.write(str(round((fitted_model.parameters[2]), 2)))
  outputFile.write(" ")
  for data in arrayRiadok:
    outputFile.write(str(data))
    outputFile.write(" ")
  outputFile.write("\n")


file.close()
outputFile.close()

print("end")
