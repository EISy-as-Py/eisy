import math
import pandas as pd
import numpy as np
import random


def added_noise(dataframe, noisescale=0.4):
    '''Returns a dataframe with noise'''
    fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

    y_noise = []
    for i in range(dataframe.shape[0]):
        rd_number = random.choice(fibonacci)
        if rd_number % 2 == 0:
            y_noise.append(dataframe['Im_Z [ohm]'][i] + noisescale *
                           (dataframe['Im_Z [ohm]'][i]) *
                           math.cos(dataframe['Im_Z [ohm]'][i]))
        else:
            y_noise.append(dataframe['Im_Z [ohm]'][i] + noisescale *
                           (dataframe['Im_Z [ohm]'][i]) *
                           math.sin(dataframe['Im_Z [ohm]'][i]))

    dataframe['Im_Z_noise [ohm]'] = y_noise
    return dataframe


def random_noise(dataframe, noisescale=0.4):
    fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    rd_number = random.choice(fibonacci)
    y_noise = []
    pts = dataframe.shape[0]
    for i in range(pts):
        yactual = dataframe['Im_Z [ohm]'][i]

        y_noise.append(yactual+noisescale*(yactual.max()-yactual.min()
                                           )*np.random.normal(rd_number))

    dataframe['Im_Z_noise [ohm]'] = y_noise
    # dataframe['Re_Z_noise [ohm]'] = y_noise
    return

    def missing_data(dataframe):

        n = dataframe.shape[0]

        return
