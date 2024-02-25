import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Define the function
def custom_function(x, a, b, c, t):
    return a * x + b - (c / (x - t))

# Given data points
x_data = np.array([ 10.433, 13.8, 17.7, 20.7, 59.5])
y_data = np.array([ 12.6, 19.1, 23.1, 27.1, 61])

# Fit the function to the data
params, _ = curve_fit(custom_function, x_data, y_data, maxfev=1000000)

# Generate points on the fitted curve for smooth plotting
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = custom_function(x_fit, *params)

# print(params)

# Plot the data points and the fitted curve
plt.plot(x_fit, y_fit, label='Custom Function Fit', color='red')
plt.scatter(x_data, y_data, label='Data Points', marker='h', color='green')
plt.xlabel('Energy (KeV)')
plt.ylabel('ToT (ADU)')
plt.legend()
plt.show()