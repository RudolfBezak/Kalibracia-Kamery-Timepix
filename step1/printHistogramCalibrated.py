import matplotlib.pyplot as plt
import numpy as np

from globals import MAX_TOT, RESOLUTION

from custom_function import custom_function2
from sumCalibrationData import sumCalibrationData

# inputFile = f"calibrationData.rudolf"
# caliba = f"calib_a.txt"
# calibb = f"calib_b.txt"
# calibc = f"calib_c.txt"
# calibt = f"calib_t.txt"

def find_max_in_2d_array(array):
    if not array or not array[0]:
        return None  # Return None if the array is empty or has no columns

    max_value = array[0][0]
    for row in array:
        for element in row:
            if element > max_value:
                max_value = element

    return max_value

def printHistogramCalibrated(inputFile, riadokNaVypis, caliba, calibb, calibc, calibt, porovnanie):

  file = open(inputFile, 'r', encoding='utf-8')
  filea = open(caliba, 'r', encoding='utf-8')
  fileb = open(calibb, 'r', encoding='utf-8')
  filec = open(calibc, 'r', encoding='utf-8')
  filet = open(calibt, 'r', encoding='utf-8')

  if (riadokNaVypis == ""):
    #1D pole pre kazdy pixel
    aData = []
    for riadok in filea:
        riadok = riadok.strip()
        riadok = riadok.split(" ")
        for i in range(len(riadok)):
            aData.append(float(riadok[i]))

    bData = []
    for riadok in fileb:
        riadok = riadok.strip()
        riadok = riadok.split(" ")
        for i in range(len(riadok)):
            bData.append(float(riadok[i]))

    cData = []
    for riadok in filec:
        riadok = riadok.strip()
        riadok = riadok.split(" ")
        for i in range(len(riadok)):
            cData.append(float(riadok[i]))

    tData = []
    for riadok in filet:
        riadok = riadok.strip()
        riadok = riadok.split(" ")
        for i in range(len(riadok)):
            tData.append(float(riadok[i]))

    #2d polia pre data a kanaly
    count = []
    channel = []
    i = -1
    for riadok in file:
        i += 1
        #1D pole ktore budem kladat do count a channel
        riadokChannels = []
        riadokData = []
        riadok = riadok.strip()
        riadok = riadok.split(" ")
        for j in range(len(riadok)):
            riadokData.append(int(riadok[j]))
            # print(i, j, aData[i], bData[i], cData[i], tData[i])
            kev = round(custom_function2(j+1, aData[i], bData[i], cData[i], tData[i], i))
            if (kev > MAX_TOT*2):
                riadokChannels.append(1)
                continue
            riadokChannels.append(kev)

        count.append(riadokData)
        channel.append(riadokChannels)

    #vytvor pole pre vysledok
    maxValue = find_max_in_2d_array(channel)
    resultArray = [[0]*maxValue for i in range(RESOLUTION*RESOLUTION)]

    #spocitaj data
    for i in range(len(count)):
        for j in range(len(count[i])):
            if (channel[i][j] < 1):
                continue
            resultArray[i][channel[i][j] - 1] += count[i][j]

    arraySpocitany = sumCalibrationData(resultArray, True)
    arrayx = list(range(1, maxValue + 1))

       
  else:
    riadokNaVypis = int(riadokNaVypis)
    riadokCislo=0
    for riadok in filea:
        if (int(riadokCislo) == (riadokNaVypis // RESOLUTION)):
            riadok = riadok.strip()
            riadok = riadok.split(" ")

            aValue = riadok[(riadokNaVypis-1) % RESOLUTION]
        riadokCislo += 1

    riadokCislo=0
    for riadok in fileb:
        if (riadokCislo == (riadokNaVypis // RESOLUTION)):
            riadok = riadok.strip()
            riadok = riadok.split(" ")
            bValue = riadok[(riadokNaVypis-1) % RESOLUTION]
        riadokCislo += 1

    riadokCislo=0
    for riadok in filec:
        if (riadokCislo == (riadokNaVypis // RESOLUTION)):
            riadok = riadok.strip()
            riadok = riadok.split(" ")
            cValue = riadok[(riadokNaVypis-1) % RESOLUTION]
        riadokCislo += 1

    riadokCislo=0
    for riadok in filet:
        if (riadokCislo == (riadokNaVypis // RESOLUTION)):
            riadok = riadok.strip()
            riadok = riadok.split(" ")
            tValue = riadok[(riadokNaVypis-1) % RESOLUTION]
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
  plt.ylabel("Početnosť")
  plt.plot(x, y, color ="blue", label="Kalibrované [KeV]")
  if (riadokNaVypis == ""):
      plt.title("Spektrum všetkých pixelov")
      y = sumCalibrationData(inputFile)
  else:
      plt.title("Spektrum " + str(riadokNaVypis) + " pixela")
  if (porovnanie): 
      plt.plot(x2, y, color ="red", label="Nekalibrované ToT [ADU]")
      plt.xlabel("Energia [KeV] resp. ToT [ADU]")
  else:
      plt.xlabel("Energia [KeV]")
  plt.legend()
  plt.show()
