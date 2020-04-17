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

        assert dataframe.columns[0] == 'freq [Hz]', 'the first column should\
 contain the frequency respose.'
        assert dataframe.columns[1] == 'angular_freq [1/s]', 'the second\
 column should contain the angular frequency respose.'
        assert dataframe.columns[2] == 'Re_Z [ohm]', 'the fourth column should\
 contain the real impedance part.'
        assert dataframe.columns[3] == 'Im_Z [ohm]', 'the fifth column\
 should contain the imaginary impedance part.'
        assert dataframe.columns[4] == '|Z| [ohm]', 'the sixth column\
 should contain the magnitude of the impedance.'
        assert dataframe.columns[5] == 'phase_angle [rad]', 'the seventh\
 column should contain the phase angle of the impedance.'
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

    def test_circuit_simulation(self):
        high_freq = 10**6  # Hz
        low_freq = 0.01  # Hz
        R = 100  # ohm
        C = 10E-6  # F
        n_points = np.round(decades * (np.log10(int(high_freq)) -
                            np.log10(low_freq)))
        f_range = circuits.freq_gen(high_freq, low_freq, decades=10)
        circuit_name = 'RC_parallel'
        impedance_data = circuit_simulation(freq_range, circuit_name, C=C, R=R)

        assert isinstance(circuit_name, str), 'the circuit name should be +\
        inputted as a string'
        assert isinstance(impedance_data, pd.DataFrame), \
            'The output should be a pandas.DataFrame'
        assert isinstance(C, float), 'the capacitance should be a float, +\
                                      not an integer'
        assert C <= 1, 'the capacitance value is probably too high.'
