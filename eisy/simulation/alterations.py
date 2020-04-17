import math
import numpy as np
# import pandas as pd
import random
from scipy.special import erfinv


def imag_noise(dataframe, noisescale=0.4):
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


def random_imag_noise(dataframe, noisescale=0.4):
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
    return dataframe


def freq_noise(dataframe, noisescale=0.4):
    '''Returns a dataframe with noise'''
    fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

    f_noise = []
    w_noise = []
    for i in range(dataframe.shape[0]):
        rd_number = random.choice(fibonacci)
        if rd_number % 2 == 0:
            f_noise.append(dataframe['freq [Hz]'][i] + noisescale *
                           (dataframe['freq [Hz]'][i]) *
                           math.cos(dataframe['freq [Hz]'][i]))
            w_noise.append(dataframe['angular_freq [1/s]'][i] + noisescale *
                           (dataframe['angular_freq [1/s]'][i]) *
                           math.cos(dataframe['angular_freq [1/s]'][i]))
        else:
            f_noise.append(dataframe['freq [Hz]'][i] + noisescale *
                           (dataframe['freq [Hz]'][i]) *
                           math.sin(dataframe['freq [Hz]'][i]))
            w_noise.append(dataframe['angular_freq [1/s]'][i] + noisescale *
                           (dataframe['angular_freq [1/s]'][i]) *
                           math.sin(dataframe['angular_freq [1/s]'][i]))

    dataframe['freq_noise [Hz]'] = f_noise
    dataframe['angular_freq_noise [1/s]'] = w_noise
    # need to add few lines here
    return dataframe


def real_noise(dataframe, noisescale=0.4):
    '''Returns a dataframe with noise'''
    fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

    x_noise = []
    for i in range(dataframe.shape[0]):
        rd_number = random.choice(fibonacci)
        if rd_number % 2 == 0:
            x_noise.append(dataframe['Re_Z [ohm]'][i] + noisescale *
                           (dataframe['Re_Z [ohm]'][i]) *
                           math.cos(dataframe['Re_Z [ohm]'][i]))
        else:
            x_noise.append(dataframe['Re_Z [ohm]'][i] + noisescale *
                           (dataframe['Re_Z [ohm]'][i]) *
                           math.sin(dataframe['Re_Z [ohm]'][i]))

    dataframe['Re_Z_noise [ohm]'] = x_noise
    return dataframe


def complex_noise(dataframe, noisescale=0.4):
    '''Returns a dataframe with random noise in the real adn imaginary
       part of the impedance'''
    dataframe_y = imag_noise(dataframe, noisescale)
    dataframe = real_noise(dataframe_y, noisescale)
    return dataframe


def current_noise(dataframe, voltage_amplitude, amplitude):
    '''Returns a dataframe with random noise in the real adn imaginary +
       part of the impedance'''

    current = voltage_amplitude/dataframe['complex_Z [ohm]']
    noise = []
    real = []
    imag = []
    current_noise = []
    for i in range(len(current)):
        rdm1 = random.random()
        noise.append(np.sqrt(2)*amplitude*erfinv(2*rdm1-1))
        rdm2 = random.random()
        real.append(current.to_numpy().real[i]+noise[i]*np.cos(rdm2*2*np.pi))
        imag.append(current.to_numpy().imag[i]+noise[i]*np.sin(rdm2*2*np.pi))
        current_noise.append(real[i]+1j*imag[i])

    complex_impedance = voltage_amplitude/np.array(current_noise)
    dataframe['Re_Z_noise [ohm]'] = complex_impedance.real
    dataframe['Im_Z_noise [ohm]'] = complex_impedance.imag
    return dataframe


def voltage_noise(dataframe, voltage_amplitude, amplitude):
    '''Returns a dataframe with random noise in the real adn imaginary +
       part of the impedance'''

    current = voltage_amplitude/dataframe['complex_Z [ohm]']
    noise = []
    voltage_noise = []
    for i in range(len(current)):
        rdm1 = random.random()
        noise.append(np.sqrt(2)*amplitude*erfinv(2*rdm1-1))
        voltage_noise.append(voltage_amplitude+noise[i])

    complex_impedance = voltage_noise/current
    dataframe['Re_Z_noise [ohm]'] = complex_impedance.to_numpy().real
    dataframe['Im_Z_noise [ohm]'] = complex_impedance.to_numpy().imag
    return dataframe


def iv_noise(dataframe, voltage_amplitude, amplitude):
    '''Returns a dataframe with random noise in the real adn imaginary +
       part of the impedance'''

    current = voltage_amplitude/dataframe['complex_Z [ohm]']
    noise = []
    real = []
    imag = []
    current_noise = []
    voltage_noise = []
    for i in range(len(current)):
        rdm1 = random.random()
        noise.append(np.sqrt(2)*amplitude*erfinv(2*rdm1-1))
        voltage_noise.append(voltage_amplitude+noise[i])
        rdm2 = random.random()
        real.append(current.to_numpy().real[i]+noise[i]*np.cos(rdm2*2*np.pi))
        imag.append(current.to_numpy().imag[i]+noise[i]*np.sin(rdm2*2*np.pi))
        current_noise.append(real[i]+1j*imag[i])

    complex_impedance = voltage_noise/np.array(current_noise)
    dataframe['Re_Z_noise [ohm]'] = complex_impedance.real
    dataframe['Im_Z_noise [ohm]'] = complex_impedance.imag
    return dataframe


def normalize(impedance_array):
    '''Function that returns a normalized impedance_array

    The function takes the maximum value of an array and divides each entry of
    the array by it. Additionally, if the minimum of the array is negative, it
    shifts it to zero, so that the resulting normalized array will have a range
    zero to one.

    Parameters
    ----------

    impedance_array : array
                      the array to be normalized.

    Returns
    -------

    normalized_impedance_array :  array
                                  the normalized array. This should have range
                                  zero to one.
    '''

    if min(impedance_array) < 0:
        impedance_array += abs(min(impedance_array))
    if max(impedance_array) > 1:
        normalized_impedance_array = impedance_array/max(impedance_array)

    return normalized_impedance_array
