import math
import numpy as np
import random
from scipy.special import erfinv


def freq_noise(dataframe, noise_amplitude=0.4):
    '''Returns a dataframe with noise added to the frequency'''
    fibonacci = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]

    f_noise = []
    w_noise = []
    for i in range(dataframe.shape[0]):
        rd_number = random.choice(fibonacci)
        if rd_number % 2 == 0:
            f_noise.append(dataframe['freq [Hz]'][i] + noise_amplitude *
                           (dataframe['freq [Hz]'][i]) *
                           math.cos(dataframe['freq [Hz]'][i]))
            w_noise.append(dataframe['angular_freq [1/s]'][i] +
                           noise_amplitude *
                           (dataframe['angular_freq [1/s]'][i]) *
                           math.cos(dataframe['angular_freq [1/s]'][i]))
        else:
            f_noise.append(dataframe['freq [Hz]'][i] + noise_amplitude *
                           (dataframe['freq [Hz]'][i]) *
                           math.sin(dataframe['freq [Hz]'][i]))
            w_noise.append(dataframe['angular_freq [1/s]'][i] +
                           noise_amplitude *
                           (dataframe['angular_freq [1/s]'][i]) *
                           math.sin(dataframe['angular_freq [1/s]'][i]))

    dataframe['freq_noise [Hz]'] = f_noise
    dataframe['angular_freq_noise [1/s]'] = w_noise
    # need to add few lines here
    return dataframe


def complex_noise(dataframe, noise_amplitude):
    '''
    Function that returns a dataframe with noise added to the real and
    imaginary parts of the impedance

    Parameters
    ----------
    dataframe: pandas.DataFrame
               A pandas dataframe containing the dataset to modify with noise
    noise_amplitude: float
                      A number between 0 and 1 representing the percentage of
                      the signal to use when scaling the amplitude of the noise

    Returns
    -------
    dataframe: pandas.DataFrame
               A pandas dataframe containing the dataset with added colomns
               containing the modified signal
    '''

    # noisescale = noise_scaling(noise_amplitude, 'complex_noise', dataframe)
    noisescale = noise_amplitude * dataframe['Re_Z [ohm]'].iloc[-1]
    noise = []
    real_noisy = []
    imag_noisy = []
    for i in range(len(dataframe.index)):
        rdm1 = random.random()
        noise.append(np.sqrt(2)*noisescale*erfinv(2*rdm1-1))
        rdm2 = random.random()
        real_noise = noise[i] * np.cos(rdm2*2*np.pi)
        imag_noise = noise[i] * np.sin(rdm2*2*np.pi)
        real_noisy.append(dataframe['Re_Z [ohm]'][i] + real_noise)
        imag_noisy.append(dataframe['Im_Z [ohm]'][i] + imag_noise)

    dataframe['Re_Z_noise [ohm]'] = real_noisy
    dataframe['Im_Z_noise [ohm]'] = imag_noisy
    return dataframe


def current_noise(dataframe, noise_amplitude, voltage_amplitude=0.01):
    '''
    Function that returns a dataframe with noise added to current output signal

    Parameters
    ----------
    dataframe: pandas.DataFrame
               A pandas dataframe containing the dataset to modify with noise
    noise_amplitude: float
                      A number between 0 and 1 representing the percentage of
                      the signal to use when scaling the amplitude of the noise
    voltage_amplitude: float
                       The amplitude of the voltage input signal expressed
                       in [V]
    Returns
    -------
    dataframe: pandas.DataFrame
               A pandas dataframe containing the dataset with added colomns
               containing the modified signal
    '''
    current = voltage_amplitude/dataframe['complex_Z [ohm]']
    noisescale = noise_amplitude * current.iloc[0].real
    noise = []
    real = []
    imag = []
    current_noise = []
    for i in range(len(current)):
        rdm1 = random.random()
        noise.append(np.sqrt(2)*noisescale*erfinv(2*rdm1-1))
        rdm2 = random.random()
        real_noise = noise[i] * np.cos(rdm2*2*np.pi)
        imag_noise = noise[i] * np.sin(rdm2*2*np.pi)
        real.append(current.to_numpy().real[i] + real_noise)
        imag.append(current.to_numpy().imag[i] + imag_noise)
        current_noise.append(real[i]+1j*imag[i])

    complex_impedance = voltage_amplitude/np.array(current_noise)
    dataframe['Re_Z_noise [ohm]'] = complex_impedance.real
    dataframe['Im_Z_noise [ohm]'] = complex_impedance.imag
    return dataframe


