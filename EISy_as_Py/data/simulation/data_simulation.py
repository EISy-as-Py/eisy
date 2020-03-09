import csv
import os
import time

import alteration
import numpy as np
import pandas as pd
import circuits

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
                  circuit_configuration):
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
    circuit_configuration : str
                            string indicating the configuration of the RC
                            circuit to be simulated

    Output
    ----------
    impedance_data_df: pandas.DataFrame
                           pandas dataframe containing frequency and imepedance
                           data.
    """
    # Define the frequency range to be simulated
    freq_range = circuits.freq_gen(high_freq, low_freq, decades)
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
                   circuit_configuration, alteration=None, save_image=None,
                   save_location='simulation_data/'):
    """
    Function that returns a .csv file containing metadata and simulated data
    of a resistor and a capacitor in two possible configuration: series or
    parallel.
    The filename contains a serial number composed by the date the funciton was
    run and the number of simuation for that day. If a file containing the
    output plot of the simulation is created, it will have the same filename
    to allow for fast matching of the visual and table representation of the
    same dataset.

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
                 Solution resistance [ohm]
    capacitance : single value (int or float)
                  Electrode capacitance [F]
    circuit_configuration : str
                            string containing the circuit configuration to be
                            simulated. Allowed configurations are 'series'or
                            'parallel'. [-]
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    save_image : True/False
                 Option to save the output of the simuation as a plot in a .png
                 file format. The filename used for the file will be the same
                 as the raw data file created in this function.
    save_location : str
                    String containing the path of the forlder to use when
                    saving the data and the image. Default option is a
                    folder called  'simulation_data' which will be created
                    in the current working directory.
    Output
    ----------
    *.csv : a .csv file containing metadata and raw data of the RC simulation.
    *.png : a .png file containing the plot of the simuated data. Default
            plot is a nyquist plot.

    """
    # Save the simulated data in a csv file to be exported in a database
    # the format will be in the form of :
    # yymmdd-serial#_sim_classifier.csv
    date = time.strftime('%y%m%d', time.localtime())
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    i = 1
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
        data_file.write('Circuit type:, -RC-'+'\n')
        data_file.write('Circuit configuration:, {}'
                        .format(circuit_configuration)+'\n')
        data_file.write('Circuit elements:, [R={} ohm C={} F]'
                        .format(resistance, capacitance) + '\n')
        if alteration:
            data_file.write('Alteration :, {}'.format(alteration))
        else:
            return
        data_file.write('---'+'\n')
        freq_range = circuits.freq_gen(high_freq, low_freq, decades)
        if circuit_configuration == 'series':
            circuit = circuits.cir_RC_series(freq_range[1], resistance,
                                             capacitance)
        elif circuit_configuration == 'parallel':
            circuit = circuits.cir_RC_parallel(freq_range[1], resistance,
                                               capacitance)
        else:
            raise AssertionError('The inputted configuration is not supported')
        df = RC_simulation(high_freq, low_freq, decades, resistance,
                           capacitance, circuit_configuration)
        if alteration:
            df = alteration.added_noise(df, 0.4)
        else:
            return
        df.to_csv(data_file, mode='a')
        data_file.close()
    if save_image:
        if alteration:
            nyquist_plot(df, filename, save_location, alteration=True,
                         save_image=True)
        else:
            nyquist_plot(df, filename, save_location, save_image=True)

    return


def RQ_simulation(high_freq, low_freq, decades, resistance,
                  constant_phase_element, alpha, circuit_configuration):
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
    constant_phase_element : single value (int or float)
                             Constant phase angle [s^(alpha-1)/ohm]
    alpha : single value -float
            Exponent of the constant phase element. Should be a value between
            0 and 1 [-]
    circuit_configuration : str
                            string indicating the configuration of the RC
                            circuit to be simulated

    Output
    ----------
    impedance_data_df: pandas.DataFrame
                           pandas dataframe containing frequency and imepedance
                           data.
    """
    # Define the frequency range to be simulated
    freq_range = circuits.freq_gen(high_freq, low_freq, decades)
    # Obtain the impedance of the RC circuit
    if circuit_configuration == 'series':
        complex_impedance = circuits.cir_RQ_series(freq_range[1], resistance,
                                                   constant_phase_element,
                                                   alpha)
    elif circuit_configuration == 'parallel':
        complex_impedance = circuits.cir_RQ_parallel(freq_range[1], resistance,
                                                     constant_phase_element,
                                                     alpha)
    else:
        raise AssertionError('The inputted configuration is not supported')
    impedance_data = impedance_array(complex_impedance)
    impedance_data_df = to_dataframe(freq_range, impedance_data)
    return impedance_data_df


