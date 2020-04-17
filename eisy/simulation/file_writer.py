import csv
import glob
import os
import sys
import time


import numpy as np
import pandas as pd

from . import alterations
from . import circuits
from .data_simulation import *
from .plotting import *


def file_writer(freq_range, circuit_name, alteration=None, noisescale=None,
                axis_off=None, save_location='simulation_data/',
                source='simulation', scatter=None, plot_type='nyquist',
                transparent=None, save_image=None,
                **circuit_elements):
    ''' Function used to write a .csv file containing the metadata and raw data
     of the simulated impedance response.

    This function should be used to create a .csv file containing the metadata
    and the raw data of the simulation file.
    The circuit to be simulated is indicated in the circuit_name argument.
    Based on the circuit_name, the corresponding circuit function in the
    circuit module will be used. The circuit element parameters are to be
    specified in the circuit_elements arguments.

    Parameters
    ----------
    freq_range : array
                an array containing the frequency and angular frequency values
                used to determine the corresponding impedance response.
                freq_range[0]- the frequency response [Hz]
                freq_range[1]- the angualr frequncy [1/s]
    circucit_name: str
                   A string containng the name of the circuit to be simulated.
                   Refer to the circuits module for the list of accepted names.
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    noisescale : float
                 Scale of the noise added to the data. This number should be
                 contained betweed 0 and 1.
    axis_off : bool
               Option to remove the axis from a plot. This will allow to
               display only the datapoints. This format is preferred for CNN
               input.
    plot_type : str
                string indicating teh desired plot to use to visualize the data
                Te options are 'nyquist', 'log_freq' or 'both', if both
                representations are desired. An individual file per each type
                of plot will be generated and saved in a separate folder.
    scatter : bool
              Changes the type of matplotlib fuction to use from 'plot' to
              'scatter'.
    transparent : bool
                  Removes thebackground of the plot in the saving step. The
                  resulting .png file(s) will have a transparent background.
    save_location : str
                       String containing the path of the forlder to use when
                       saving the data and the image. Default option is a
                       folder called  'simulation_data' which will be created
                       in the current working directory.
    save_image : bool
                 Option to save the output of the simuation as a plot
                 in a .png file format.
                 The filename used for the file will be the same
                 as the raw data file created in this function.
    circuit_elements : dictionary or keyword arguments
                       input argument composed by the circuit elements
                       composing the called circuit. Refer to the circuits
                       module for the correct list of arguments that can be
                       added to this input.

    Returns
    ----------
    *.csv : a .csv file containing metadata and raw data of the simulation.
    *.png : a .png file containing the plot of the simulated data. Default
            plot is a nyquist plot.

    '''

    if not os.path.exists(save_location):
        os.makedirs(save_location)
    filename, serial_num = simulation_filename(circuit_name,
                                               alteration=alteration,
                                               save_location=save_location)
    with open(save_location + filename + ".csv", mode='a',
              newline='') as data_file:
        write_metadata(data_file, serial_num, circuit_name,
                       alteration=alteration, source=source,
                       **circuit_elements)
        df = write_data(data_file, freq_range, circuit_name,
                        alteration=alteration, noisescale=noisescale,
                        **circuit_elements)
    if save_image:
        save_plots(df, filename, plot_type=plot_type, alteration=alteration,
                   save_location=save_location,
                   axis_off=axis_off, save_image=save_image,
                   scatter=scatter, transparent=transparent)

    return


