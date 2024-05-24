import numpy as np
from scipy.optimize import curve_fit
import concurrent.futures

from custom_function import custom_function
from globals import RESOLUTION, THRESHOLD

# Inicializácia premenných a polí
riadokCislo = 0
arrayA = [0] * (RESOLUTION * RESOLUTION)  # Pole pre hodnoty parametra A
arrayB = [0] * (RESOLUTION * RESOLUTION)  # Pole pre hodnoty parametra B
arrayC = [0] * (RESOLUTION * RESOLUTION)  # Pole pre hodnoty parametra C
arrayT = [0] * (RESOLUTION * RESOLUTION)  # Pole pre hodnoty parametra T
x_data = []  # Pole pre hodnoty x, ktoré sa budú používať pri fitovaní

def calibLine(riadok):
    # Definovanie funkcie na kalibráciu jedného riadku
    global riadokCislo  # Globálna premenná pre sledovanie aktuálneho riadku
    tentoRiadokCislo = riadokCislo  # Uloženie aktuálneho čísla riadku
    riadokCislo += 1  # Zvýšenie čísla riadku pre ďalšie volanie funkcie
    global arrayA, arrayB, arrayC, arrayT, x_data  # Použitie globálnych polí a dát

    if (tentoRiadokCislo % RESOLUTION) == 0:
        # Ak je aktuálny riadok násobkom RESOLUTION, vypíše sa progres
        print(round(tentoRiadokCislo / RESOLUTION / RESOLUTION * 100, 1), "%")
    
    riadok.insert(0, 0)  # Pridanie 0 na začiatok riadku
    y_data = np.array(riadok)  # Konvertovanie riadku na numpy pole

    # Fitovanie dát na základe custom_function a ukladanie parametrov do príslušných polí
    params, _ = curve_fit(custom_function, x_data, y_data, maxfev=1000000, bounds=([0, -np.inf, -np.inf, 0], [np.inf, np.inf, np.inf, THRESHOLD]))
    arrayA[tentoRiadokCislo] = params[0]
    arrayB[tentoRiadokCislo] = params[1]
    arrayC[tentoRiadokCislo] = params[2]
    arrayT[tentoRiadokCislo] = params[3]

def zapisCalibDoSuboru(priecinok):
    # Definovanie funkcie pre zápis kalibračných dát do súborov
    print("zapis do suborov")
    print(len(arrayA))  # Výpis počtu prvkov v arrayA
    riadokCislo = 0  # Inicializácia počítadla riadkov

    # Otvorenie štyroch súborov pre zápis
    with open(priecinok + "/calib_a.txt", "w") as filea, open(priecinok + "/calib_b.txt", "w") as fileb, \
         open(priecinok + "/calib_c.txt", "w") as filec, open(priecinok + "/calib_t.txt", "w") as filet:

        for i in range(len(arrayA)):
            riadokCislo += 1  # Zvýšenie počítadla riadkov
            # Zápis zaokrúhlených hodnôt do súborov
            filea.write(str(round(arrayA[i], 4)) + " ")
            fileb.write(str(round(arrayB[i], 4)) + " ")
            filec.write(str(round(arrayC[i], 4)) + " ")
            filet.write(str(round(arrayT[i], 4)) + " ")

            if riadokCislo == RESOLUTION:
                # Ak je počet riadkov rovný RESOLUTION, pridá nový riadok do súboru
                riadokCislo = 0
                filea.write("\n")
                fileb.write("\n")
                filec.write("\n")
                filet.write("\n")
  
def multithreadingFitting(casy, x_dataVstup, vystupnySuborCesta):
  # Definovanie funkcie pre paralelné fitovanie viacerých riadkov
  global x_data  # Použitie globálnej premenná x_data
  x_data = x_dataVstup  # Nastavenie vstupných dát pre x

  # Použitie ThreadPoolExecutor pre paralelné spracovanie riadkov
  with concurrent.futures.ThreadPoolExecutor() as executor:
      executor.map(calibLine, casy)  # Mapovanie funkcie calibLine na každý riadok v casy

  zapisCalibDoSuboru(vystupnySuborCesta)  # Zavolanie funkcie pre zápis výsledkov do súborov