def RQ_file_writer(high_freq, low_freq, decades, resistance,
                   constant_phase_element, alpha, circuit_configuration,
                   alteration=None, save_image=None,
                   save_location='simulation_data/'):
    """
    Function that returns a .csv file containing metadata and simulated data
    of a resistor and a constant phase element in two possible configuration:
    series or parallel.
    The filename contains a serial number composed by the date the funciton was
    run and the number of simuation for that day. If a file containing the
    output plot of the simulation is created, it will have the same filename
    to allow for fast matching of the visual and table representation of the
    same dataset.

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
                 Solution resistance [Ohm]
    constant_phase_element : single value (int or float)
                             Constant phase angle [s^(alpha-1)/ohm]
    alpha : single value -float
            Exponent of the constant phase element. Should be a value between
            0 and 1 [-]
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    save_image : True/False
                 Option to save the output of the simuation as a plot in a .png
                 file format. The filename used for the file will be the same
                 as the raw data file created in this function.
    save_location : str
                    String containing the path of the forlder to use when
                    saving the data and the image. Default option is a
                    folder called  'simulation_data' which will be created
                    in the current working directory.
    Output
    ----------
    *.csv : a .csv file containing metadata and raw data of the RC simulation.
    *.png : a .png file containing the plot of the simuated data. Default
            plot is a nyquist plot.
    """
    # Save the simulated data in a csv file to be exported in a database
    # the format will be in the form of :
    # yymmdd-serial#_sim_classifier.csv
    date = time.strftime('%y%m%d', time.localtime())
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    i = 1
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
        data_file.write('Circuit configuration:, {}'
                        .format(circuit_configuration)+'\n')
        data_file.write('Circuit elements:, [R={} ohm Q={} [s^(alpha-1)/ohm]\
alpha={}]'.format(resistance, constant_phase_element, alpha)
                        + '\n')
        if alteration:
            data_file.write('Alteration :, {}'.format(alteration))
        else:
            return
        data_file.write('---'+'\n')

        freq_range = circuits.freq_gen(high_freq, low_freq, decades)
        if circuit_configuration == 'series':
            circuit = circuits.cir_RQ_series(freq_range[1], resistance,
                                             constant_phase_element,
                                             alpha)
        elif circuit_configuration == 'parallel':
            circuit = circuits.cir_RQ_parallel(freq_range[1], resistance,
                                               constant_phase_element,
                                               alpha)
        else:
            raise AssertionError('The inputted configuration is not supported')
        df = RQ_simulation(high_freq, low_freq, decades, resistance,
                           constant_phase_element, alpha,
                           circuit_configuration)
        if alteration:
            df = alteration.added_noise(df, 0.4)
        else:
            return
        df.to_csv(data_file, mode='a')
        data_file.close()
    if save_image:
        if alteration:
            nyquist_plot(df, filename, save_location, alteration=True,
                         save_image=True)
        else:
            nyquist_plot(df, filename, save_location, save_image=True)
    return