def simulation_filename(circuit_name, alteration=None,
                        save_location='simulation_data/'):
    """ Functiongenerates the filename of the simulation run and associates it
    with both the .csv and the .png files.

    The function generates the filename associated with the simulated
    impedance response that needs to be saved.
    The filename contains a serial number composed by the date the funciton was
    run and the number of simuation for that day. If a file containing the
    Output plot of the simulation is created, it will have the same filename
    to allow for fast matching of the visual and table representation of the
    same dataset. Additional tags in the filename are added to aid the
    labelling of each dataset genearted.

    Parameters
    ----------
    circucit_name: str
               A string containng the name of the circuit to be simulated.
               Refer to the circuits module for the list of accepted names.
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    save_location : str
                    String containing the path of the forlder to use when
                    saving the data and the image. Default option is a
                    folder called  'simulation_data' which will be created
                    in the current working directory.

    Returns
    ----------
    filename : str
               The filename contains a serial number composed by the date
               the funciton was run and the number of simuation for that day.
               The filename will be the same as the .csv file created from the
               impedance response used to create this plot.

    serial_number: str
                   serial number composed by the date the funciton was
                   run and the number of simuation for that day.

    """
    circuit_file_name = {'RC_series': 'none', 'RQ_series': 'none',
                         'RC_parallel': 'one', 'RQ_parallel': 'one',
                         'RsRC': 'one', 'RsRCRC': 'spread',
                         'RsRQRQ': 'two', 'Randles': 'tail'}
    if circuit_name in circuit_file_name:
        name = circuit_file_name[circuit_name]
    else:
        print('The indicated circuit in not support by the simuation module')

    date = time.strftime('%y%m%d', time.localtime())
    assert isinstance(date, str), 'the date should be a string'
    assert len(date) == 6, 'The date string should be 6 characters long'
    assert len(number) == 4, 'the serial number should be four characters +\
    long'

    i = 1
    assert isinstance(i, int), 'the serial number counters should be an +\
    integer'

    while i < 9999:
        number = str(i).zfill(4)

        if alteration and noisescale >= 0.2:
            filename = str('{}-{}_sim_{}_{}'.format(date, number,
                                                    name, alteration))
        else:
            filename = str('{}-{}_sim_{}'.format(date, number, name))

        serial_number, *rest = filename.split('_')

        # Need to figure this out
        list_of_files = glob.glob(save_location + '*.csv')
        if len(list_of_files) != 0:
            latest_file = max(list_of_files, key=os.path.getctime)
            if serial_number == latest_file.split('\\')[-1].split('_')[0]:
                i += 1
            else:
                break
        else:
            break

    return filename, serial_number


def write_metadata(data_file, serial_number, circuit_name,
                   alteration=None, source='simulation', **circuit_elements):
    """ Function used to write the metadata section of the .csv file containing
    impedance spectroscopy data.

    The metadata section contains infomration on the serial number of the file
    and its corresponding plots for easy association. The source of the data
    will be indicated as well, be it simulated or experimental. If simulated
    data is contained in the file, indication of the circuit configuration
    used and the corresponding values of each circuit element composing the
    circuit will be saved as well. If alterations were applied to the data,
    added noise or simualted instrument artifact, will be contained in this
    section as well.

    Parameters
    ----------
    data_file: str
               the name with which the file to be written was defined as.
               The file is open in append mode, so the raw data will be written
               below the metadata section.
    serial_number : str
                    string containg the serial number generated in the
                    simulation_filename function. This contains information
                    on the date the simulation was run and the order of
                    generation of this file.
    circucit_name: str
               A string containng the name of the circuit to be simulated.
               Refer to the circuits module for the list of accepted names.
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts.
    source: str
            String containing information on the source of the raw data
            contained in the .csv file. For now, only the simulation metadata
            structure has been finalized.
    circuit_elements : dictionary or keyword arguments
                       input argument composed by the circuit elements
                       composing the called circuit. Refer to the circuits
                       module for the correct list of arguments that can be
                       added to this input.
    """
