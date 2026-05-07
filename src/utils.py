import numpy as np

def normalize(x):
    return (x - np.mean(x)) / np.std(x)