def voltage_noise(dataframe, noise_amplitude, current_amplitude=0.01):
    '''
    Function that returns a dataframe with noise added to voltage output signal

    Parameters
    ----------
    dataframe: pandas.DataFrame
               A pandas dataframe containing the dataset to modify with noise
    noise_amplitude: float
                      A number between 0 and 1 representing the percentage of
                      the signal to use when scaling the amplitude of the noise
    current_amplitude: float
                       The amplitude of the current input signal expressed
                       in [A]
    Returns
    -------
    dataframe: pandas.DataFrame
               A pandas dataframe containing the dataset with added colomns
               containing the modified signal
    '''

    voltage = current_amplitude*dataframe['complex_Z [ohm]']
    noisescale = noise_amplitude * voltage.iloc[-1].real
    imag = []
    real = []
    noise = []
    voltage_noise = []
    for i in range(len(voltage)):
        rdm1 = random.random()
        noise.append(np.sqrt(2)*noisescale*erfinv(2*rdm1-1))
        rdm2 = random.random()
        real_noise = noise[i] * np.cos(rdm2*2*np.pi)
        imag_noise = noise[i] * np.sin(rdm2*2*np.pi)
        real.append(voltage.to_numpy().real[i] + real_noise)
        imag.append(voltage.to_numpy().imag[i] + imag_noise)
        voltage_noise.append(real[i]+1j*imag[i])

    complex_impedance = np.array(voltage_noise)/current_amplitude
    dataframe['Re_Z_noise [ohm]'] = complex_impedance.real
    dataframe['Im_Z_noise [ohm]'] = complex_impedance.imag
    return dataframe


def outliers(dataframe, percentage_outliers, outliers_amplitude):
    '''Function that randomly creates outliers in the impedance response

    The function will modify a percentage of the data to be outliers, with
    an amplitude defined by the user. The number of points to be modified
    can also be modified by the user.

    Parameters
    ----------
    dataframe: pandas.DataFrame
               A pandas dataframe containing the dataset to modify with noise

    percentage_outliers : float
                          A number between 0 and 1 indicating the percentge
                          of points to modify as outliers
    outliers_amplitude : float or int
                         A number indicating the percentge of
                         the signal the outliers will be scaled by.
    Returns
    -------
    dataframe: pandas.DataFrame
               A pandas dataframe containing the dataset with added colomns
               containing the modified signal
    '''
    complex_response = dataframe['complex_Z [ohm]'].copy()
    for i in range(len(complex_response)):
        rdm = random.random()
        complex_response[i] = complex_response[i] + \
            (random.choice([-1, 1]) * dataframe['Re_Z [ohm]'].iloc[-1] *
             outliers_amplitude * (2*rdm-1) * np.exp(1j*rdm*2*np.pi) *
             (1 if rdm < outliers else 0))

    dataframe['Re_Z_noise [ohm]'] = complex_response.to_numpy().real
    dataframe['Im_Z_noise [ohm]'] = complex_response.to_numpy().imag

    return dataframe


def normalize(impedance_array):
    '''Function that returns a normalized impedance_array

    The function takes the maximum value of an array and divides each entry of
    the array by it. Additionally, if the minimum of the array is negative, it
    shifts it to zero, so that the resulting normalized array will have a range
    zero to one.

    Parameters
    ----------
    impedance_array : array-like
                      the array to be normalized.

    Returns
    -------
    normalized_impedance_array :  array-like
                                  the normalized array. All entries in this
                                  array should be values in the range
                                  zero to one.
    '''
    temp_array = impedance_array.copy()
    if np.amin(temp_array, axis=0) < 0:
        temp_array += abs(np.amin(temp_array, axis=0))
    if np.amax(temp_array, axis=0) > 1:
        normalized_impedance_array = temp_array/np.amax(temp_array, axis=0)
    else:
        normalized_impedance_array = temp_array

    return normalized_impedance_array
