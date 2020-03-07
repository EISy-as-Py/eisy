import csv
import os
import time

import numpy as np
import pandas as pd
import circuits

from PyEIS import *
from plotting import nyquist_plot


def to_dataframe(freq_range, impedance_array):
    """
    Gunction that creates a dataframe containing impedance data and the
    frequency range used to determine the impedance respose.

    Parameters
    ----------
    freq_range : array-like
                an array containing the frequency and angular frequency values
                used to determine the corresponding impedance response.
                freq_range[0]- the frequency response [Hz]
                freq_range[1]- the angualr frequncy [1/s]

    Output
    ----------
    impedance_response_df: pandas.DataFrame
                           pandas dataframe containing frequency and imepedance
                           data. Columns are labeled based on the dictionary's
                           keys.
    """
    # Create a dictionary containng the keys and values of data to be
    # converted ina pandas dataframe. The 'keys' will be used as column names.
    impedance_dict = {'freq [Hz]': freq_range[0],
                      'angular_freq [1/s]': freq_range[1],
                      'Re_Z [ohm]': impedance_array[1],
                      'Im_Z [ohm]': impedance_array[2],
                      '|Z| [ohm]': impedance_array[3],
                      'phase_angle [rad]': impedance_array[4]}
    impedance_response_df = pd.DataFrame(impedance_dict)
    return impedance_response_df


def impedance_array(complex_impedance):
    '''
    Function that breaks the complex impedance in its rela and Imaginary
    components. It also calculates the magnitude of the impedance, as well
    as its phase angle.

    Parameters
    ----------
    complez_impedance: array-like
                       the impedance in its complex form [ohm]

    Output
    ----------
    impedance[0] : The complex form of the impedance (input)[ohm]
    impedance[1] : Real part of the impedance [ohm]
    impedance[2] : Imaginary part of the impedance [ohm]
    impedance[3] : Magnitude of the impedance [ohm]
    impedance[4] : Phase angle [rad]

    '''
    # Separate the impedance into its real and imaginary components
    real_Z = complex_impedance.real
    imag_Z = complex_impedance.imag
    # Calcuate the magnitude and phase angle of the impedance
    phase_angle = np.arctan(imag_Z/real_Z)
    total_Z = np.sqrt((real_Z**2) + (imag_Z**2))
    impedance = [complex_impedance, real_Z, imag_Z, total_Z, phase_angle]
    return impedance


def RC_simulation(high_freq, low_freq, decades, resistance, capacitance,
                  circuit_configuration, i):
    """
    Function that takes imputs parameters to simulated the impedance response
    of a circuit composed by a resistor and a capacitor in series over the
    indicated frequency range.

    Parameters
    ----------
    high_freq : single value (int or float)
                initial frequency value (high frequency domain) [Hz]
    high_freq : single value (int or float)
                final frequency value (low frequency domain) [Hz]
    decades : integer
              number of frequency decades to be used as range. Default value
              is set to be 7 [-]
    resistance : single value (int or float)
                 Resistance [Ohm]
    capacitance : single value (int or float)
                  Capacitance [F]
    circuit_configuration :

    i :

    Output
    ----------
    impedance_data_df: pandas.DataFrame
                           pandas dataframe containing frequency and imepedance
                           data.
    """
    # Define the frequency range to be simulated
    freq_range = freq_gen(high_freq, low_freq, decades)
    # Obtain the impedance of the RC circuit
    if circuit_configuration == 'series':
        complex_impedance = circuits.cir_RC_series(freq_range[1], resistance,
                                                   capacitance)
    elif circuit_configuration == 'parallel':
        complex_impedance = circuits.cir_RC_parallel(freq_range[1], resistance,
                                                     capacitance)
    else:
        raise AssertionError('The inputted configuration is not supported')
    impedance_data = impedance_array(complex_impedance)
    impedance_data_df = to_dataframe(freq_range, impedance_data)
    return impedance_data_df


