import csv
import os
import time

import numpy as np
import pandas as pd

from PyEIS import *


def to_dataframe(f_range, real_z, imag_z, total_z, phase):
    """
    """
    sim_data = {'freq [Hz]': f_range[0], 'angular_freq [1/s]': f_range[1],
                'Re_Z [Ohm]': real_z, 'Im_Z [Ohm]': imag_z, '|Z| [Ohm]':
                total_z, 'phase_angle [rad]': phase}
    sim_data_df = pd.DataFrame(sim_data)
    return sim_data_df


def rc_simulation(f_start, f_stop, decades, R, C, i):
    """
    """
    # Define the frequency range to be simulated
    f_range = freq_gen(f_start, f_stop, decades)
    # Obtain the impedance of the RC circuit
    circuit = cir_RC(f_range[1], R, C)
    # Separate the impedance into its real and imaginary components
    real_z = circuit.real
    imag_z = circuit.imag
    # Calcuate the magnitude and phase angle of the impedance
    phase = np.arctan(imag_z/real_z)
    total_z = np.sqrt((real_z**2) + (imag_z**2))
    sim_data = to_dataframe(f_range, real_z, imag_z, total_z, phase)
    return sim_data


def sim_rc_file_writer(f_start, f_stop, decades, R, C, i,
                       alteration=None):
    """
    """
    # Save the simulated data in a csv file to be exported in a database
    # the format will be in the form of :
    # yymmdd-serial#_sim_classifier.csv
    date = time.strftime('%y%m%d', time.localtime())
    save_location = 'sim_data/'
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
        df = rc_simulation(f_start, f_stop, decades, R, C, i)
        df.to_csv(data_file, mode='a')
        data_file.close()

def randles(f_start, f_stop, decades, Rs, R, n, sigma, Q):
    """
    """
    # Define the frequency range to be simulated
    f_range = freq_gen(f_start, f_stop, decades)
    # Obtain the impedance of the RC circuit
    Randles = cir_Randles_simplified(f_range[1], Rs, R, n, sigma, Q)
    # Separate the impedance into its real and imaginary components
    real_z = Randles.real
    imag_z = Randles.imag
    # Calcuate the magnitude and phase angle of the impedance
    phase = np.arctan(imag_z/real_z)
    total_z = np.sqrt((real_z**2) + (imag_z**2))
    sim_data = to_dataframe(f_range, real_z, imag_z, total_z, phase)
    return sim_data

def sim_randles_file_writer(f_start, f_stop, decades, Rs, R, n, sigma, Q, alteration=None):
    """
    """
    # Save the simulated data in a csv file to be exported in a database
    # the format will be in the form of :
    # yymmdd-serial#_sim_classifier.csv
    i=1
    date = time.strftime('%y%m%d', time.localtime())
    save_location = 'sim_data/'
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    while i < 9999:
        number = str(i).zfill(4)
        if alteration:
            filename = str('{}-{}_sim_tail-{}'.format(date, number, alteration))
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
        data_file.write('Circuit elements:, [R={} ohm Rs ={} ohm sigma = {} ohm Q = {} F]'.format(R, Rs, sigma, Q) +
                        '\n')
        data_file.write('---'+'\n')
        df = randles(f_start, f_stop, decades, Rs, R, n, sigma, Q)
        df.to_csv(data_file, mode='a')
        data_file.close()
