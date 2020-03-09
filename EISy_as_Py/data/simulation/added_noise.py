import maths
import pandas as import
import numpy as np


def added_noise(dataframe):
    '''Returns a dataframe with noise'''
    fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    rd_number = random.choice(fibonacci)
    print(rd_number)
    noisescale = 0.4
    y_noise = []
    for i in range(dataframe.shape[0]):
        if rd_number % 2 == 0:
            y_noise.append(dataframe['Im_Z [Ohm]'][i] + noisescale *
                           (dataframe['Im_Z [Ohm]'][i]) *
                           math.cos(dataframe['Im_Z [Ohm]'][i]))
        else:
            y_noise.append(dataframe['Im_Z [Ohm]'][i] + noisescale *
                           (dataframe['Im_Z [Ohm]'][i]) *
                           math.sin(dataframe['Im_Z [Ohm]'][i]))

    dataframe['y_noise'] = y_noise
    return dataframe
