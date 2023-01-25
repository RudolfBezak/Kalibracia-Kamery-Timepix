import numpy as np
from scipy.optimize import curve_fit

import numpy as np
from scipy.optimize import curve_fit

def gauss(x, a, mu, sigma):
    return a*np.exp(-(x-mu)**2/(2*sigma**2))

def process_file(input_file, output_file):
    print("start")
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            data = [float(x) for x in line.split()]
            x = np.linspace(0, len(data), len(data))
            try:
                popt, _ = curve_fit(gauss, x, data)
                f_out.write(str(popt[1]) + '\n')
            except Exception as e:
                f_out.write("0" + '\n')
                continue
    print("end")

process_file("calibrationData.rudolf", "indGauss.rudolf")