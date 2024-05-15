import matplotlib.pyplot as plt
import numpy as np

from globals import MAX_TOT

from custom_function import custom_function
from custom_function import custom_function2

# pri 15 to ide

inputFile = f"calibrationData.rudolf"
caliba = f"calib_a.txt"
calibb = f"calib_b.txt"
calibc = f"calib_c.txt"
calibt = f"calib_t.txt"

arraySpocitany = 0

riadokNaVypis = int(input("ktory riadok: "))

file = open(inputFile, 'r', encoding='utf-8')
filea = open(caliba, 'r', encoding='utf-8')
fileb = open(calibb, 'r', encoding='utf-8')
filec = open(calibc, 'r', encoding='utf-8')
filet = open(calibt, 'r', encoding='utf-8')

riadokCislo=0
for riadok in filea:
    if (int(riadokCislo) == (riadokNaVypis // 256)):
        riadok = riadok.strip()
        riadok = riadok.split(" ")

        aValue = riadok[(riadokNaVypis-1) % 256]
    riadokCislo += 1

riadokCislo=0
for riadok in fileb:
    if (riadokCislo == (riadokNaVypis // 256)):
        riadok = riadok.strip()
        riadok = riadok.split(" ")
        bValue = riadok[(riadokNaVypis-1) % 256]
    riadokCislo += 1

riadokCislo=0
for riadok in filec:
    if (riadokCislo == (riadokNaVypis // 256)):
        riadok = riadok.strip()
        riadok = riadok.split(" ")
        cValue = riadok[(riadokNaVypis-1) % 256]
    riadokCislo += 1

riadokCislo=0
for riadok in filet:
    if (riadokCislo == (riadokNaVypis // 256)):
        riadok = riadok.strip()
        riadok = riadok.split(" ")
        tValue = riadok[(riadokNaVypis-1) % 256]
    riadokCislo += 1

arrayx = [0] * MAX_TOT

#premen data na kalibrovanie pomocou inverznej kalibracnej funkcie
print(aValue, bValue, cValue, tValue)
for i in range(len(arrayx)):
    arrayx[i] = custom_function2(i+1, float(aValue), float(bValue), float(cValue), float(tValue))

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


x = np.array(arrayx)
y = np.array(arraySpocitany)
x2 = np.arange(1, MAX_TOT+1)
plt.title("Spektrum 26. pixela")
plt.xlabel("Energia [KeV] resp. ToT [ADU]")
plt.ylabel("Početnosť")
plt.plot(x, y, color ="blue", label="Kalibrované [KeV]")
plt.plot(x2, y, color ="red", label="Nekalibrované ToT [ADU]")
plt.legend()
plt.show()
