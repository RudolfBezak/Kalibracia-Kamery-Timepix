import matplotlib.pyplot as plt
import numpy as np

from globals import MAX_TOT

inputFile = f"summedCalibrationData.rudolf"

arraySpocitany = 0

file = open(inputFile, 'r', encoding='utf-8')
for riadok in file:
  riadok = riadok.strip()
  riadok = riadok.split(" ")
  arraySpocitany = riadok

file.close()

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
