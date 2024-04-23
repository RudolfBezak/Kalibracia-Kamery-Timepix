import matplotlib.pyplot as plt

# Example arrays
x_values = [1, 2, 5.5, 4, 5]
y_values = [2, 4, 10, 8, 10]

# Plotting
plt.plot(x_values, y_values)
plt.xlabel('X values')
plt.ylabel('Y values')
plt.title('Plot of X and Y values')
plt.grid(True)
plt.show()
