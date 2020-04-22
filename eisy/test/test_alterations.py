import numpy as np
import pandas as pd
import unittest


import eisy.simulation.alterations as alterations
import eisy.simulation.circuits as circuits
import eisy.simulation.data_simulation as data_simulation


# Define the dataframe to use as a testing set.

high_freq = 10**6
low_freq = 0.01
decades = 10
freq_range = circuits.freq_gen(high_freq, low_freq, decades)
Rs = 100  # ohm
C = 25E-6  # F
circuit_response = data_simulation.circuit_simulation(freq_range,
                                                      'RC_parallel',
                                                      R=Rs, C=C)


class TestSimulationTools(unittest.TestCase):

    def test_imag_noise(self):
        noisescale = 0.5
        noisy_dataframe = alterations.imag_noise(circuit_response, noisescale)

        assert isinstance(noisescale, (int, float, np.int32, np.float64)), \
            'the noiscale should be a number'
        assert isinstance(circuit_response, pd.DataFrame), \
            'the input data should be contained in a pandas dataframe'
        assert isinstance(noisy_dataframe, pd.DataFrame), \
            'the output should be a pandas dataframe'
        assert 'Im_Z_noise [ohm]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'

    def test_real_noise(self):
        noisescale = 0.5
        noisy_dataframe = alterations.real_noise(circuit_response, noisescale)

        assert isinstance(noisescale, (int, float, np.int32, np.float64)), \
            'the noiscale should be a number'
        assert isinstance(circuit_response, pd.DataFrame), \
            'the input data should be contained in a pandas dataframe'
        assert isinstance(noisy_dataframe, pd.DataFrame), \
            'the output should be a pandas dataframe'
        assert 'Re_Z_noise [ohm]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'

    def test_freq_noise(self):
        noisescale = 0.5
        noisy_dataframe = alterations.freq_noise(circuit_response, noisescale)

        assert isinstance(noisescale, (int, float, np.int32, np.float64)), \
            'the noiscale should be a number'
        assert isinstance(circuit_response, pd.DataFrame), \
            'the input data should be contained in a pandas dataframe'
        assert isinstance(noisy_dataframe, pd.DataFrame), \
            'the output should be a pandas dataframe'
        assert 'freq_noise [Hz]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'
        assert 'angular_freq_noise [1/s]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'

    def test_complex_noise(self):
        noisescale = 0.5
        noisy_dataframe = alterations.complex_noise(circuit_response,
                                                    noisescale)

        assert isinstance(noisescale, (int, float, np.int32, np.float64)), \
            'the noiscale should be a number'
        assert isinstance(circuit_response, pd.DataFrame), \
            'the input data should be contained in a pandas dataframe'
        assert isinstance(noisy_dataframe, pd.DataFrame), \
            'the output should be a pandas dataframe'
        assert 'Re_Z_noise [ohm]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'
        assert 'Im_Z_noise [ohm]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'

    def test_current_noise(self):
        noisescale = 0.5
        voltage_amplitude = 0.02  # V
        noisy_dataframe = alterations.current_noise(circuit_response,
                                                    noisescale,
                                                    voltage_amplitude)

        assert isinstance(noisescale, (int, float, np.int32, np.float64)), \
            'the noiscale should be a number'
        assert isinstance(voltage_amplitude, (int, float, np.int32, np.float64)
                          ), 'the voltage amplitude should be a number'
        assert isinstance(circuit_response, pd.DataFrame), \
            'the input data should be contained in a pandas dataframe'
        assert isinstance(noisy_dataframe, pd.DataFrame), \
            'the output should be a pandas dataframe'
        assert 'Re_Z_noise [ohm]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'
        assert 'Im_Z_noise [ohm]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'

    def test_voltage_noise(self):
        noisescale = 0.5
        voltage_amplitude = 0.02  # V
        noisy_dataframe = alterations.voltage_noise(circuit_response,
                                                    noisescale,
                                                    voltage_amplitude)

        assert isinstance(noisescale, (int, float, np.int32, np.float64)), \
            'the noiscale should be a number'
        assert isinstance(voltage_amplitude, (int, float, np.int32, np.float64)
                          ), 'the voltage amplitude should be a number'
        assert isinstance(circuit_response, pd.DataFrame), \
            'the input data should be contained in a pandas dataframe'
        assert isinstance(noisy_dataframe, pd.DataFrame), \
            'the output should be a pandas dataframe'
        assert 'Re_Z_noise [ohm]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'
        assert 'Im_Z_noise [ohm]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'

    def test_iv_noise(self):
        noisescale = 0.5
        voltage_amplitude = 0.02  # V
        noisy_dataframe = alterations.iv_noise(circuit_response,
                                               noisescale,
                                               voltage_amplitude)

        assert isinstance(noisescale, (int, float, np.int32, np.float64)), \
            'the noiscale should be a number'
        assert isinstance(voltage_amplitude, (int, float, np.int32, np.float64)
                          ), 'the voltage amplitude should be a number'
        assert isinstance(circuit_response, pd.DataFrame), \
            'the input data should be contained in a pandas dataframe'
        assert isinstance(noisy_dataframe, pd.DataFrame), \
            'the output should be a pandas dataframe'
        assert 'Re_Z_noise [ohm]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'
        assert 'Im_Z_noise [ohm]' in list(noisy_dataframe), \
            'the computed noisy data was not saved in the dataframe'

    def test_normalize(self):
        to_normalized = circuit_response['Re_Z [ohm]']
        normalized_array = alterations.normalize(to_normalized)
        assert isinstance(to_normalized, (pd.core.series.Series, np.ndarray)),\
            'the input of the normalization function should be an array or' +\
            'a pandas dataframe'
        assert 0 <= min(normalized_array), \
            'the lower limit of the normalized array should be zero'
        np.testing.assert_almost_equal(max(normalized_array),
                                       1, decimal=18, err_msg='the ormalized \
                                       array is nto correclty computed.')