#     units= {'R': 'ohm', 'C': 'F', 'alpha': '[-]', 'Q': '[s^(alpha-1)/ohm]'}

    # Serial number and data source:
    data_file.write('Serial number:, {}'.format(serial_number)+'\n')
    data_file.write('Data Source:,{}'.format(source)+'\n')

    # If simulated data, record the circuit type, the circuit element values
    if source == 'sim' or 'simulation':
        data_file.write('Circuit type:, -{}-'.format(circuit_name)+'\n')

        if circuit_name.split('_')[0] == 'RC':
            assert len(circuit_elements) == 2, 'the number of circuit +\
                                                elements should be 2'
            data_file.write('Circuit elements:, [R={} ohm C={} F]'
                            .format(circuit_elements['R'],
                                    circuit_elements['C']) + '\n')
        if circuit_name.split('_')[0] == 'RQ':
            assert len(circuit_elements) == 3, 'the number of circuit +\
                                                elements should be 3'
            data_file.write('Circuit elements:, [R={} ohm Q={} +\
            [s^(alpha-1)/ohm] alpha={}]'.format(circuit_elements['R'],
                                                circuit_elements['Q'],
                                                circuit_elements['alpha']
                                                ) + '\n')
        if circuit_name == 'RsRC':
            assert len(circuit_elements) == 3, 'the number of circuit +\
                                                elements should be 3'
            data_file.write('Circuit elements:, [Rs={} ohm Rp={} ohm C={} F]'
                            .format(circuit_elements['Rs'],
                                    circuit_elements['Rp'],
                                    circuit_elements['C']) + '\n')
        if circuit_name == 'RsRCRC':
            assert len(circuit_elements) == 5, 'the number of circuit +\
                                                elements should be 5'
            data_file.write('Circuit elements: , [Rs={} ohm Rp1={} ohm C1={} +\
            F Rp2={} ohm C2={} F]'.format(circuit_elements['Rs'],
                                          circuit_elements['Rp1'],
                                          circuit_elements['C1'],
                                          circuit_elements['Rp2'],
                                          circuit_elements['C2']) + '\n')
        if circuit_name == 'RsRQRQ':
            assert len(circuit_elements) == 7, 'the number of circuit+\
                                                elements should be 7'
            data_file.write('Circuit elements: , [Rs={} ohm Rp1={} ohm Q1={} +\
            [s^(alpha-1)/ohm] alpha_1={} Rp2={} ohm Q2={} [s^(alpha-1)/ohm] +\
            alpha_2={}]'.format(circuit_elements['Rs'],
                                circuit_elements['Rp1'],
                                circuit_elements['Q1'],
                                circuit_elements['alpha1'],
                                circuit_elements['Rp2'],
                                circuit_elements['Q2'],
                                circuit_elements['alpha2']) + '\n')
        if circuit_name == 'Randles':
            assert len(circuit_elements) == 5, 'the number of circuit+\
                                                elements should be 5'
            data_file.write('Circuit elements:, [Rs={} ohm Rp={} ohm Q={} +\
            [s^(alpha-1)/ohm] alpha={} sigma={}] +\
            '.format(circuit_elements['Rs'], circuit_elements['Rp'],
                     circuit_elements['Q'], circuit_elements['alpha'],
                     circuit_elements['sigma']) + '\n')
    # Indication of alteration
    if alteration and noisescale >= 0.2:
        data_file.write('Alteration :, {}'.format(alteration))
    else:
        data_file.write('Alteration :, None')

    data_file.write('\n'+'---'+'\n')

    return


def write_data(data_file, freq_range, circuit_name, alteration=None,
               noisescale=None, **circuit_elements):
    '''Function ued to save the raw data into a .csv file.

    The simulated raw data will be generated and saved into the file by
    converting the pandas DataFrame into a .csv file.

    Parameters
    ----------
    data_file: str
               the name with which the file to be written was defined as.
               The file is open in append mode, so the raw data will be written
               below the metadata section.
    freq_range : array-like
                an array containing the frequency and angular frequency values
                used to determine the corresponding impedance response.
                freq_range[0]- the frequency response [Hz]
                freq_range[1]- the angualr frequncy [1/s]
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts.
    noisescale : float
                 Scale of the noise added to the data. This number should be
                 contained betweed 0 and 1.
    circuit_elements : dictionary or keyword arguments
                       input argument composed by the circuit elements
                       composing the called circuit. Refer to the circuits
                       module for the correct list of arguments that can be
                       added to this input.

    Returns
    -------
    dataframe: pandas DataFrame
               pandas dataframe containing frequency and imepedance data
    '''
    dataframe = circuit_simulation(freq_range, circuit_name,
                                   noisescale=noisescale,
                                   alteration=alteration,
                                   **circuit_elements)

    if alteration:
        noise_function = getattr(alterations, alteration)
        dataframe = noise_function(df, noisescale)
    else:
        dataframe = dataframe
    dataframe.to_csv(data_file, mode='a')
    data_file.close()

    return dataframe


