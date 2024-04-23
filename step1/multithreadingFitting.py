import numpy as np
from scipy.optimize import curve_fit
import concurrent.futures

inputFile = "am4peaks.rudolf"
outputFilea = "calib_a.txt"
outputFileb = "calib_b.txt"
outputFilec = "calib_c.txt"
outputFilet = "calib_t.txt"

x_data = np.array([6, 17.7, 20.7, 26.3, 59.5])

# Define the function
def custom_function(x, a, b, c, t):
    return a * x + b - (c / (x - t))

def process_line(riadok):
    global riadokCislo
    tentoRiadokCislo = riadokCislo
    global percenta
    global arrayA
    global arrayB
    global arrayC
    global arrayT

    riadokCislo += 1
    riadok = riadok.strip().split(" ")
    if riadokCislo % 256 == 0:
        print(riadokCislo / 256 / 256 * 100, "%")
    for i in range(len(riadok)):
        riadok[i] = int(riadok[i])
    
    riadok.insert(0, 0)
    y_data = np.array(riadok)
    params, _ = curve_fit(custom_function, x_data, y_data, maxfev=1000000, bounds=([-np.inf, -np.inf, -np.inf, 0], [np.inf, np.inf, np.inf, np.inf]))
    arrayA[tentoRiadokCislo] = params[0]
    arrayB[tentoRiadokCislo] = params[1]
    arrayC[tentoRiadokCislo] = params[2]
    arrayT[tentoRiadokCislo] = params[3]

# Main execution
riadokCislo = 0
percenta = 0
arrayA = [0] * (256*256)
arrayB = [0] * (256*256)
arrayC = [0] * (256*256)
arrayT = [0] * (256*256)

with open(inputFile, 'r', encoding='utf-8') as file:
    lines = file.readlines()

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_line, lines)


print("zapis do suborov")
print(len(arrayA))
riadokCislo = 0
with open(outputFilea, "w") as filea, open(outputFileb, "w") as fileb, \
    open(outputFilec, "w") as filec, open(outputFilet, "w") as filet:
    for i in range(len(arrayA)):
        riadokCislo += 1

        filea.write(str(arrayA[i]) + " ")
        fileb.write(str(arrayB[i]) + " ")
        filec.write(str(arrayC[i]) + " ")
        filet.write(str(arrayT[i]) + " ")
        
        if(riadokCislo == 256):
            riadokCislo = 0
            filea.write("\n")
            fileb.write("\n")
            filec.write("\n")
            filet.write("\n")