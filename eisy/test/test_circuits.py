import os
import sys
import csv
import time
import unittest


module_path = os.path.abspath(os.path.join('../data/simulation'))
if module_path not in sys.path:
    sys.path.append(module_path)

import eisy.data.simulation.circuits as circuits

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


    #def test_rc_circuit(self):

