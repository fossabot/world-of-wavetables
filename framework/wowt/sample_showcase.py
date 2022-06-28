from librosa import display
import numpy as np
from matplotlib import pyplot

def visualize_signal(samples: np.ndarray):
    display.waveshow(samples)
    pyplot.show()