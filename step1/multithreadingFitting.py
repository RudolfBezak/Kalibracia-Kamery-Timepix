import numpy as np
from scipy.optimize import curve_fit
import concurrent.futures

from custom_function import custom_function
from globals import RESOLUTION, TRESHOLD

inputFile = "am4peaks.rudolf"
outputFilea = "calib_a.txt"
outputFileb = "calib_b.txt"
outputFilec = "calib_c.txt"
outputFilet = "calib_t.txt"

def calibLine(riadok):
    global riadokCislo
    tentoRiadokCislo = riadokCislo
    riadokCislo += 1
    global window
    global percenta
    global arrayA
    global arrayB
    global arrayC
    global arrayT
    global x_data
    if ((tentoRiadokCislo % RESOLUTION) == 0):
        print(tentoRiadokCislo / RESOLUTION / RESOLUTION * 100, "%")
        window.file_text2.config(text = str(round(tentoRiadokCislo / RESOLUTION / RESOLUTION * 100)) + "%")
        window.update_idletasks()
    
    riadok.insert(0, 0)
    y_data = np.array(riadok)
    params, _ = curve_fit(custom_function, x_data, y_data, maxfev=1000000, bounds=([0, -np.inf, -np.inf, 0], [np.inf, np.inf, np.inf, TRESHOLD]))
    arrayA[tentoRiadokCislo] = params[0]
    arrayB[tentoRiadokCislo] = params[1]
    arrayC[tentoRiadokCislo] = params[2]
    arrayT[tentoRiadokCislo] = params[3]

# Main execution
riadokCislo = 0
percenta = 0
arrayA = [0] * (RESOLUTION*RESOLUTION)
arrayB = [0] * (RESOLUTION*RESOLUTION)
arrayC = [0] * (RESOLUTION*RESOLUTION)
arrayT = [0] * (RESOLUTION*RESOLUTION)
x_data = []
window = None

def multithreadingFitting(casy, x_dataVstup, vystupnySuborCesta, windowApp):
    global x_data
    x_data = x_dataVstup
    global window
    window = windowApp
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
          executor.map(calibLine, casy)

    zapisCalibDoSuboru(vystupnySuborCesta)


def zapisCalibDoSuboru(priecinok):
    print("zapis do suborov")
    print(len(arrayA))
    riadokCislo = 0
    with open(priecinok + "/calib_a.txt", "w") as filea, open(priecinok + "/calib_b.txt", "w") as fileb, \
        open(priecinok + "/calib_c.txt", "w") as filec, open(priecinok + "/calib_t.txt", "w") as filet:
        for i in range(len(arrayA)):
            riadokCislo += 1

            filea.write(str(arrayA[i]) + " ")
            fileb.write(str(arrayB[i]) + " ")
            filec.write(str(arrayC[i]) + " ")
            filet.write(str(arrayT[i]) + " ")
            
            if(riadokCislo == RESOLUTION):
                riadokCislo = 0
                filea.write("\n")
                fileb.write("\n")
                filec.write("\n")
                filet.write("\n")