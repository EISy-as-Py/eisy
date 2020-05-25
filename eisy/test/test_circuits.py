import numpy as np
import unittest

import eisy.simulation.circuits as circuits


# Define the common variables to be used for as a testing dataset
high_freq = 10**8  # Hz
low_freq = 0.01  # Hz
decades = 10
Resistance = 10
Parallel_Resistance = 100
Capacitance = 10**-6
Constant_phase_element = 10**-6
alpha = 1
sigma = 500

f_range = circuits.freq_gen(high_freq, low_freq, decades)


class TestSimulationTools(unittest.TestCase):

    def test_freq_gen(self):

        f_range = circuits.freq_gen(high_freq, low_freq, decades)

        assert isinstance(decades, int),\
            'the number of decades should be an integer'
        assert high_freq >= low_freq,\
            'the low frequency should be smaller than the high' +\
            'frequency limit value. Check again.'

        assert max(f_range[0])-min(f_range[0]) == high_freq - low_freq, \
            'The frequency range returned is invalid'

        assert len(f_range[0]) == len(f_range[1]), \
            'The output returned is invalid'

    def test_RC_parallel(self):

        response = circuits.cir_RC_parallel(f_range[1], R=Resistance,
                                            C=Capacitance)

        assert np.positive(Resistance), \
            'The input resistance is invalid'
        assert np.positive(Capacitance), \
            'The input capacitance is invalid'
        assert isinstance(Capacitance, float), \
            'the capacitance should be a float, not an integer'
        assert len(response) == len(f_range[1]), \
            'The returned response is not valid'

        for item in response:
            assert isinstance(item, complex),\
                'The returned response includes invalid impedance'

    def test_RC_series(self):

        response = circuits.cir_RC_series(f_range[1], R=Resistance,
                                          C=Capacitance)
        assert np.positive(Resistance), \
            'The input resistance is invalid'
        assert np.positive(Capacitance), \
            'The input capacitance is invalid'
        assert isinstance(Capacitance, float), \
            'the capacitance should be a float, not an integer'
        assert len(response) == len(f_range[1]), \
            'The returned response is not valid'

        for item in response:
            assert isinstance(item, complex),\
                'The returned response includes invalid impedance'

    def test_RQ_parallel(self):

        response = circuits.cir_RQ_parallel(f_range[1], R=Resistance,
                                            Q=Constant_phase_element,
                                            alpha=alpha)
        assert np.positive(Resistance), \
            'The input resistance is invalid'
        assert np.positive(Constant_phase_element), \
            'The input phase element is invalid'
        assert len(response) == len(f_range[1]), \
            'The returned response is not valid'

        for item in response:
            assert isinstance(item, complex), \
                'The returned response includes invalid impedance'

    def test_RQ_series(self):

        response = circuits.cir_RQ_series(f_range[1], R=Resistance,
                                          Q=Constant_phase_element,
                                          alpha=alpha)
        assert np.positive(Resistance), \
            'The input resistance is invalid'
        assert np.positive(Constant_phase_element), \
            'The input phase element is invalid'
        assert len(response) == len(f_range[1]), \
            'The returned response is not valid'

        for item in response:
            assert isinstance(item, complex), \
                'The returned response includes invalid impedance'

    def test_RsRC(self):

        response = circuits.cir_RsRC(f_range[1], Rs=Resistance,
                                     Rp=Parallel_Resistance,
                                     C=Capacitance)

        assert np.positive(Resistance), \
            'The input resistance is invalid'
        assert np.positive(Parallel_Resistance), \
            'The input resistance is invalid'
        assert np.positive(Capacitance),  \
            'The input capacitance is invalid'

        assert len(response) == len(f_range[1]), \
            'The returned response is not valid'

        for item in response:
            assert isinstance(item, complex), \
                'The returned response includes invalid impedance'
            real_Z = item.real
            imag_Z = item.imag
            total_Z = np.sqrt((real_Z**2) + (imag_Z**2))
            assert total_Z > Resistance,\
                'The Impedance value returned is lower than the' +\
                'Solution Resistance'

    def test_RsRQ(self):

        response = circuits.cir_RsRQ(f_range[1], Rs=Resistance,
                                     Rp=Parallel_Resistance,
                                     Q=Constant_phase_element,
                                     alpha=alpha)

        assert np.positive(Resistance), \
            'The input resistance is invalid'
        assert np.positive(Parallel_Resistance), \
            'The input resistance is invalid'
        assert np.positive(Constant_phase_element), \
            'The input phase element is invalid'
        assert len(response) == len(f_range[1]), \
            'The returned response is not valid'

        assert len(response) == len(f_range[1]), \
            'The returned response is not valid'

        for item in response:
            assert isinstance(item, complex), \
                'The returned response includes invalid impedance'
            real_Z = item.real
            imag_Z = item.imag
            total_Z = np.sqrt((real_Z**2) + (imag_Z**2))
            assert total_Z > Resistance,\
                'The Impedance value returned is lower than the' +\
                'Solution Resistance'

    def test_RsRQRQ(self):

        response = circuits.cir_RsRQRQ(f_range[1], Rs=Resistance,
                                       Rp1=Parallel_Resistance,
                                       Q1=Constant_phase_element,
                                       alpha1=alpha,
                                       Rp2=Parallel_Resistance,
                                       Q2=Constant_phase_element,
                                       alpha2=alpha)

        assert np.positive(Resistance), \
            'The input resistance is invalid'
        assert np.positive(Parallel_Resistance), \
            'The input resistance is invalid'
        assert np.positive(Constant_phase_element),  \
            'The input phase element is invalid'
        assert alpha > 0 or alpha <= 1, 'The values of alpha is invalid'
        assert len(response) == len(f_range[1]), \
            'The returned response is not valid'

        for item in response:
            assert isinstance(item, complex), \
                'The returned response includes invalid impedance'
            real_Z = item.real
            imag_Z = item.imag
            total_Z = np.sqrt((real_Z**2) + (imag_Z**2))
            assert total_Z > Resistance, \
                'The Impedance value returned is lower than the' +\
                'Solution Resistance'

    def test_RsRCRC(self):

        response = circuits.cir_RsRCRC(f_range[1], Rs=Resistance,
                                       Rp1=Parallel_Resistance,
                                       C1=Capacitance,
                                       Rp2=Parallel_Resistance,
                                       C2=Capacitance)
        assert np.positive(Resistance), \
            'The input resistance is invalid'
        assert np.positive(Parallel_Resistance), \
            'The input resistance is invalid'
        assert np.positive(Capacitance),  \
            'The input capacitance is invalid'

        assert len(response) == len(f_range[1]), \
            'The returned response is not valid'

        for item in response:
            assert isinstance(item, complex), \
                'The returned response includes invalid impedance'
            real_Z = item.real
            imag_Z = item.imag
            total_Z = np.sqrt((real_Z**2) + (imag_Z**2))
            assert total_Z > Resistance,\
                'The Impedance value returned is lower than the' +\
                'Solution Resistance'

    def test_randles(self):

        response = circuits.cir_Randles_simplified(f_range[1],
                                                   Rs=Resistance,
                                                   Rp=Parallel_Resistance,
                                                   alpha=alpha,
                                                   sigma=sigma,
                                                   Q=Constant_phase_element)

        assert np.positive(Resistance), \
            'The input resistance is invalid'
        assert np.positive(Parallel_Resistance), \
            'The input resistance is invalid'
        assert alpha > 0 or alpha <= 1, \
            'The values of alpha is nonpositive'
        assert np.positive(Constant_phase_element), \
            'The input constant phase element is non-positive'
        assert np.positive(sigma), 'The input coefficient is non-positive'

        assert len(response) == len(f_range[1]),\
            'The returned response is not valid'

        for item in response:
            assert isinstance(item, complex), \
                'The returned response includes invalid impedance'
            real_Z = item.real
            imag_Z = item.imag
            total_Z = np.sqrt((real_Z**2) + (imag_Z**2))
            assert total_Z > Resistance, \
                'The Impedance value returned is lower than the' +\
                'Solution Resistance'
