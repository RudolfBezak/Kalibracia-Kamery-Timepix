import matplotlib.pyplot as plt
import numpy as np
from astropy import modeling

from globals import MAX_TOT

# inputFile = f"summedCalibrationData2.rudolf"
inputFile = f"calibrationData.rudolf"
# inputFile = f"summedMovedDataWithGauss2.rudolf"
# inputFile = f"testData.rudolf"

riadokNaVypis = int(input("ktory riadok: "))

arrayRiadok = 0
riadokCislo = 0
pocetHodnot = 0

file = open(inputFile, 'r', encoding='utf-8')
for riadok in file:
  riadokCislo += 1
  if (riadokCislo == riadokNaVypis):
    riadok = riadok.strip()
    riadok = riadok.split(" ")
    arrayRiadok = riadok
    pocetHodnot = len(arrayRiadok)
    break

file.close()

print(arrayRiadok)
for i in range(len(arrayRiadok)):
  arrayRiadok[i] = int(arrayRiadok[i])


x = np.linspace(0, pocetHodnot, pocetHodnot)
y = np.array(arrayRiadok)


fitter = modeling.fitting.LevMarLSQFitter()
model = modeling.models.Gaussian1D()   # do zatvorky (amplitude, mean, stddev) https://docs.astropy.org/en/stable/modeling/fitting.html
fitted_model = fitter(model, x, arrayRiadok)
print("výška", fitted_model.parameters[0])
print("stred", fitted_model.parameters[1])
print("tretia hodnota", fitted_model.parameters[2])
print(fitted_model)

plt.title("Line graph")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.plot(x, y, color ="red")
plt.plot(x, fitted_model(x))
plt.show()