def RC_file_writer(high_freq, low_freq, decades, resistance, capacitance,
                   circuit_configuration, i, alteration=None, save_image=None,
                   save_location='simulation_data/'):
    """
    Parameters
    ----------
    Output
    ----------
    """
    # Save the simulated data in a csv file to be exported in a database
    # the format will be in the form of :
    # yymmdd-serial#_sim_classifier.csv
    date = time.strftime('%y%m%d', time.localtime())
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    while i < 9999:
        number = str(i).zfill(4)
        if alteration:
            filename = str('{}-{}_sim_one-{}'.format(date, number, alteration))
        else:
            filename = str('{}-{}_sim_one'.format(date, number))
        if os.path.exists(save_location + filename + '.csv'):
            i += 1
        else:
            break
    with open(save_location + filename + ".csv", mode='a',
              newline='') as data_file:
        data_file.write('Date:, {}'.format(date)+'\n')
        data_file.write('Serial number:, {}'.format(number)+'\n')
        data_file.write('Data Source:, simulation'+'\n')
        data_file.write('Circuit type:, rc'+'\n')
        data_file.write('Circuit elements:, [R={} ohm C={} F]'.format(R, C) +
                        '\n')
        data_file.write('---'+'\n')
        if circuit_configuration == 'series':
            df = circuits.cir_RC_series(freq_range[1], resistance,
                                        capacitance)
        elif circuit_configuration == 'parallel':
            df = circuits.cir_RC_parallel(freq_range[1], resistance,
                                          capacitance)
        else:
            raise AssertionError('The inputted configuration is not supported')
        df.to_csv(data_file, mode='a')
        data_file.close()
    if save_image:
        plot_nyquist(df, filename, save_image=True)

    return


def randles(f_start, f_stop, decades, Rs, R, n, sigma, Q):
    """
    Parameters
    ----------
    Output
    ----------
    """
    # Define the frequency range to be simulated
    f_range = freq_gen(f_start, f_stop, decades)
    # Obtain the impedance of the RC circuit
    Randles = circuits.cir_Randles_simplified(f_range[1], Rs, R, n, sigma, Q)
    # Separate the impedance into its real and imaginary components
    real_z = Randles.real
    imag_z = Randles.imag
    # Calcuate the magnitude and phase angle of the impedance
    phase = np.arctan(imag_z/real_z)
    total_z = np.sqrt((real_z**2) + (imag_z**2))
    sim_data = to_dataframe(f_range, real_z, imag_z, total_z, phase)
    return sim_data


def sim_randles_file_writer(f_start, f_stop, decades, Rs, R, n, sigma,
                            Q, alteration=None):
    """
    Parameters
    ----------
    Output
    ----------
    """
    # Save the simulated data in a csv file to be exported in a database
    # the format will be in the form of :
    # yymmdd-serial#_sim_classifier.csv
    i = 1
    date = time.strftime('%y%m%d', time.localtime())
    save_location = 'sim_data/'
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    while i < 9999:
        number = str(i).zfill(4)
        if alteration:
            filename = str('{}-{}_sim_tail-{}'.format(date, number,
                                                      alteration))
        else:
            filename = str('{}-{}_sim_tail'.format(date, number))
        if os.path.exists(save_location + filename + '.csv'):
            i += 1
        else:
            break
    with open(save_location + filename + ".csv", mode='a',
              newline='') as data_file:
        data_file.write('Date:, {}'.format(date)+'\n')
        data_file.write('Serial number:, {}'.format(number)+'\n')
        data_file.write('Data Source:, simulation'+'\n')
        data_file.write('Circuit type:, rc'+'\n')
        data_file.write('Circuit elements:, [R={} ohm Rs ={} ohm sigma = {} \
                         ohm Q = {} F]'.format(R, Rs, sigma, Q) +
                        '\n')
        data_file.write('---'+'\n')
        df = randles(f_start, f_stop, decades, Rs, R, n, sigma, Q)
        df.to_csv(data_file, mode='a')
        data_file.close()
