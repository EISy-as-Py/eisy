import os
import csv
import unittest


import eisy.simulation.circuits as circuits
from eisy.simulation.file_writer import (file_writer, simulation_filename,
                                         write_metadata, write_data)


class TestSimulationTools(unittest.TestCase):

    def test_file_writer(self):
        freq_range = circuits.freq_gen(10**6, 0.01)
        save_loc = './eisy/test'
        circuit_name = 'RC_parallel'
        alteration = 'random_imag_noise'
        file_writer(freq_range, circuit_name, save_location=save_loc,
                    C=1E-5, R=100)
        assert isinstance(save_loc, str), 'the save_location input \
should be a string'
        assert isinstance(circuit_name, str), 'the circuit name should be \
inputted as a string'
        assert isinstance(alteration, str), 'the alteration argument should \
be a string'
        filename, serail_number = simulation_filename(circuit_name,
                                                      alteration=alteration,
                                                      save_location=save_loc,
                                                      noise_amplitude=0)
        with open(save_loc + filename + '.csv', mode='r',
                  newline='') as data_file:
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
            print('# of lines : {}'.format(len(rows)))
            assert 'Serial number' in rows[0][0], 'the first row of the \
metadata part of the file should containg the serial_number'
            assert '---' in rows[5][0], 'the metadata should be included in \
the file'
            assert 'angular_freq [1/s]' in rows[6][2], 'the raw data should be\
 contained in the generated file'
            data_file.close()
        os.remove(save_loc + filename + '.csv')

    def test_simulation_filename(self):
        save_loc = './'
        circuit_name = 'RC_parallel'
        alteration = 'random_imag_noise'
        assert isinstance(save_loc, str), 'the save_location input \
should be a string'
        assert isinstance(circuit_name, str), 'the circuit name should be \
inputted as a string'
        assert isinstance(alteration, str), 'the alteration argument should \
be a string'

        filename, serial_number = simulation_filename(circuit_name,
                                                      alteration=alteration,
                                                      save_location=save_loc,
                                                      noise_amplitude=0)
        assert isinstance(filename, str), 'The filename should be a string'
        assert isinstance(serial_number, str), 'The serial_number should be \
a string'

    def test_write_metadata(self):
        filename, serial_number = simulation_filename('RC_parallel',
                                                      save_location='./')
        C = 1E-5
        R = 100
        source = 'sim'
        with open('test'+filename + ".csv", mode='w', newline='') as data_file:
            write_metadata(data_file, serial_number, 'RC_parallel',
                           source='sim', C=C, R=R)
            data_file.close()
        with open('test'+filename + ".csv", mode='r', newline='') as data_file:
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
            assert serial_number in rows[0][0], 'the first row of the \
metadata part of the file should containg the serial_number'
            assert source in rows[1][0], 'the data source should be \
part of the metadata of the file'
            assert 'R={}'.format(R) in rows[3][0], 'the circuit elements \
values should be indicated'
            assert 'C={}'.format(C) in rows[3][0], 'the circuit elements \
values should be indicated'
            assert '---' in rows[5][0], 'the three hyphens indicating the \
break of the metadata part of the files need to be present '

            data_file.close()
        os.remove('test'+filename + ".csv")

    def test_write_data(self):
        freq_range = circuits.freq_gen(10**6, 0.01)
        filename, serial_number = simulation_filename('RC_parallel',
                                                      save_location='./')

        with open('test'+filename + ".csv", mode='w', newline='') as data_file:
            write_data(data_file, freq_range, 'RC_parallel', C=1E-5, R=100)
            data_file.close()
        with open('test'+filename + ".csv", mode='r', newline='') as data_file:
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
            assert 'freq [Hz]' in rows[0][1], 'the dataframe is not appended \
to the .csv file just created'
            assert str(freq_range[0][0]) in rows[1][1], 'the dataframe is \
not appended to the .csv file created'
        data_file.close()
        os.remove('test'+filename + ".csv")
