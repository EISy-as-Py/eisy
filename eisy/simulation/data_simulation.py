import numpy as np
import pandas as pd

from . import circuits
from . import alterations


def to_dataframe(freq_range, impedance_array, alteration=None,
                 noisescale=None, **kwargs):
    """ Function returning a df with impedance and frequency data

    Function that creates a dataframe containing impedance data and the
    frequency range used to determine the impedance respose.

    Parameters
    ----------
    freq_range : array-like
                an array containing the frequency and angular frequency values
                used to determine the corresponding impedance response.
                freq_range[0]- the frequency response [Hz]
                freq_range[1]- the angualr frequncy [1/s]
    impedance_array: array-like
                     an array containng the different parts of the impedance
                     response just investigated. The expected content of the
                     array should be: complex impedance, Re and Im parts,
                     magnitude and phase angle of the complex impedance.
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    noisescale : float
                 Scale of the noise added to the data. This number should be
                 contained betweed 0 and 1.

    Returns
    ----------
    impedance_response_df: pandas.DataFrame
                           pandas dataframe containing frequency and imepedance
                           data. Columns are labeled based on the dictionary's
                           keys.
    """

    np.testing.assert_almost_equal(len(freq_range[1]),
                                   impedance_array[0].shape[0], decimal=18,
                                   err_msg='the impedance is not correclty\
                                   computed. The number of points in the\
                                   array is not correct.')
    assert len(freq_range[1]) == impedance_array[0].shape[0], 'the frequency\
and the impedance respons do not match in length. '
    assert len(impedance_array) == 5, 'the impedance array inputted is not\
the right dimensions. The number of columns exceed the expected value (5)'
    assert isinstance(impedance_array[0][1], complex), 'the first column of\
the impedance response should be populated by complex numberes'
    # Create a dictionary containng the keys and values of data to be
    # converted ina pandas dataframe. The 'keys' will be used as column names.
    impedance_dict = {'freq [Hz]': freq_range[0],
                      'angular_freq [1/s]': freq_range[1],
                      'complex_Z [ohm]': impedance_array[0],
                      'Re_Z [ohm]': impedance_array[1],
                      'Im_Z [ohm]': impedance_array[2],
                      '|Z| [ohm]': impedance_array[3],
                      'phase_angle [rad]': impedance_array[4]}
    if kwargs:
        for key, value in kwargs.items():
            if key not in impedance_dict:
                impedance_dict[key] = value
    impedance_response_df = pd.DataFrame(impedance_dict)
    if alteration:
        noise_function = getattr(alterations, alteration)
        impedance_response_df = noise_function(impedance_response_df,
                                               noisescale)

    return impedance_response_df


def impedance_array(complex_impedance):
    ''' Function that breaks the impedance in its real and imaginary parts

    Function that breaks the complex impedance in its real and imaginary
    components. It also calculates the magnitude of the impedance, as well
    as its phase angle.

    Parameters
    ----------
    complez_impedance: array-like
                       the impedance in its complex form [ohm]

    Returns
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


def circuit_simulation(freq_range, circuit_name, alteration=None,
                       noisescale=None, **circuit_elements):
    '''Function that returns a df containing simualated impedance data

    Function that takes imputs parameters to simulated the impedance response
    of a circuit over the indicated frequency range.
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
    circuit_elements : dictionary or keyword arguments
                       input argument composed by the circuit elements
                       composing the called circuit. Refer to the circuits
                       module for the correct list of arguments that can be
                       added to this input.

    Returns
    ----------
    impedance_data_df: pandas.DataFrame
                           pandas dataframe containing frequency and imepedance
                           data.
    '''

    circuit_function_name = 'cir_' + circuit_name
    # make sure the correct number of inputs is given based on teh crcuit name
    # provided
    assert isinstance(circuit_name, str), 'the circuit name should be a string'

    if circuit_name.split('_')[0] == 'RC':
        assert len(circuit_elements) == 2, 'the number of circuit\
elements should be 2'
    if circuit_name.split('_')[0] == 'RQ':
        assert len(circuit_elements) == 3, 'the number of circuit\
elements should be 3'
    if circuit_name == 'RsRC':
        assert len(circuit_elements) == 3, 'the number of circuit\
elements should be 3'
    if circuit_name == 'RsRCRC':
        assert len(circuit_elements) == 5, 'the number of circuit\
elements should be 5'
    if circuit_name == 'RsRQRQ':
        assert len(circuit_elements) == 7, 'the number of circuit\
elements should be 7'
    if circuit_name == 'Randles':
        assert len(circuit_elements) == 5, 'the number of circuit\
elements should be 5'

    circuit_function = getattr(circuits, circuit_function_name)

    assert circuit_function != 0, 'The function could not be found in the\
indicated module.'

    complex_impedance = circuit_function(freq_range[1], **circuit_elements)

    impedance_data = impedance_array(complex_impedance)
    impedance_data_df = to_dataframe(freq_range, impedance_data,
                                     alteration=alteration,
                                     noisescale=noisescale)
    if alteration == 'freq_noise':
        complex_impedance_noise = circuit_function(
                                impedance_data_df['angular_freq_noise [1/s]'],
                                **circuit_elements)
        impedance_data_df['Im_Z_noise [ohm]'] = \
            complex_impedance_noise.to_numpy().imag
        impedance_data_df['Re_Z_noise [ohm]'] = \
            complex_impedance_noise.to_numpy().real
    return impedance_data_df
