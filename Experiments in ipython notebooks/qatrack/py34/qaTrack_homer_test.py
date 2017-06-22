from scipy.misc import imread
from scipy.ndimage import gaussian_filter
import numpy as np

data = imread(BIN_FILE)   # returns a numpy array
red = data[:,:,0]    # keep only red channel

homer = {
    "max": float(np.max(red)),
    "min": float(np.min(red)),
    "mean": float(np.mean(red))
}    # this is the return value of the script, must specify floats

blurred = gaussian_filter(red, 10)
write_file('blurred_homer.png', blurred)