def RsRCRC_simulation(high_freq, low_freq, decades, sol_resistance,
                      parallel_resistance_1, capacitance_1,
                      parallel_resistance_2, capacitance_2):
    """
    Function that takes imputs parameters to simulated the impedance response
    of a circuit composed by a resistor in series wihta two parallel circuits.
    Each circuit is composed by a resistor and a capacitor. The impedance
    response of the overall circuit is investigated over the indicated
    frequency range.

    Parameters
    ----------
    high_freq : single value (int or float)
                initial frequency value (high frequency domain) [Hz]
    high_freq : single value (int or float)
                final frequency value (low frequency domain) [Hz]
    decades : integer
              number of frequency decades to be used as range. Default value
              is set to be 7 [-]
    solution_resistance : single value (int or float)
                          Solution resistance [ohm]
    parallel_resistance_1 : single value (int or float)
                            first combination of resistor in parallel with
                            capacitor [ohm]
    capacitance_1 : single value (int or float)
                    Capacitance of an electrode surface whichi is part of the
                    first combination of RC in parallel [F]
    parallel_resistance_2 : single value (int or float)
                            second combination of resistor in parallel with
                            capacitor [ohm]
    capacitance_2 : single value (int or float)
                    Capacitance of an electrode surface whichi is part of the
                    second combination of RC in parallel [F]

    Output
    ----------
    impedance_data_df: pandas.DataFrame
                           pandas dataframe containing frequency and imepedance
                           data.
    """
    # Define the frequency range to be simulated
    freq_range = circuits.freq_gen(high_freq, low_freq, decades)
    # Obtain the impedance of the RsRCRC circuit
    complex_impedance = circuits.cir_RsRCRC(freq_range[1],
                                            sol_resistance,
                                            parallel_resistance_1,
                                            capacitance_1,
                                            parallel_resistance_2,
                                            capacitance_2)
    impedance_data = impedance_array(complex_impedance)
    impedance_data_df = to_dataframe(freq_range, impedance_data)
    return impedance_data_df


def RsRCRC_file_writer(high_freq, low_freq, decades, sol_resistance,
                       parallel_resistance_1, capacitance_1,
                       parallel_resistance_2, capacitance_2,
                       alteration=None, save_image=None,
                       save_location='simulation_data/'):
    """
    Function that returns a .csv file containing metadata and simulated data
    of a resistor in series wihta two parallel circuits.
    Each circuit is composed by a resistor and a capacitor. The impedance
    response of the overall circuit is investigated over the indicated
    frequency range.
    The filename contains a serial number composed by the date the funciton was
    run and the number of simuation for that day. If a file containing the
    output plot of the simulation is created, it will have the same filename
    to allow for fast matching of the visual and table representation of the
    same dataset.

    Parameters
    ----------
    high_freq : single value (int or float)
                initial frequency value (high frequency domain) [Hz]
    high_freq : single value (int or float)
                final frequency value (low frequency domain) [Hz]
    decades : integer
              number of frequency decades to be used as range. Default value
              is set to be 7 [-]
    solution_resistance : single value (int or float)
                          Solution resistance [ohm]
    parallel_resistance_1 : single value (int or float)
                            first combination of resistor in parallel with
                            capacitor [ohm]
    capacitance_1 : single value (int or float)
                    Capacitance of an electrode surface whichi is part of the
                    first combination of RC in parallel [F]
    parallel_resistance_2 : single value (int or float)
                            second combination of resistor in parallel with
                            capacitor [ohm]
    capacitance_2 : single value (int or float)
                    Capacitance of an electrode surface whichi is part of the
                    second combination of RC in parallel [F]
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    save_image : True/False
                 Option to save the output of the simuation as a plot in a .png
                 file format. The filename used for the file will be the same
                 as the raw data file created in this function.
    save_location : str
                    String containing the path of the forlder to use when
                    saving the data and the image. Default option is a
                    folder called  'simulation_data' which will be created
                    in the current working directory.
    Output
    ----------
    *.csv : a .csv file containing metadata and raw data of the RC simulation.
    *.png : a .png file containing the plot of the simuated data. Default
            plot is a nyquist plot.
    """
    # Save the simulated data in a csv file to be exported in a database
    # the format will be in the form of :
    # yymmdd-serial#_sim_classifier.csv
    date = time.strftime('%y%m%d', time.localtime())
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    i = 1
    while i < 9999:
        number = str(i).zfill(4)
        if alteration:
            filename = str('{}-{}_sim_spread-{}'.format(date,
                                                        number, alteration))
        else:
            filename = str('{}-{}_sim_spread'.format(date, number))
        if os.path.exists(save_location + filename + '.csv'):
            i += 1
        else:
            break
    with open(save_location + filename + ".csv", mode='a',
              newline='') as data_file:
        data_file.write('Date:, {}'.format(date)+'\n')
        data_file.write('Serial number:, {}'.format(number)+'\n')
        data_file.write('Data Source:, simulation'+'\n')
        data_file.write('Circuit type:, -Rs-(RC)-(RC)-'+'\n')
        data_file.write('Circuit elements: , [Rs={} ohm R1={} ohm C1={} F\
R2={} ohm C2={} F]'
                        .format(sol_resistance, parallel_resistace_1,
                                capacitance_1, parallel_resistace_2,
                                capacitance_2) + '\n')
        if alteration:
            data_file.write('Alteration :, {}'.format(alteration))
        else:
            return
        data_file.write('---'+'\n')

        freq_range = circuits.freq_gen(high_freq, low_freq, decades)

        df = RsRCRC_simulation(high_freq, low_freq, decades, sol_resistance,
                               parallel_resistace_1, capacitance_1,
                               parallel_resistace_2, capacitance_2)
        if alteration:
            df = alteration.added_noise(df, 0.4)
        else:
            return
        df.to_csv(data_file, mode='a')
        data_file.close()
    if save_image:
        if alteration:
            nyquist_plot(df, filename, save_location, alteration=True,
                         save_image=True)
        else:
            nyquist_plot(df, filename, save_location, save_image=True)
    return


