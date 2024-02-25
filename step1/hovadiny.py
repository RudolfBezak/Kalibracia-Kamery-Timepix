import numpy as np
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

def fit_and_plot_gaussians(data):
    # fit the data to a Gaussian mixture model with 3 components
    data = np.array(data)
    gmm = GaussianMixture(n_components=4)
    gmm.fit(data.reshape(-1, 1))
    means = gmm.means_.ravel()
    stds = np.sqrt(gmm.covariances_).ravel()
    weights = gmm.weights_
    
    # plot the original data as a line plot
    plt.plot(data, label='Original Data')
    x = np.linspace(np.min(data), np.max(data), 1000)
    for mean, std, weight in zip(means, stds, weights):
        plt.plot(x, weight*np.exp(-(x - mean)**2 / (2*std**2)), label='Mean: {:.2f} Std: {:.2f}'.format(mean, std))
    plt.legend()
    plt.show()
    
data = [7, 16, 21, 24, 34, 50, 57, 68, 76, 97, 117, 130, 140, 174, 241, 270, 284, 317, 281, 304, 359, 445, 465, 426, 359, 242, 298, 303, 279, 214, 165, 119, 93, 78, 56, 40, 33, 24, 20, 25, 10, 15, 17, 15, 17, 16, 13, 22, 20, 17, 23, 18, 18, 21, 21, 24, 27, 25, 25, 24, 20, 19, 26, 27, 34, 24, 37, 47, 42, 53, 49, 30, 14, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fit_and_plot_gaussians(data)
