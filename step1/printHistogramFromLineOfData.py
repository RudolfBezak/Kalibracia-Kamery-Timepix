import matplotlib.pyplot as plt
import numpy as np

from globals import MAX_TOT

# inputFile = f"calibrationData.rudolf"
# inputFile = f"summedCalibrationData.rudolf"
# inputFile = f"summedMovedDataWithGauss2.rudolf"
inputFile = f"calibrationDataUhladene1.rudolf"

arraySpocitany = 0

riadokNaVypis = int(input("ktory riadok: "))

file = open(inputFile, 'r', encoding='utf-8')

riadokCislo=0

for riadok in file:
  riadokCislo += 1
  if (riadokCislo == riadokNaVypis):
    riadok = riadok.strip()
    riadok = riadok.split(" ")
    arraySpocitany = riadok

print(arraySpocitany)
for i in range(len(arraySpocitany)):
  arraySpocitany[i] = int(arraySpocitany[i])


x = np.arange(1, MAX_TOT+1)
y = np.array(arraySpocitany)

plt.title("Line graph")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.plot(x, y, color ="red")
plt.show()