def RsRQRQ_simulation(high_freq, low_freq, decades, solution_resistance,
                      parallel_resistance_1, constant_phase_element_1,
                      alpha_1, parallel_resistance_2,
                      constant_phase_element_2, alpha_2):
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
    solution_resistance : single value (int or float)
                          Solution resistance [ohm]
    parallel_resistance_1 : single value (int or float)
                            first combination of resistor in parallel with
                            constant phase element [ohm]
    constant_phase_element_1 : single value (int or float)
                               First constant phas angle [s^(alpha-1)/ohm]
    alpha_1 : single value -float
              Exponent of the first constant phase element.
              Should be a value between 0 and 1 [-]
    parallel_resistance_2 : single value (int or float)
                            Second combination of resistor in parallel with
                            constant phase element [ohm]
    constant_phase_element_2 : single value (int or float)
                               Second Constant phas angle [s^(alpha-1)/ohm]
    alpha_2 : single value -float
              Exponent of the second constant phase element.
              Should be a value between 0 and 1 [-]

    Output
    ----------
    impedance_data_df: pandas.DataFrame
                           pandas dataframe containing frequency and imepedance
                           data.
    """
    # Define the frequency range to be simulated
    freq_range = circuits.freq_gen(high_freq, low_freq, decades)
    # Obtain the impedance of the RsRCRC circuit
    complex_impedance = circuits.cir_RsRQRQ(freq_range[1],
                                            solution_resistance,
                                            parallel_resistance_1,
                                            constant_phase_element_1,
                                            alpha_1,
                                            parallel_resistance_2,
                                            constant_phase_element_2,
                                            alpha_2)
    impedance_data = impedance_array(complex_impedance)
    impedance_data_df = to_dataframe(freq_range, impedance_data)
    return impedance_data_df


def RsRQRQ_file_writer(high_freq, low_freq, decades, solution_resistance,
                       parallel_resistance_1, constant_phase_element_1,
                       alpha_1, parallel_resistance_2,
                       constant_phase_element_2, alpha_2,
                       alteration=None, save_image=None,
                       save_location='simulation_data/'):
    """
    Function that returns a .csv file containing metadata and simulated data
    of a resistor in series wihta two parallel circuits.
    Each parallel circuit is composed by a resistor and a constant phase
    element. The impedance response of the overall circuit is investigated
    over the indicated frequency range.

    The filename contains a serial number composed by the date the funciton was
    run and the number of simuation for that day. If a file containing the
    output plot of the simulation is created, it will have the same filename
    to allow for fast matching of the visual and table representation of the
    same dataset.

    Parameters
    ----------
    high_freq : single value (int or float)
                initial frequency value (high frequency domain) [Hz]
    high_freq : single value (int or float)
                final frequency value (low frequency domain) [Hz]
    decades : integer
              number of frequency decades to be used as range. Default value
              is set to be 7 [-]
    solution_resistance : single value (int or float)
                          Solution resistance [ohm]
    parallel_resistance_1 : single value (int or float)
                            first combination of resistor in parallel with
                            constant phase element [ohm]
    constant_phase_element_1 : single value (int or float)
                               First constant phas angle [s^(alpha-1)/ohm]
    alpha_1 : single value -float
              Exponent of the first constant phase element.
              Should be a value between 0 and 1 [-]
    parallel_resistance_2 : single value (int or float)
                            Second combination of resistor in parallel with
                            constant phase element [ohm]
    constant_phase_element_2 : single value (int or float)
                               Second Constant phas angle [s^(alpha-1)/ohm]
    alpha_2 : single value -float
              Exponent of the second constant phase element.
              Should be a value between 0 and 1 [-]
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    save_image : True/False
                 Option to save the output of the simuation as a plot in a .png
                 file format. The filename used for the file will be the same
                 as the raw data file created in this function.
    save_location : str
                    String containing the path of the forlder to use when
                    saving the data and the image. Default option is a
                    folder called  'simulation_data' which will be created
                    in the current working directory.
    Output
    ----------
    *.csv : a .csv file containing metadata and raw data of the RC simulation.
    *.png : a .png file containing the plot of the simuated data. Default
            plot is a nyquist plot.
    """
    # Save the simulated data in a csv file to be exported in a database
    # the format will be in the form of :
    # yymmdd-serial#_sim_classifier.csv
    date = time.strftime('%y%m%d', time.localtime())
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    i = 1
    while i < 9999:
        number = str(i).zfill(4)
        if alteration:
            filename = str('{}-{}_sim_two-{}'.format(date, number, alteration))
        else:
            filename = str('{}-{}_sim_two'.format(date, number))
        if os.path.exists(save_location + filename + '.csv'):
            i += 1
        else:
            break
    with open(save_location + filename + ".csv", mode='a',
              newline='') as data_file:
        data_file.write('Date:, {}'.format(date)+'\n')
        data_file.write('Serial number:, {}'.format(number)+'\n')
        data_file.write('Data Source:, simulation'+'\n')
        data_file.write('Circuit type:, -Rs-(RQ)-(RQ)-'+'\n')
        data_file.write('Circuit elements: , [Rs={} ohm R1={} ohm Q1={}\
[s^(alpha-1)/ohm] alpha_1={} R2={} ohm Q2={} [s^(alpha-1)/ohm] alpha_2={}]'
                        .format(solution_resistance, parallel_resistance_1,
                                constant_phase_element_1, alpha_1,
                                parallel_resistance_2,
                                constant_phase_element_1, alpha_2) + '\n')
        if alteration:
            data_file.write('Alteration :, {}'.format(alteration))
        else:
            return
        data_file.write('---'+'\n')

        freq_range = circuits.freq_gen(high_freq, low_freq, decades)

        df = RsRQRQ_simulation(high_freq, low_freq, decades,
                               solution_resistance,
                               parallel_resistance_1, constant_phase_element_1,
                               alpha_1, parallel_resistance_2,
                               constant_phase_element_2, alpha_2)
        if alteration:
            df = alteration.added_noise(df, 0.4)
        else:
            return
        df.to_csv(data_file, mode='a')
        data_file.close()
    if save_image:
        if alteration:
            nyquist_plot(df, filename, save_location, alteration=True,
                         save_image=True)
        else:
            nyquist_plot(df, filename, save_location, save_image=True)
    return

# Need to fix the following  functions before using them


def randles_simulation(f_start, f_stop, decades, Rs, R, n, sigma, Q):
    """
    Parameters
    ----------
    Output
    ----------
    """
    # Define the frequency range to be simulated
    freq_range = circuits.freq_gen(f_start, f_stop, decades)
    # Obtain the impedance of the RC circuit
    complex_impedance = circuits.cir_Randles_simplified(freq_range[1], Rs, R, n, sigma, Q)
    # Separate the impedance into its real and imaginary components
    impedance_data = impedance_array(complex_impedance)
    impedance_data_df = to_dataframe(freq_range, impedance_data)
    return impedance_data_df


def sim_randles_file_writer(high_freq, low_freq, decades, solution_resistance,
                            parallel_resistance_1, constant_phase_element_1,
                            alpha_1, sigma_1, alteration=None, save_image=None,
                            save_location='simulation_data/'):
    """
    Function that returns a .csv file containing metadata and simulated data
    of a resistor in series wihta two parallel circuits.
    Each parallel circuit is composed by a resistor and a constant phase
    element. The impedance response of the overall circuit is investigated
    over the indicated frequency range.

    The filename contains a serial number composed by the date the funciton was
    run and the number of simuation for that day. If a file containing the
    output plot of the simulation is created, it will have the same filename
    to allow for fast matching of the visual and table representation of the
    same dataset.

    Parameters
    ----------
    high_freq : single value (int or float)
                initial frequency value (high frequency domain) [Hz]
    high_freq : single value (int or float)
                final frequency value (low frequency domain) [Hz]
    decades : integer
              number of frequency decades to be used as range. Default value
              is set to be 7 [-]
    solution_resistance : single value (int or float)
                          Solution resistance [ohm]
    parallel_resistance_1 : single value (int or float)
                            first combination of resistor in parallel with
                            constant phase element [ohm]
    constant_phase_element_1 : single value (int or float)
                               First constant phas angle [s^(alpha-1)/ohm]
    alpha_1 : single value -float
              Exponent of the first constant phase element.
              Should be a value between 0 and 1 [-]
    parallel_resistance_2 : single value (int or float)
                            Second combination of resistor in parallel with
                            constant phase element [ohm]
    constant_phase_element_2 : single value (int or float)
                               Second Constant phas angle [s^(alpha-1)/ohm]
    alpha_2 : single value -float
              Exponent of the second constant phase element.
              Should be a value between 0 and 1 [-]
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    save_image : True/False
                 Option to save the output of the simuation as a plot in a .png
                 file format. The filename used for the file will be the same
                 as the raw data file created in this function.
    save_location : str
                    String containing the path of the forlder to use when
                    saving the data and the image. Default option is a
                    folder called  'simulation_data' which will be created
                    in the current working directory.
    Output
    ----------
    *.csv : a .csv file containing metadata and raw data of the RC simulation.
    *.png : a .png file containing the plot of the simuated data. Default
            plot is a nyquist plot.
    """
    # Save the simulated data in a csv file to be exported in a database
    # the format will be in the form of :
    # yymmdd-serial#_sim_classifier.csv
    date = time.strftime('%y%m%d', time.localtime())
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    i = 1
    while i < 9999:
        number = str(i).zfill(4)
        if alteration:
            filename = str('{}-{}_randles_simp-{}'.format(date, number,
                                                          alteration))
        else:
            filename = str('{}-{}_randles_simp'.format(date, number))
        if os.path.exists(save_location + filename + '.csv'):
            i += 1
        else:
            break
    with open(save_location + filename + ".csv", mode='a',
              newline='') as data_file:
        data_file.write('Date:, {}'.format(date)+'\n')
        data_file.write('Serial number:, {}'.format(number)+'\n')
        data_file.write('Data Source:, simulation'+'\n')
        data_file.write('Circuit type:, -Rs-(Cdl-(Rct-Zw))-'+'\n')
        data_file.write('Circuit elements: , [Rs={} ohm R1={} ohm Q1={}\
[s^(alpha-1)/ohm] alpha_1={} ohm sigma={}'
                        .format(solution_resistance, parallel_resistance_1,
                                constant_phase_element_1, alpha_1,
                                sigma_1) + '\n')
        if alteration:
            data_file.write('Alteration :, {}'.format(alteration))
        else:
            return
        data_file.write('---'+'\n')

        freq_range = circuits.freq_gen(high_freq, low_freq, decades)

        df = randles_simulation(high_freq, low_freq, decades,
                                solution_resistance,
                                parallel_resistance_1,
                                constant_phase_element_1,
                                alpha_1, sigma_1)

        if alteration:
            df = alteration.added_noise(df, 0.4)
        else:
            return
        df.to_csv(data_file, mode='a')
        data_file.close()
    if save_image:
        if alteration:
            nyquist_plot(df, filename, save_location, alteration=True,
                         save_image=True)
        else:
            nyquist_plot(df, filename, save_location, save_image=True)
    return
