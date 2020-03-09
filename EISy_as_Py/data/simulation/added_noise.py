import math
import pandas as pd
import numpy as np


def added_noise(dataframe, noisescale=0.4):
    '''Returns a dataframe with noise'''
    fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    rd_number = random.choice(fibonacci)
    print(rd_number)
    y_noise = []
    for i in range(dataframe.shape[0]):
        if rd_number % 2 == 0:
            y_noise.append(dataframe['Im_Z [ohm]'][i] + noisescale *
                           (dataframe['Im_Z [ohm]'][i]) *
                           math.cos(dataframe['Im_Z [ohm]'][i]))
        else:
            y_noise.append(dataframe['Im_Z [ohm]'][i] + noisescale *
                           (dataframe['Im_Z [ohm]'][i]) *
                           math.sin(dataframe['Im_Z [ohm]'][i]))

    dataframe['Im_Z_noise'] = y_noise
    return dataframe


def noise_to_dataframe(dataframe, noisescale=0.4, )
