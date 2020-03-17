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
from eisy.simulation.plotting import nyquist_plot
from eisy.simulation.data_simulation import *


class TestSimulationTools(unittest.TestCase):

    def test_to_dataframe(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        R = 100  # ohm
        C = 10E-6  # F
        n_points = np.round(decades * np.log10(int(high_freq)) -
                            np.log10(low_freq))
        f_range = circuits.freq_gen(high_freq, low_freq, decades=7)
        circuit = circuits.cir_RC_parallel(f_range[1], R, C)
        impedance_arr = impedance_array(circuit)
        dataframe = to_dataframe(f_range, impedance_arr)

        assert isinstance(decades, int),\
            'the number of decades should be an integer'
        assert high_freq >= low_freq,\
            'the low frequency should be smaller than the high\
 frequency limit value. Check again.'
        np.testing.assert_almost_equal(len(f_range[1]),
                                       impedance_arr[0].shape[0], decimal=18,
                                       err_msg='the impedance is not correclty\
 computed. The number of points in the array is not correct.')
        assert len(f_range[1]) == impedance_arr[0].shape[0],\
            'the frequency and the impedance respons do not match in length.\
 Check again.'
        assert len(impedance_arr) == 5, 'the impedance array inputted is not\
 the right dimensions. The number of columns exceed the expected value (5)'
        assert isinstance(impedance_arr[0][1], complex), 'the first column of\
 the impedance response should be populated by complex numberes'
        assert dataframe.columns[0] == 'freq [Hz]', 'the first column should\
 contain the frequency respose.'
        assert dataframe.columns[1] == 'angular_freq [1/s]', 'the second\
 column should contain the angular frequency respose.'
        assert dataframe.columns[2] == 'Re_Z [ohm]', 'the third column should\
 contain the real impedance part.'
        assert dataframe.columns[3] == 'Im_Z [ohm]', 'the fourth column\
 should contain the imaginary impedance part.'
        assert dataframe.columns[4] == '|Z| [ohm]', 'the fifth column \
should contain the magnitude of the impedance.'
        assert dataframe.columns[5] == 'phase_angle [rad]', 'the sixth column\
 should contain the phase angle of the impedance.'
        assert dataframe['freq [Hz]'][0] == f_range[0][0], 'the first column\
 should contain the frequency respose. Check again'
        assert dataframe['angular_freq [1/s]'][0] == f_range[1][0],\
            'the second column should contain the angular frequency respose.\
 Check again'
        assert dataframe['Re_Z [ohm]'][0] == circuit[0].real, 'the third\
 column should contain the real impedance respose. Check again'
        assert dataframe['Im_Z [ohm]'][0] == circuit[0].imag, 'the fourth\
 column should contain the real impedance respose. Check again'
        assert isinstance(dataframe, pd.DataFrame), 'The output should be\
 a pandas.DataFrame'

    def test_impedance_array(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        R = 100  # ohm
        C = 10E-6  # F
        n_points = np.round(decades * np.log10(int(high_freq)) -
                            np.log10(low_freq))
        f_range = circuits.freq_gen(high_freq, low_freq, decades=7)
        circuit = circuits.cir_RC_parallel(f_range[1], R, C)
        impedance = impedance_array(circuit)
        assert isinstance(decades, int), 'the number of decades should\
 be an integer'
        assert high_freq >= low_freq, 'the low frequency should be smaller\
 than the high frequency limit value. Check again.'
        np.testing.assert_almost_equal(len(f_range[1]),
                                       impedance[0].shape[0], decimal=18,
                                       err_msg='the impedance is\
 not correclty computed. The number of points in the array is not correct.')
        assert len(f_range[1]) == impedance[0].shape[0], 'the frequency and\
 the impedance respons do not match in length. Check again.'
        assert len(impedance) == 5, 'the impedance array inputted is not the\
 right dimensions. The number of columns exceed the expected value (5)'
        assert isinstance(impedance[0][1], complex), 'the first column of the\
 impedance response should be populated by complex numberes'
        assert circuit[0].real == impedance[1][0], 'the complex impedance is\
 not separated into its real and imaginary parts correctly.'
        assert circuit[0].imag == impedance[2][0], 'the complex impedance is\
 not separated into its real and imaginary parts correctly.'

    def test_RC_simuation(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        R = 100  # ohm
        C = 10E-6  # F
        n_points = np.round(decades * np.log10(int(high_freq)) -
                            np.log10(low_freq))
        f_range = circuits.freq_gen(high_freq, low_freq, decades=7)
        # Define the RC parallel simulation
        circuit_configuration_p = 'parallel'
        circuit_parallel = circuits.cir_RC_parallel(f_range[1], R, C)
        impedance_data_p = impedance_array(circuit_parallel)
        impedance_data_p_df = to_dataframe(f_range, impedance_data_p)
        # Define the RC series simulation
        circuit_configuration_s = 'series'
        circuit_series = circuits.cir_RC_series(f_range[1], R, C)
        impedance_data_s = impedance_array(circuit_series)
        impedance_data_s_df = to_dataframe(f_range, impedance_data_s)

        assert isinstance(decades, int), 'the number of decades should be\
    an integer'
        assert high_freq >= low_freq, 'the low frequency should be smaller\
 than the high frequency limit value. Check again.'
        np.testing.assert_almost_equal(len(f_range[1]),
                                       impedance_data_p[0].shape[0],
                                       decimal=18, err_msg='the impedance\
 is not correclty computed. The number of points in the array is not correct.')
        np.testing.assert_almost_equal(len(f_range[1]),
                                       impedance_data_s[0].shape[0],
                                       decimal=18, err_msg='the impedance\
 is not correclty computed. The number of points in the array is not correct.')
        assert isinstance(impedance_data_p_df, pd.DataFrame), \
            'The output should be a pandas.DataFrame'
        assert isinstance(impedance_data_s_df, pd.DataFrame), \
            'The output should be a pandas.DataFrame'
        assert len(f_range[1]) == impedance_data_p[0].shape[0], 'the frequency\
 and the impedance respons do not match in length. Check again.'
        assert isinstance(circuit_configuration_p, str), 'the circuit\
     configuration should be a string.'
        assert len(impedance_data_p) == 5, 'the impedance array inputted\
 is not the right dimensions. The number of columns exceed the\
 expected value (5)'
        for item in impedance_data_p[0][:]:
            assert isinstance(item, complex), 'the first\
 column of the impedance response should be populated by complex numberes'
        assert circuit_parallel[0].real == impedance_data_p[1][0], 'the\
 complex impedance is not separated into its real and imaginary\
 parts correctly.'
        assert circuit_parallel[0].imag == impedance_data_p[2][0], 'the\
 complex impedance is not separated into its real and imaginary parts\
 correctly.'
        assert isinstance(circuit_configuration_s, str), 'the circuit\
     configuration should be a string.'
        assert len(f_range[1]) == impedance_data_s[0].shape[0], 'the frequency\
 and the impedance respons do not match in length. Check again.'
        assert len(impedance_data_s) == 5, 'the impedance array inputted is\
 not the right dimensions. The number of columns exceed the expected value (5)'
        for item in impedance_data_s[0][:]:
            assert isinstance(item, complex), 'the first\
 column of the impedance response should be populated by complex numberes'
        assert circuit_series[0].real == impedance_data_s[1][0], 'the complex\
     impedance is not separated into its real and imaginary parts correctly.'
        assert circuit_series[0].imag == impedance_data_s[2][0], 'the complex\
     impedance is not separated into its real and imaginary parts correctly.'
        assert isinstance(C, float), 'the capacitance should be a float,\
     not an integer'
        assert C <= 1, 'the capacitance value is probably too high.'

    def test_RC_file_writer(self):

        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        R = 100  # ohm
        C = 10E-6  # F
        f_range = circuits.freq_gen(high_freq, low_freq, decades=7)

        # Define the RC parallel simulation
        circuit_configuration_p = 'parallel'
        date = time.strftime('%y%m%d', time.localtime())
        assert isinstance(date, str), 'the date should be a string'
        assert len(date) == 6, 'The date string should be 6 characters long'
        save_location = 'simulation_data/'
        assert isinstance(save_location, str)
        i = 1
        assert isinstance(i, int), 'the serial number counters should be an\
 integer'
        assert i >= 1, 'the counter should be a number higher than one'
        alteration = 'noise'
        number = str(i).zfill(4)
        assert len(number) == 4, 'the serial number should be four characters \
 long'
        assert isinstance(alteration, str), 'the alteration argument should be\
 a string'
        filename = str('{}-{}_sim_one-{}'.format(date, number, alteration))
        assert isinstance(filename, str), 'the filename should be a string'
        assert date in filename, 'the filename should contain the date as part\
 of the serial number'
        assert number in filename, 'the filename should contain the file\
 number as part of the serial number'
        assert isinstance(circuit_configuration_p, str), 'the circuit\
 configuration should be a string.'
        with open(filename + ".csv", mode='a', newline='') as data_file:
            data_file.write('Date:, {}'.format(date)+'\n')
            data_file.write('Serial number:, {}'.format(number)+'\n')
            data_file.write('Data Source:, simulation'+'\n')
            data_file.write('Circuit type:, -RC-'+'\n')
            data_file.write('Circuit configuration:, {}'
                            .format(circuit_configuration_p)+'\n')
            data_file.write('Circuit elements:, [R={} ohm C={} F]'
                            .format(R, C) + '\n')
            if alteration:
                data_file.write('Alteration :, {} \n'.format(alteration))
            else:
                data_file.write('Alteration :, None', '\n')
            data_file.write('---'+'\n')
            freq_range = circuits.freq_gen(high_freq, low_freq, decades)
            df = RC_simulation(high_freq, low_freq, decades, R, C,
                               circuit_configuration_p)
            if alteration:
                df = alterations.added_noise(df, 0.4)
            else:
                df = df
            df.to_csv(data_file, mode='a')
            data_file.close()
        with open(filename + ".csv", mode='r', newline='') as data_file:
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
            assert date in rows[0][1], 'the first row of the metadata part\
 of the file should containg the data the file was created'
            assert number in rows[1][1], 'the second row of the metadata part\
 of the file should containg the serial number of the file'
            assert 'Data Source:' in rows[2][0], 'the data source should be\
 part of the metadata of the file'
            assert 'Circuit type:' in rows[3][0], 'the circuit type should\
 be indicated if the '
            assert circuit_configuration_p in rows[4][1], 'the circuit\
 configuraiton should be indicated in the metadata part of the file'
            assert 'R={}'.format(R) in rows[5][1], 'the circuit elements\
 values should be indicated'
            assert 'C={}'.format(C) in rows[5][1], 'the circuit elements\
 values should be indicated'
            assert 'Alteration :' in rows[6], 'Indication of any type of data\
 alteration to the simuation data needs to be inidcated'
            assert '---' in rows[7], 'the three hyphens indicating the break\
 of the metadata part of the files need to be present '
            # print(rows)
            assert 'freq [Hz]' in rows[8][1], 'the dataframe is not appended\
 to the .csv file just created'
            assert str(freq_range[0][0]) in rows[9][1], 'the dataframe is not\
 appended to the .csv file created'
        os.remove(filename + ".csv")

    def test_RQ_simulation(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        R = 100  # ohm
        Q = 10E-6  #
        alpha = 0.75
        n_points = np.round(decades * np.log10(int(high_freq)) -
                            np.log10(low_freq))
        f_range = circuits.freq_gen(high_freq, low_freq, decades=7)
        # Define the RC parallel simulation
        circuit_configuration_p = 'parallel'
        circuit_parallel = circuits.cir_RQ_parallel(f_range[1], R, Q, alpha)
        impedance_data_p = impedance_array(circuit_parallel)
        impedance_data_p_df = to_dataframe(f_range, impedance_data_p)
        # Define the RC series simulation
        circuit_configuration_s = 'series'
        circuit_series = circuits.cir_RQ_series(f_range[1], R, Q, alpha)
        impedance_data_s = impedance_array(circuit_series)
        impedance_data_s_df = to_dataframe(f_range, impedance_data_s)

        assert isinstance(decades, int), 'the number of decades should be\
    an integer'
        assert high_freq >= low_freq, 'the low frequency should be smaller\
 than the high frequency limit value. Check again.'
        np.testing.assert_almost_equal(len(f_range[1]),
                                       impedance_data_p[0].shape[0],
                                       decimal=18, err_msg='the impedance\
 is not correclty computed. The number of points in the array is not correct.')
        np.testing.assert_almost_equal(len(f_range[1]),
                                       impedance_data_s[0].shape[0],
                                       decimal=18, err_msg='the impedance\
 is not correclty computed. The number of points in the array is not correct.')
        assert isinstance(impedance_data_p_df, pd.DataFrame), \
            'The output should be a pandas.DataFrame'
        assert isinstance(impedance_data_s_df, pd.DataFrame), \
            'The output should be a pandas.DataFrame'
        assert len(f_range[1]) == impedance_data_p[0].shape[0], 'the frequency\
 and the impedance respons do not match in length. Check again.'
        assert isinstance(circuit_configuration_p, str), 'the circuit\
     configuration should be a string.'
        assert len(impedance_data_p) == 5, 'the impedance array inputted\
 is not the right dimensions. The number of columns exceed the\
 expected value (5)'
        for item in impedance_data_p[0][:]:
            assert isinstance(item, complex), 'the first\
column of the impedance response should be populated by complex numberes'
        assert circuit_parallel[0].real == impedance_data_p[1][0], 'the\
 complex impedance is not separated into its real and imaginary\
 parts correctly.'
        assert circuit_parallel[0].imag == impedance_data_p[2][0], 'the\
 complex impedance is not separated into its real and imaginary parts\
 correctly.'
        assert isinstance(circuit_configuration_s, str), 'the circuit\
     configuration should be a string.'
        assert len(f_range[1]) == impedance_data_s[0].shape[0], 'the frequency\
 and the impedance respons do not match in length. Check again.'
        assert len(impedance_data_s) == 5, 'the impedance array inputted is\
 not the right dimensions. The number of columns exceed the expected value (5)'
        for item in impedance_data_s[0][:]:
            assert isinstance(item, complex), 'the first\
column of the impedance response should be populated by complex numberes'
        assert circuit_series[0].real == impedance_data_s[1][0], 'the complex\
     impedance is not separated into its real and imaginary parts correctly.'
        assert circuit_series[0].imag == impedance_data_s[2][0], 'the complex\
     impedance is not separated into its real and imaginary parts correctly.'
        assert isinstance(Q, float), 'the capacitance should be a float,\
     not an integer'
        assert Q <= 1, 'the constant phase element value is probably too high'
        assert alpha <= 1, 'the exponent of the constatn phase element should\
 be a number between 0 and 1'
        assert 0 <= alpha, 'the exponent of the constatn phase element should\
 be a number between 0 and 1'

    def test_RQ_file_writer(self):

        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        R = 100  # ohm
        Q = 10E-6  # s^(alpha-1)/ohm
        alpha = 0.75  # [-]
        # Define the RC parallel simulation
        circuit_configuration = 'parallel'
        # circuit_parallel = circuits.cir_RQ_parallel(f_range[1], R, Q, alpha)
        # impedance_data_p = impedance_array(circuit_parallel)
        # impedance_data_p_df = to_dataframe(f_range, impedance_data_p)

        date = time.strftime('%y%m%d', time.localtime())
        assert isinstance(date, str), 'the date should be a string'
        assert len(date) == 6, 'The date string should be 6 characters long'
        save_location = 'simulation_data/'
        assert isinstance(save_location, str)
        i = 1
        assert isinstance(i, int), 'the serial number counters should be an\
    integer'
        assert i >= 1, 'the counter should be a number higher than one'
        alteration = 'noise'
        number = str(i).zfill(4)
        assert len(number) == 4, 'the serial number should be four characters \
    long'
        assert isinstance(alteration, str), 'the alteration argument should be\
    a string'
        filename = str('{}-{}_sim_one-{}'.format(date, number, alteration))
        assert isinstance(filename, str), 'the filename should be a string'
        assert date in filename, 'the filename should contain the date as part\
    of the serial number'
        assert number in filename, 'the filename should contain the file\
    number as part of the serial number'
        assert isinstance(circuit_configuration, str), 'the circuit\
    configuration should be a string.'
        with open(filename + ".csv", mode='a', newline='') as data_file:
            data_file.write('Date:, {}'.format(date)+'\n')
            data_file.write('Serial number:, {}'.format(number)+'\n')
            data_file.write('Data Source:, simulation'+'\n')
            data_file.write('Circuit type:, -RQ-'+'\n')
            data_file.write('Circuit configuration:, {}'
                            .format(circuit_configuration)+'\n')
            data_file.write('Circuit elements:, [R={} ohm Q={}\
 [s^(alpha-1)/ohm] alpha={}]'.format(R, Q, alpha) + '\n')
            if alteration:
                data_file.write('Alteration :, {} \n'.format(alteration))
            else:
                data_file.write('Alteration :, None', '\n')
            data_file.write('---'+'\n')
            freq_range = circuits.freq_gen(high_freq, low_freq, decades)
            df = RQ_simulation(high_freq, low_freq, decades, R, Q, alpha,
                               circuit_configuration)
            if alteration:
                df = alterations.added_noise(df, 0.4)
            else:
                df = df
            df.to_csv(data_file, mode='a')
            data_file.close()
        with open(filename + ".csv", mode='r', newline='') as data_file:
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
            assert date in rows[0][1], 'the first row of the metadata part\
    of the file should containg the data the file was created'
            assert number in rows[1][1], 'the second row of the metadata part\
    of the file should containg the serial number of the file'
            assert 'Data Source:' in rows[2][0], 'the data source should be\
    part of the metadata of the file'
            assert 'Circuit type:' in rows[3][0], 'the circuit type should\
    be indicated if the '
            assert circuit_configuration in rows[4][1], 'the circuit\
    configuraiton should be indicated in the metadata part of the file'
            assert 'R={}'.format(R) in rows[5][1], 'the circuit elements\
    values should be indicated'
            assert 'Q={}'.format(Q) in rows[5][1], 'the circuit elements\
    values should be indicated'
            assert 'alpha={}'.format(alpha) in rows[5][1], 'the circuit\
 elements values should be indicated'
            assert 'Alteration :' in rows[6], 'Indication of any type of data\
    alteration to the simuation data needs to be inidcated'
            assert '---' in rows[7], 'the three hyphens indicating the break\
    of the metadata part of the files need to be present '
            assert 'freq [Hz]' in rows[8][1], 'the dataframe is not appended\
    to the .csv file just created'
            assert str(freq_range[0][0]) in rows[9][1], 'the dataframe is not\
    appended to the .csv file created'
        os.remove(filename + ".csv")

    def test_RsRCRC_simulation(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        Rs = 100  # ohm
        R1 = 20  # ohm
        R2 = 70  # ohm
        C = 10E-6  # F
        n_points = np.round(decades * np.log10(int(high_freq)) -
                            np.log10(low_freq))
        f_range = circuits.freq_gen(high_freq, low_freq, decades=7)
        circuit = circuits.cir_RsRCRC(f_range[1], Rs, R1, C, R2, C)
        impedance_data = impedance_array(circuit)
        impedance_data_df = to_dataframe(f_range, impedance_data)

        assert isinstance(decades, int), 'the number of decades should be\
 an integer'
        assert high_freq >= low_freq, 'the low frequency should be smaller\
 than the high frequency limit value. Check again.'
        np.testing.assert_almost_equal(len(f_range[1]),
                                       impedance_data[0].shape[0],
                                       decimal=18, err_msg='the impedance\
 is not correclty computed. The number of points in the array is not correct.')
        assert isinstance(impedance_data_df, pd.DataFrame), \
            'The output should be a pandas.DataFrame'
        assert len(f_range[1]) == impedance_data[0].shape[0], 'the\
 frequency and the impedance respons do not match in length. Check again.'
        assert len(impedance_data) == 5, 'the impedance array inputted\
 is not the right dimensions. The number of columns exceed the\
 expected value (5)'
        for item in impedance_data[0][:]:
            assert isinstance(item, complex), 'the first\
 column of the impedance response should be populated by complex numberes'
        assert circuit[0].real == impedance_data[1][0], 'the\
 complex impedance is not separated into its real and imaginary\
 parts correctly.'
        assert circuit[0].imag == impedance_data[2][0], 'the\
 complex impedance is not separated into its real and imaginary parts\
 correctly.'
        assert isinstance(C, float), 'the capacitance should be a float,\
     not an integer'
        assert C <= 1, 'the capacitance value is probably too high.'

    def test_RsRCRC_file_writer(self):

        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        Rs = 100  # ohm
        R1 = 20  # ohm
        R2 = 70  # ohm
        C = 10E-6  # F

        date = time.strftime('%y%m%d', time.localtime())
        assert isinstance(date, str), 'the date should be a string'
        assert len(date) == 6, 'The date string should be 6 characters long'
        save_location = 'simulation_data/'
        assert isinstance(save_location, str)
        i = 1
        assert isinstance(i, int), 'the serial number counters should be an\
 integer'
        assert i >= 1, 'the counter should be a number higher than one'
        alteration = 'noise'
        number = str(i).zfill(4)
        assert len(number) == 4, 'the serial number should be four characters \
 long'
        assert isinstance(alteration, str), 'the alteration argument should be\
 a string'
        filename = str('{}-{}_sim_spread-{}'.format(date, number, alteration))
        assert isinstance(filename, str), 'the filename should be a string'
        assert date in filename, 'the filename should contain the date as part\
 of the serial number'
        assert number in filename, 'the filename should contain the file\
 number as part of the serial number'
        with open(filename + ".csv", mode='a', newline='') as data_file:
            data_file.write('Date:, {}'.format(date)+'\n')
            data_file.write('Serial number:, {}'.format(number)+'\n')
            data_file.write('Data Source:, simulation'+'\n')
            data_file.write('Circuit type:,  -Rs-(RC)-(RC)-'+'\n')
            data_file.write('Circuit elements: , [Rs={} ohm R1={} ohm C1={} F\
    R2={} ohm C2={} F]'.format(Rs, R1, C, R2, C) + '\n')
            if alteration:
                data_file.write('Alteration :, {} \n'.format(alteration))
            else:
                data_file.write('Alteration :, None', '\n')
            data_file.write('---'+'\n')
            freq_range = circuits.freq_gen(high_freq, low_freq, decades)
            df = RsRCRC_simulation(high_freq, low_freq, decades, Rs, R1, C,
                                   R2, C)
            if alteration:
                df = alterations.added_noise(df, 0.4)
            else:
                df = df
            df.to_csv(data_file, mode='a')
            data_file.close()
        with open(filename + ".csv", mode='r', newline='') as data_file:
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
            assert date in rows[0][1], 'the first row of the metadata part\
 of the file should containg the data the file was created'
            assert number in rows[1][1], 'the second row of the metadata part\
 of the file should containg the serial number of the file'
            assert 'Data Source:' in rows[2][0], 'the data source should be\
 part of the metadata of the file'
            assert 'Circuit type:' in rows[3][0], 'the circuit type should\
 be indicated if the '
            assert 'Rs={}'.format(Rs) in rows[4][1], 'the circuit elements\
 values should be indicated'
            assert 'C1={}'.format(C) in rows[4][1], 'the circuit elements\
 values should be indicated'
            assert 'Alteration :' in rows[5], 'Indication of any type of data\
 alteration to the simuation data needs to be inidcated'
            assert '---' in rows[6], 'the three hyphens indicating the break\
 of the metadata part of the files need to be present '
            # print(rows)
            assert 'freq [Hz]' in rows[7][1], 'the dataframe is not appended\
 to the .csv file just created'
            assert str(freq_range[0][0]) in rows[8][1], 'the dataframe is not\
 appended to the .csv file created'
        os.remove(filename + ".csv")

    def test_RsRQRQ_simulation(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        Rs = 100  # ohm
        R1 = 20  # ohm
        R2 = 70  # ohm
        Q = 10E-6  # F
        alpha = 0.75
        n_points = np.round(decades * np.log10(int(high_freq)) -
                            np.log10(low_freq))
        f_range = circuits.freq_gen(high_freq, low_freq, decades=7)
        circuit = circuits.cir_RsRCRC(f_range[1], Rs, R1, Q, alpha, R2,
                                      Q, alpha)
        impedance_data = impedance_array(circuit)
        impedance_data_df = to_dataframe(f_range, impedance_data)

        assert isinstance(decades, int), 'the number of decades should be\
    an integer'
        assert high_freq >= low_freq, 'the low frequency should be smaller\
    than the high frequency limit value. Check again.'
        np.testing.assert_almost_equal(len(f_range[1]),
                                       impedance_data[0].shape[0],
                                       decimal=18, err_msg='the impedance\
 is not correclty computed. The number of points in the array is not correct.')
        assert isinstance(impedance_data_df, pd.DataFrame), \
            'The output should be a pandas.DataFrame'
        assert len(f_range[1]) == impedance_data[0].shape[0], 'the\
    frequency and the impedance respons do not match in length. Check again.'
        assert len(impedance_data) == 5, 'the impedance array inputted\
    is not the right dimensions. The number of columns exceed the\
    expected value (5)'
        for item in impedance_data[0][:]:
            assert isinstance(item, complex), 'the first\
    column of the impedance response should be populated by complex numberes'
        assert circuit[0].real == impedance_data[1][0], 'the\
    complex impedance is not separated into its real and imaginary\
    parts correctly.'
        assert circuit[0].imag == impedance_data[2][0], 'the\
    complex impedance is not separated into its real and imaginary parts\
    correctly.'
        assert isinstance(Q, float), 'the capacitance should be a float,\
     not an integer'
        assert Q <= 1, 'the capacitance value is probably too high.'
        assert alpha <= 1, 'the exponent of the constatn phase element should\
 be a number between 0 and 1'
        assert 0 <= alpha, 'the exponent of the constatn phase element should\
 be a number between 0 and 1'

    def test_RsRQRQ_file_writer(self):

        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        Rs = 100  # ohm
        R1 = 20  # ohm
        R2 = 70  # ohm
        Q = 10E-6  # s^(alpha-1)/ohm
        alpha = 0.75  # [-]

        date = time.strftime('%y%m%d', time.localtime())
        assert isinstance(date, str), 'the date should be a string'
        assert len(date) == 6, 'The date string should be 6 characters long'
        save_location = 'simulation_data/'
        assert isinstance(save_location, str)
        i = 1
        assert isinstance(i, int), 'the serial number counters should be an\
    integer'
        assert i >= 1, 'the counter should be a number higher than one'
        alteration = 'noise'
        number = str(i).zfill(4)
        assert len(number) == 4, 'the serial number should be four characters \
    long'
        assert isinstance(alteration, str), 'the alteration argument should be\
    a string'
        filename = str('{}-{}_sim_two-{}'.format(date, number, alteration))
        assert isinstance(filename, str), 'the filename should be a string'
        assert date in filename, 'the filename should contain the date as part\
    of the serial number'
        assert number in filename, 'the filename should contain the file\
    number as part of the serial number'
        with open(filename + ".csv", mode='a', newline='') as data_file:
            data_file.write('Date:, {}'.format(date)+'\n')
            data_file.write('Serial number:, {}'.format(number)+'\n')
            data_file.write('Data Source:, simulation'+'\n')
            data_file.write('Circuit type:,  -Rs-(RQ)-(RQ)-'+'\n')
            data_file.write('Circuit elements: , [Rs={} ohm R1={} ohm Q1={}\
 [s^(alpha-1)/ohm] alpha_1={} R2={} ohm Q2={} [s^(alpha-1)/ohm]\
 alpha_2={}]'.format(Rs, R1, Q, alpha, R2, Q, alpha) + '\n')
            if alteration:
                data_file.write('Alteration :, {} \n'.format(alteration))
            else:
                data_file.write('Alteration :, None', '\n')
            data_file.write('---'+'\n')
            freq_range = circuits.freq_gen(high_freq, low_freq, decades)
            df = RsRQRQ_simulation(high_freq, low_freq, decades, Rs, R1, Q,
                                   alpha, R2, Q, alpha)
            if alteration:
                df = alterations.added_noise(df, 0.4)
            else:
                df = df
            df.to_csv(data_file, mode='a')
            data_file.close()
        with open(filename + ".csv", mode='r', newline='') as data_file:
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
            assert date in rows[0][1], 'the first row of the metadata part\
    of the file should containg the data the file was created'
            assert number in rows[1][1], 'the second row of the metadata part\
    of the file should containg the serial number of the file'
            assert 'Data Source:' in rows[2][0], 'the data source should be\
    part of the metadata of the file'
            assert 'Circuit type:' in rows[3][0], 'the circuit type should\
    be indicated if the '
            assert 'Rs={}'.format(Rs) in rows[4][1], 'the circuit elements\
    values should be indicated'
            assert 'Q1={}'.format(Q) in rows[4][1], 'the circuit elements\
    values should be indicated'
            assert 'Alteration :' in rows[5], 'Indication of any type of data\
    alteration to the simuation data needs to be inidcated'
            assert '---' in rows[6], 'the three hyphens indicating the break\
    of the metadata part of the files need to be present '
            # print(rows)
            assert 'freq [Hz]' in rows[7][1], 'the dataframe is not appended\
    to the .csv file just created'
            assert str(freq_range[0][0]) in rows[8][1], 'the dataframe is not\
    appended to the .csv file created'
        os.remove(filename + ".csv")

    def test_randles_simulation(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        Rs = 100  # ohm
        R1 = 20  # ohm
        Q = 10E-6  # F
        alpha = 0.75
        sigma = 0.5
        n_points = np.round(decades * np.log10(int(high_freq)) -
                            np.log10(low_freq))
        f_range = circuits.freq_gen(high_freq, low_freq, decades=7)
        circuit = circuits.cir_RsRCRC(f_range[1], Rs, R1,
                                      alpha, sigma, Q)
        impedance_data = impedance_array(circuit)
        impedance_data_df = to_dataframe(f_range, impedance_data)

        assert isinstance(decades, int), 'the number of decades should be\
    an integer'
        assert high_freq >= low_freq, 'the low frequency should be smaller\
    than the high frequency limit value. Check again.'
        np.testing.assert_almost_equal(len(f_range[1]),
                                       impedance_data[0].shape[0],
                                       decimal=18, err_msg='the impedance\
 is not correclty computed. The number of points in the array is not correct.')
        assert isinstance(impedance_data_df, pd.DataFrame), \
            'The output should be a pandas.DataFrame'
        assert len(f_range[1]) == impedance_data[0].shape[0], 'the\
    frequency and the impedance respons do not match in length. Check again.'
        assert len(impedance_data) == 5, 'the impedance array inputted\
    is not the right dimensions. The number of columns exceed the\
    expected value (5)'
        for item in impedance_data[0][:]:
            assert isinstance(item, complex), 'the first\
    column of the impedance response should be populated by complex numberes'
        assert circuit[0].real == impedance_data[1][0], 'the\
    complex impedance is not separated into its real and imaginary\
    parts correctly.'
        assert circuit[0].imag == impedance_data[2][0], 'the\
    complex impedance is not separated into its real and imaginary parts\
    correctly.'
        assert isinstance(Q, float), 'the capacitance should be a float,\
     not an integer'
        assert Q <= 1, 'the capacitance value is probably too high.'
        assert alpha <= 1, 'the exponent of the constatn phase element should\
 be a number between 0 and 1'
        assert 0 <= alpha, 'the exponent of the constatn phase element should\
 be a number between 0 and 1'
        assert sigma <= 1, 'the exponent of the constatn phase element should\
 be a number between 0 and 1'
        assert 0 <= sigma, 'the exponent of the constatn phase element should\
 be a number between 0 and 1'

    def test_randles_file_writer(self):

        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7
        Rs = 100  # ohm
        R1 = 20  # ohm
        R2 = 70  # ohm
        Q = 10E-6  # s^(alpha-1)/ohm
        alpha = 0.75  # [-]
        sigma = 0.5

        date = time.strftime('%y%m%d', time.localtime())
        assert isinstance(date, str), 'the date should be a string'
        assert len(date) == 6, 'The date string should be 6 characters long'
        save_location = 'simulation_data/'
        assert isinstance(save_location, str)
        i = 1
        assert isinstance(i, int), 'the serial number counters should be an\
    integer'
        assert i >= 1, 'the counter should be a number higher than one'
        alteration = 'noise'
        number = str(i).zfill(4)
        assert len(number) == 4, 'the serial number should be four characters \
    long'
        assert isinstance(alteration, str), 'the alteration argument should be\
    a string'
        filename = str('{}-{}_randles_simp-{}'.format(date,
                                                      number, alteration))
        assert isinstance(filename, str), 'the filename should be a string'
        assert date in filename, 'the filename should contain the date as part\
    of the serial number'
        assert number in filename, 'the filename should contain the file\
    number as part of the serial number'
        with open(filename + ".csv", mode='a', newline='') as data_file:
            data_file.write('Date:, {}'.format(date)+'\n')
            data_file.write('Serial number:, {}'.format(number)+'\n')
            data_file.write('Data Source:, simulation'+'\n')
            data_file.write('Circuit type:,  -Rs-(Cdl-(Rct-Zw))-'+'\n')
            data_file.write('Circuit elements:, [Rs={} ohm R1={} ohm Q1={}\
 s^(alpha-1)/ohm alpha_1={} ohm sigma={}]'.format(Rs, R1, Q,
                                                  alpha, sigma) + '\n')
            if alteration:
                data_file.write('Alteration :, {} \n'.format(alteration))
            else:
                data_file.write('Alteration :, None', '\n')
            data_file.write('---'+'\n')
            freq_range = circuits.freq_gen(high_freq, low_freq, decades)
            df = randles_simulation(high_freq, low_freq, decades, Rs, R1,
                                    alpha, sigma, Q)
            if alteration:
                df = alterations.added_noise(df, 0.4)
            else:
                df = df
            df.to_csv(data_file, mode='a')
            data_file.close()
        with open(filename + ".csv", mode='r', newline='') as data_file:
            reader = csv.reader(data_file, delimiter=',')
            rows = [row for row in reader]
            assert date in rows[0][1], 'the first row of the metadata part\
 of the file should containg the data the file was created'
            assert number in rows[1][1], 'the second row of the metadata part\
 of the file should containg the serial number of the file'
            assert 'Data Source:' in rows[2][0], 'the data source should be\
 part of the metadata of the file'
            assert 'Circuit type:' in rows[3][0], 'the circuit type should\
 be indicated if the '
            assert 'Rs={}'.format(Rs) in rows[4][1], 'the circuit elements\
 values should be indicated'
            assert 'Q1={}'.format(Q) in rows[4][1], 'the circuit elements\
 values should be indicated'
            assert 'Alteration :' in rows[5], 'Indication of any type of data\
 alteration to the simuation data needs to be inidcated'
            assert '---' in rows[6], 'the three hyphens indicating the break\
 of the metadata part of the files need to be present '
            # print(rows)
            assert 'freq [Hz]' in rows[7][1], 'the dataframe is not appended\
 to the .csv file just created'
            assert str(freq_range[0][0]) in rows[8][1], 'the dataframe is not\
 appended to the .csv file created'
        os.remove(filename + ".csv")