def save_plots(response, filename, save_location='simuation_data/',
               alteration=None, plot_type='nyquist',
               axis_off=None, save_image=None,
               scatter=None, transparent=None):
    ''' Function used to save the impedance response in a nyquist or Frequency
    versus real and imaginary components.

    This function allows saving the plot of the impedance response simulated.
    Additional functionalities specified in the function are geared towards
    using theplots of the data as inputs of a neural network. The axis can be
    removed, as well as the background. The saved image will have the same
    filename of its corresponding raw data .csv file.

    Parameters
    ----------
    response : pandas.DataFrame
               a dataframe containing the impedance response to be plotted.
    filename : str
               The filename contains a serial number composed by the date
               the funciton was run and the number of simuation for that day.
               The filename will be the same as the .csv file created from the
               impedance response used to create this plot.
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    save_location : str
                    String containing the path of the forlder to use when
                    saving the data and the image. Default option is a
                    folder called  'simulation_data' which will be created
                    in the current working directory.
    save_image : bool
                 Option to save the output of the simuation as a plot
                 in a .png file format.
                 The filename used for the file will be the same
                 as the raw data file created in this function.
    axis_off : bool
               Option to remove the axis from a plot. This will allow to
               display only the datapoints. This format is preferred for CNN
               input.
    plot_type : str
                string indicating teh desired plot to use to visualize the data
                Te options are 'nyquist', 'log_freq' or 'both', if both
                representations are desired. An individual file per each type
                of plot will be generated and saved in a separate folder.
    scatter : bool
              Changes the type of matplotlib fuction to use from 'plot' to
              'scatter'.
    transparent : bool
                  Removes thebackground of the plot in the saving step. The
                  resulting .png file(s) will have a transparent background.


    Output
    ----------
    .png file(s) of the nyquist and/or frequency vs. complex impedance plots of
    the impedance response to be investigated.
    '''
    save_location = save_location + 'plots/'
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    if plot_type == 'nyquist':
        save_location = save_location + 'nyquist/'
        if not os.path.exists(save_location):
            os.makedirs(save_location)
        filename = filename + '_nyquist'
        nyquist_plot(response, filename=filename, save_location=save_location,
                     alteration=alteration, transparent=transparent,
                     axis_off=axis_off, save_image=save_image,
                     scatter=scatter)
    if plot_type == 'log_freq':
        filename = filename + '_log-freq'

        save_location = save_location + 'log_freq/'
        if not os.path.exists(save_location):
            os.makedirs(save_location)

        log_freq_plot(response, filename=filename, save_location=save_location,
                      alteration=alteration,  save_image=save_image,
                      axis_off=axis_off, scatter=None, transparent=transparent)

    if plot_type == 'both':
        filename = filename + '_nyquist'
        save_location = save_location + 'nyquist/'
        if not os.path.exists(save_location):
            os.makedirs(save_location)
        nyquist_plot(response, filename=filename, save_location=save_location,
                     alteration=alteration, transparent=transparent,
                     axis_off=axis_off, save_image=save_image,
                     scatter=scatter)

        filename = filename + '_log-freq'
        save_location = save_location + '../log_freq/'
        if not os.path.exists(save_location):
            os.makedirs(save_location)

        log_freq_plot(response, filename=filename, save_location=save_location,
                      alteration=alteration, save_image=save_image,
                      axis_off=axis_off, scatter=None, transparent=transparent)

    return
