import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# inputFile = f"am4peaks.rudolf"
# outputFilea = f"calib_a.txt"
# outputFileb = f"calib_b.txt"
# outputFilec = f"calib_c.txt"
# outputFilet = f"calib_t.txt"

x_data = np.array([ 17.7, 20.7, 26.3, 59.5])

# Define the function
def custom_function(x, a, b, c, t):
    return (a * x) + b - (c / (x - t))

# Given data points
# file = open(inputFile, 'r', encoding='utf-8')
# filea = open(outputFilea, 'w', encoding='utf-8')
# fileb = open(outputFileb, 'w', encoding='utf-8')
# filec = open(outputFilec, 'w', encoding='utf-8')
# filet = open(outputFilet, 'w', encoding='utf-8')

# riadokCislo=0
# percenta = 0

# for riadok in file:
#     riadokCislo += 1
#     riadok = riadok.strip()
#     riadok = riadok.split(" ")
#     print(riadokCislo)
#     for i in range(len(riadok)):
#         riadok[i] = int(riadok[i])
#     y_data = np.array(riadok)
#     params, _ = curve_fit(custom_function, x_data, y_data, maxfev=1000000)
#     filea.write(str(params[0]) + " ")
#     fileb.write(str(params[1]) + " ")
#     filec.write(str(params[2]) + " ")
#     filet.write(str(params[3]) + " ")
#     if (riadokCislo == 256):
#         riadokCislo = 0
#         percenta = percenta + 0.4
#         print(percenta,"%")
#         filea.write("\n")
#         fileb.write("\n")
#         filec.write("\n")
#         filet.write("\n")

# file.close()
# filea.close()
# fileb.close()
# filec.close()
# filet.close()


x_data = np.array([6, 17.7, 20.7, 26.3, 59.5]) #17.7, 20.7, 26.3, 59.5 / 13.8, 17.7, 20.7, 59.5
y_data = np.array([0, 19, 230, 28, 67]) # 19, 230, 28, 67 /

# Fit the function to the data
params, _ = curve_fit(custom_function, x_data, y_data, maxfev=1000000, bounds=([-np.inf, -np.inf, -np.inf, 0], [np.inf, np.inf, np.inf, 6]))

# Generate points on the fitted curve for smooth plotting
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = custom_function(x_fit, *params)
params = (-2.903282355458918, 8958.744464272246, 18405343.937474344, -2052.4187561429676)
y_fit2 = custom_function(x_fit, *params)
print(params)

# Plot the data points and the fitted curve
plt.plot(x_fit, y_fit2, label='Krivka 1', color='red')

# x_data = np.array([6, 17.7, 20.7, 26.3, 59.5]) #17.7, 20.7, 26.3, 59.5 / 13.8, 17.7, 20.7, 59.5
# y_data = np.array([0, 21, 28, 34, 80]) # 19, 23, 28, 67 / 17, 22, 24, 64

# # Fit the function to the data
# params, _ = curve_fit(custom_function, x_data, y_data, maxfev=1000000, bounds=([-np.inf, -np.inf, -np.inf, 0], [np.inf, np.inf, np.inf, 6]))

# # Generate points on the fitted curve for smooth plotting
# x_fit = np.linspace(min(x_data), max(x_data), 100)
# y_fit = custom_function(x_fit, *params)
# params = (0, 0, 0, 4.050051)
# # y_fit2 = custom_function(x_fit, *params)
# print(params)

# Plot the data points and the fitted curve
# plt.plot(x_fit, y_fit, label='Krivka 2', color='blue')

# x_data = np.array([6, 13.8, 17.7, 20.7, 59.5]) #17.7, 20.7, 26.3, 59.5 / 13.8, 17.7, 20.7, 59.5
# y_data = np.array([0, 17, 22, 27, 64,]) # 19, 23, 28, 67 /

# # Fit the function to the data
# params, _ = curve_fit(custom_function, x_data, y_data, maxfev=1000000, bounds=([-np.inf, -np.inf, -np.inf, 2], [np.inf, np.inf, np.inf, 6]))

# # Generate points on the fitted curve for smooth plotting
# x_fit = np.linspace(min(x_data), max(x_data), 100)
# y_fit = custom_function(x_fit, *params)
# # params = (0.922772, 11.90094, 34.002393, 4.050051)
# # y_fit2 = custom_function(x_fit, *params)
# print(params)

# # Plot the data points and the fitted curve
# plt.plot(x_fit, y_fit, label='Krivka 3', color='purple')

# x_data = np.array([6, 13.8, 17.7, 20.7, 59.5]) #17.7, 20.7, 26.3, 59.5 / 13.8, 17.7, 20.7, 59.5
# y_data = np.array([0, 18, 24, 28, 74]) # 19, 23, 28, 67 /

# # Fit the function to the data
# params, _ = curve_fit(custom_function, x_data, y_data, maxfev=1000000, bounds=([-np.inf, -np.inf, -np.inf, 0], [np.inf, np.inf, np.inf, 6]))

# # Generate points on the fitted curve for smooth plotting
# x_fit = np.linspace(min(x_data), max(x_data), 100)
# y_fit = custom_function(x_fit, *params)
# # params = (0.922772, 11.90094, 34.002393, 4.050051)
# # y_fit2 = custom_function(x_fit, *params)
# print(params)

# Plot the data points and the fitted curve
# plt.plot(x_fit, y_fit, label='Krivka 4', color='green')

# plt.scatter(x_data, y_data, label='Data Points')
plt.xlabel('Energia (KeV)')
plt.ylabel('ToT (ADU)')
plt.legend()
plt.show()