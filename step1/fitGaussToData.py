import matplotlib.pyplot as plt
import numpy as np
from astropy import modeling

from globals import MAX_TOT

# inputFile = f"summedCalibrationData.rudolf"
inputFile = f"calibrationData.rudolf"

riadokNaVypis = int(input("ktory riadok: "))

arraySpocitany = 0
riadokCislo = 0

file = open(inputFile, 'r', encoding='utf-8')
for riadok in file:
  riadokCislo += 1
  if (riadokCislo == riadokNaVypis):
    riadok = riadok.strip()
    riadok = riadok.split(" ")
    arraySpocitany = riadok

print(arraySpocitany)
for i in range(len(arraySpocitany)):
  arraySpocitany[i] = int(arraySpocitany[i])


x = np.linspace(0, MAX_TOT, MAX_TOT)
y = np.array(arraySpocitany)


fitter = modeling.fitting.LevMarLSQFitter()
model = modeling.models.Gaussian1D()   # depending on the data you need to give some initial values
fitted_model = fitter(model, x, arraySpocitany)
print("výška", fitted_model.parameters[0])
print("stred", fitted_model.parameters[1])
print("tretia picovina", fitted_model.parameters[2])

plt.title("Line graph")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.plot(x, y, color ="red")
plt.plot(x, fitted_model(x))
plt.show()