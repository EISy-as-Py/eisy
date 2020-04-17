import os
import sys
import csv
import time
import unittest

module_path = os.path.abspath(os.path.join('../simulation'))
if module_path not in sys.path:
    sys.path.append(module_path)

import numpy as np
import pandas as pd

import eisy.simulation.alterations as alterations
import eisy.simulation.circuits as circuits
from eisy.simulation.data_simulation import *
from eisy.simulation.file_writer import *


class TestSimulationTools(unittest.TestCase):

    def test_file_writer(self):
        freq_range = np.array([1, 100, 10])
        save_location = './'
        circuit_name = 'RC_parallel'
        alteration = 'random_imag_noise'
        file_writer(freq_range, circuit_name, save_location=save_location,
                    C=1E-5, R=100)
        assert isinstance(save_location, str), 'the save_location input +\
        should be a string'
        assert isinstance(circuit_name, str), 'the circuit name should be +\
        inputted as a string'
        assert isinstance(alteration, str), 'the alteration argument should +\
        be a string'
        assert isinstance(freq_range, np.ndarray), 'the frequency should in +\
        array format'
        list_of_files = glob.glob(save_location + '*.csv')
        with open(list_of_files, mode='r', newline='') as data_file:
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
            assert 'serial_number' in rows[0][0], 'the first row of the +\
            metadata part of the file should containg the serial_number'
            assert '---' in rows[5][0], 'the metadata should be included in +\
            the file'
            assert 'freq [Hz]' in rows[6][1], 'the raw data should be +\
            contained in the generated file'
            os.remove(list_of_files)

    def test_simulation_filename(self):
        save_location = './'
        circuit_name = 'RC_parallel'
        alteration = 'random_imag_noise'
        assert isinstance(save_location, str), 'the save_location input +\
        should be a string'
        assert isinstance(circuit_name, str), 'the circuit name should be +\
        inputted as a string'
        assert isinstance(alteration, str), 'the alteration argument should +\
        be a string'

        filename, serial_number = simulation_filename(circuit_name,
                                                      alteration,
                                                      save_location)
        assert isinstance(filename, str), 'The filename should be a string'
        assert isinstance(serial_number, str), 'The serial_number should be +\
        a string'
        assert filename.includes(serial_number), 'the seral_number should be +\
        contained in teh filename'

    def test_write_metadata(self):
        filename, serial_number = simulation_filename('RC_parallel',
                                                      save_location='./')

        with open('test'+filename + ".csv", mode='r', newline='') as data_file:
            write_metadata(data_file, serial_number, 'RC_parallel',
                           source='sim', C=1E-5, R=100)
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
            assert serial_number in rows[0][1], 'the first row of the +\
            metadata part of the file should containg the serial_number'
            assert source in rows[1][1], 'the data source should be +\
            part of the metadata of the file'
            assert 'R={}'.format(R) in rows[3][1], 'the circuit elements +\
            values should be indicated'
            assert 'C={}'.format(C) in rows[3][1], 'the circuit elements +\
            values should be indicated'
            assert '---' in rows[5][0], 'the three hyphens indicating the +\
            break of the metadata part of the files need to be present '

            data_file.close()
            os.remove('test'+filename + ".csv")

    def test_write_data(self):
        freq_range = np.array([1, 100, 10])
        filename, serial_number = simulation_filename('RC_parallel',
                                                      save_location='./')

        with open('test'+filename + ".csv", mode='r', newline='') as data_file:
            write_data(data_file, freq_range, 'RC_parallel', C=1E-5, R=100)
        assert isinstance(freq_gen, np.ndarray), 'the frequency should be +\
        inputted as an array'
        assert 'freq [Hz]' in rows[0][1], 'the dataframe is not appended +\
        to the .csv file just created'
        assert str(freq_range[0][0]) in rows[1][1], 'the dataframe is not +\
        appended to the .csv file created'
        os.remove('test'+filename + ".csv")
        data_file.close()
