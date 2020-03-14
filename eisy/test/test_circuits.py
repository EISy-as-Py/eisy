import os
import sys
import csv
import time
import unittest

module_path = os.path.abspath(os.path.join('../data/simulation'))
if module_path not in sys.path:
    sys.path.append(module_path)

import eisy.simulation.circuits as circuits

import numpy as np
import pandas as pd


class TestSimulationTools(unittest.TestCase):

    def test_freq_gen(self):

        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7

        assert isinstance(decades, int),\
            'the number of decades should be an integer'
        assert high_freq >= low_freq,\
            'the low frequency should be smaller than the high\
             frequency limit value. Check again.'

        f_range = circuits.freq_gen(high_freq, low_freq, decades)

        assert max(f_range[0])-min(f_range[0]) == high_freq - low_freq, \
            'The frequency range returned is invalid'

        assert len(f_range[0]) == len(f_range[1]), \
            'The output returned is invalid'

    def test_rc_parallel(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7

        assert isinstance(decades, int),\
            'The number of decades should be an integer'
        assert high_freq >= low_freq,\
            'The low frequency should be smaller than the high\
             frequency limit value. Check again.'

        f_range = circuits.freq_gen(high_freq, low_freq, decades)

        Resistance = 10
        Capacitance = 10**-6

        assert np.positive(Resistance), 'The input resistance\
            is invalid'
        assert np.positive(Capacitance), 'The input capacitance\
            is invalid'

        response = circuits.cir_RC_parallel(f_range[1], Resistance,
                                            Capacitance)

        assert len(response) == len(f_range[1]), 'The returned response\
            is not valid'

        for item in response:
            assert isinstance(item, complex), 'The returned response\
                includes invalid impedance'

    def test_rc_series(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7

        assert isinstance(decades, int),\
            'The number of decades should be an integer'
        assert high_freq >= low_freq,\
            'The low frequency should be smaller than the high\
             frequency limit value. Check again.'

        f_range = circuits.freq_gen(high_freq, low_freq, decades)

        Resistance = 10
        Capacitance = 10**-6

        assert np.positive(Resistance), 'The input resistance\
            is invalid'
        assert np.positive(Capacitance), 'The input capacitance\
            is invalid'

        response = circuits.cir_RC_series(f_range[1], Resistance,
                                          Capacitance)

        assert len(response) == len(f_range[1]), 'The returned response\
            is not valid'

        for item in response:
            assert isinstance(item, complex), 'The returned response\
                includes invalid impedance'

    def test_RQ_parallel(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7

        assert isinstance(decades, int),\
            'The number of decades should be an integer'
        assert high_freq >= low_freq,\
            'The low frequency should be smaller than the high\
             frequency limit value. Check again.'

        f_range = circuits.freq_gen(high_freq, low_freq, decades)

        Resistance = 10
        Constant_phase_element = 10**-6
        alpha = 1

        assert np.positive(Resistance), 'The input resistance\
            is invalid'
        assert np.positive(Constant_phase_element), 'The input phase element\
            is invalid'

        response = circuits.cir_RQ_parallel(f_range[1], Resistance,
                                            Constant_phase_element, alpha)

        assert len(response) == len(f_range[1]), 'The returned response\
            is not valid'

        for item in response:
            assert isinstance(item, complex), 'The returned response\
                includes invalid impedance'

    def test_RQ_series(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7

        assert isinstance(decades, int),\
            'The number of decades should be an integer'
        assert high_freq >= low_freq,\
            'The low frequency should be smaller than the high\
             frequency limit value. Check again.'

        f_range = circuits.freq_gen(high_freq, low_freq, decades)

        Resistance = 10
        Constant_phase_element = 10**-6
        alpha = 1

        assert np.positive(Resistance), 'The input resistance\
            is invalid'
        assert np.positive(Constant_phase_element), 'The input phase element\
            is invalid'

        response = circuits.cir_RQ_series(f_range[1], Resistance,
                                          Constant_phase_element, alpha)

        assert len(response) == len(f_range[1]), 'The returned response\
            is not valid'

        for item in response:
            assert isinstance(item, complex), 'The returned response\
                includes invalid impedance'

    def test_RsRC(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7

        assert isinstance(decades, int),\
            'The number of decades should be an integer'
        assert high_freq >= low_freq,\
            'The low frequency should be smaller than the high\
             frequency limit value. Check again.'

        f_range = circuits.freq_gen(high_freq, low_freq, decades)

        Solution_Resistance = 10
        Parallel_Resistance = 100
        Capacitance = 10**-6

        assert np.positive(Solution_Resistance), 'The input resistance\
            is invalid'
        assert np.positive(Parallel_Resistance), 'The input resistance\
            is invalid'
        assert np.positive(Capacitance), 'The input capacitance\
            is invalid'

        response = circuits.cir_RQ_series(f_range[1], Solution_Resistance,
                                          Parallel_Resistance, Capacitance)

        assert len(response) == len(f_range[1]), 'The returned response\
            is not valid'

        for item in response:
            assert isinstance(item, complex), 'The returned response\
                includes invalid impedance'
            real_Z = item.real
            imag_Z = item.imag
            total_Z = np.sqrt((real_Z**2) + (imag_Z**2))
            assert total_Z > Solution_Resistance, 'The Impedance value\
                returned is lower than the Solution Resistance'

    def test_RsRQRQ(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7

        assert isinstance(decades, int),\
            'The number of decades should be an integer'
        assert high_freq >= low_freq,\
            'The low frequency should be smaller than the high\
             frequency limit value. Check again.'

        f_range = circuits.freq_gen(high_freq, low_freq, decades)

        Solution_Resistance = 10
        Parallel_Resistance_1 = 100
        Parallel_Resistance_2 = 100
        Constant_phase_element_1 = 10**-6
        Constant_phase_element_2 = 10**-6
        alpha_1 = 1
        alpha_2 = 1

        assert np.positive(Solution_Resistance), 'The input resistance\
            is invalid'
        assert np.positive(Parallel_Resistance_1), 'The input resistance\
            is invalid'
        assert np.positive(Parallel_Resistance_2), 'The input resistance\
            is invalid'
        assert np.positive(Constant_phase_element_1), 'The input cnstant\
            phase element is invalid'
        assert np.positive(Constant_phase_element_2), 'The input contant\
            phase element is invalid'
        assert alpha_1 > 0 or alpha_1 <= 1, 'The values of alpha is invalid'
        assert alpha_2 > 0 or alpha_2 <= 1, 'The values of alpha is invalid'

        response = circuits.cir_RsRQRQ(f_range[1], Solution_Resistance,
                                       Parallel_Resistance_1,
                                       Constant_phase_element_1, alpha_1,
                                       Parallel_Resistance_2,
                                       Constant_phase_element_2, alpha_2)

        assert len(response) == len(f_range[1]), 'The returned response\
            is not valid'

        for item in response:
            assert isinstance(item, complex), 'The returned response\
                includes invalid impedance'
            real_Z = item.real
            imag_Z = item.imag
            total_Z = np.sqrt((real_Z**2) + (imag_Z**2))
            assert total_Z > Solution_Resistance, 'The Impedance value\
                returned is lower than the Solution Resistance'

    def test_RsRCRC(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7

        assert isinstance(decades, int),\
            'The number of decades should be an integer'
        assert high_freq >= low_freq,\
            'The low frequency should be smaller than the high\
             frequency limit value. Check again.'

        f_range = circuits.freq_gen(high_freq, low_freq, decades)

        Solution_Resistance = 10
        Parallel_Resistance_1 = 100
        Parallel_Resistance_2 = 100
        Capacitance_1 = 10**-6
        Capacitance_2 = 10**-6

        assert np.positive(Solution_Resistance), 'The input resistance\
            is invalid'
        assert np.positive(Parallel_Resistance_1), 'The input resistance\
            is invalid'
        assert np.positive(Parallel_Resistance_2), 'The input resistance\
            is invalid'
        assert np.positive(Capacitance_1), 'The input capacitance\
            is invalid'
        assert np.positive(Capacitance_2), 'The input capacitance\
            is invalid'

        response = circuits.cir_RsRCRC(f_range[1], Solution_Resistance,
                                       Parallel_Resistance_1,
                                       Capacitance_1,
                                       Parallel_Resistance_2,
                                       Capacitance_2)

        assert len(response) == len(f_range[1]), 'The returned response\
            is not valid'

        for item in response:
            assert isinstance(item, complex), 'The returned response\
                includes invalid impedance'
            real_Z = item.real
            imag_Z = item.imag
            total_Z = np.sqrt((real_Z**2) + (imag_Z**2))
            assert total_Z > Solution_Resistance, 'The Impedance value\
                returned is lower than the Solution Resistance'

    def test_randles(self):
        high_freq = 10**8  # Hz
        low_freq = 0.01  # Hz
        decades = 7

        assert isinstance(decades, int),\
            'The number of decades should be an integer'
        assert high_freq >= low_freq,\
            'The low frequency should be smaller than the high\
             frequency limit value. Check again.'

        f_range = circuits.freq_gen(high_freq, low_freq, decades)

        Solution_Resistance = 10
        Parallel_Resistance = 100
        alpha = 1
        Constant_phase_element = 10**-6
        sigma = 500

        assert np.positive(Solution_Resistance), 'The input resistance\
            is non-positive'
        assert np.positive(Parallel_Resistance), 'The input resistance\
            is non-positive'
        assert alpha > 0 or alpha <= 1, 'The values of alpha is\
             nonpositive'
        assert np.positive(Constant_phase_element), 'The input constant\
            phase element is non-positive'
        assert np.positive(sigma), 'The input coefficient is non-positive'

        response = circuits.cir_Randles_simplified(f_range[1],
                                                   Solution_Resistance,
                                                   Parallel_Resistance,
                                                   alpha,
                                                   sigma,
                                                   Constant_phase_element)

        assert len(response) == len(f_range[1]), 'The returned response\
            is not valid'

        for item in response:
            assert isinstance(item, complex), 'The returned response\
                includes invalid impedance'
            real_Z = item.real
            imag_Z = item.imag
            total_Z = np.sqrt((real_Z**2) + (imag_Z**2))
            assert total_Z > Solution_Resistance, 'The Impedance value\
                returned is lower than the Solution Resistance'
