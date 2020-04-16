import numpy as np


def freq_gen(high_freq, low_freq, decades=10):
    '''
    Function that generates the frequency range used to investigate the
    impedance response of an electrical circuit Frequency Generator with
    logspaced freqencies

    Parameters
    ----------
    high_freq : single value (int or float)
                initial frequency value (high frequency domain) [Hz]
    high_freq : single value (int or float)
                final frequency value (low frequency domain) [Hz]
    decades : integer
              number of frequency decades to be used as range. Default value
              is set to be 10 [-]

    Returns
    ----------
    [0] = frequency range [Hz]
    [1] = Angular frequency range [1/s]
    '''
    f_decades = int(np.log10(int(high_freq)) - np.log10(low_freq))
    f_range = np.logspace(np.log10(int(high_freq)), np.log10(low_freq),
                          np.around(decades*f_decades), endpoint=True)
    w_range = 2 * np.pi * f_range
    return f_range, w_range


def cir_RC_parallel(angular_freq, **circuit_elements):
    '''
    Function that simulates the impedance response of a resistor and a
    capacitor in a parallel configuration.
    String representation for this circuit: -(RC)-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]

   **circuit_elements : dictionary or keyword arguments

        resistance : single value (int or float)
                     Solution resistance [ohm]
        capacitance : single value (int or float)
                      Capacitance of an electrode surface [F]

    Returns
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [ohm]
    '''
    circuit_string = '-(RC)-'
    # define the elements from the input dictionary
    if len(circuit_elements) != 2:
        raise AssertionError('The wrong number of circuit elements was+\
                              inputted')
    resistance = circuit_elements['R']
    capacitance = circuit_elements['C']
    # compute the impedance response as a complex array
    Z_complex = (resistance/(1+resistance*capacitance*(angular_freq*1j)))
    return Z_complex


def cir_RC_series(angular_freq, **circuit_elements):
    '''
    Function that simulates the impedance response of a resistor and a
    capacitor in a series configuration.
    This circuit configuration is used to simulate the response of an ideally
    polarizable electrode, also known as a blocking electrode.
    String representation for this circuit: -R-C-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]

    **circuit_elements : dictionary or keyword arguments

        resistance : single value (int or float)
                     Solution resistance [ohm]
        capacitance : single value (int or float)
                      Capacitance of an electrode surface [F]

    Returns
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [ohm]
    '''
    circuit_string = '-RC-'

    if len(circuit_elements) != 2:
        raise AssertionError('The wrong number of circuit elements was+\
                              inputted')
    resistance = circuit_elements['R']
    capacitance = circuit_elements['C']
    # compute the impedance response as a complex array
    Z_complex = resistance + 1/(capacitance*(angular_freq*1j))
    return Z_complex


def cir_RQ_parallel(angular_freq, **circuit_elements):
    '''
    Function that simulates the impedance response of a resistor and a
    constant phase element in a parallel configuration.
    String representation for this circuit: -(RQ)-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]

   **circuit_elements : dictionary or keyword arguments

        resistance : single value (int or float)
                       Solution resistance [Ohm]
        constant_phase_element : single value (int or float)
                                 Constant phase angle [s^(alpha-1)/ohm]
        alpha : single value -float
                Exponent of the constant phase element. Should be a value
                between 0 and 1 [-]

    Returns
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
    '''
    circuit_string = '-(RQ)-'
    if len(circuit_elements) != 3:
        raise AssertionError('The wrong number of circuit elements was+\
                              inputted')
    resistance = circuit_elements['R']
    constant_phase_element = circuit_elements['Q']
    alpha = circuit_elements['alpha']

    # compute the impedance response as a complex array
    Z_complex = (resistance/(1+resistance*constant_phase_element*(
                 angular_freq*1j)**alpha))
    return Z_complex


def cir_RQ_series(angular_freq, **circuit_elements):
    '''
    Function that simulates the impedance response of a resistor and a
    constant phase element in a series configuration.
    This circuit configuration is used to simulate the response of a
    blocking electrode with distribution of reactivity.
    String representation for this circuit: -R-Q-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]

    **circuit_elements : dictionary or keyword arguments

        resistance : single value (int or float)
                     Solution resistance [ohm]
        constant_phase_element : single value (int or float)
                                 Constant phase angle [s^(alpha-1)/ohm]
        alpha : single value -float
                Exponent of the constant phase element. Should be a value
                between 0 and 1 [-]

    Returns
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Oom]
    '''
    circuit_string = '-R-Q-'

    if len(circuit_elements) != 3:
        raise AssertionError('The wrong number of circuit elements was+\
                              inputted')
    resistance = circuit_elements['R']
    constant_phase_element = circuit_elements['Q']
    alpha = circuit_elements['alpha']
    # compute the impedance response as a complex array
    Z_complex = resistance + 1/(constant_phase_element*(
                                angular_freq*1j)**alpha)
    return Z_complex


def cir_RsRC(angular_freq, **circuit_elements):
    ''''
    Function that simulates the impedance response of a solution resistor in
    series with a resistor in parallel with a capacitor.
    This circuit configuration is used to simulate the response of an ideally
    polarizable electrode, also known as a blocking electrode.
    String representation for this circuit: -Rs-(RC)-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]

    **circuit_elements : dictionary or keyword arguments

        solution_resistance : single value (int or float)
                              Solution resistance [ohm]
        parallel_resistance : single value (int or float)
                              resistance of the element in parallel with
                              the capacitor [ohm]
        capacitance : single value (int or float)
                      Capacitance of an electrode surface [F]

    Returns
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
    '''
    circuit_string = '-Rs-(RC)-'

    if len(circuit_elements) != 3:
        raise AssertionError('The wrong number of circuit elements was+\
                              inputted')
    solution_resistance = circuit_elements['Rs']
    parallel_resistace = circuit_elements['Rp']
    capacitance = circuit_elements['C']

    # compute the impedance response as a complex array
    Z_parallel = (parallel_resistance/(1 + parallel_resistance *
                                       capacitance * (angular_freq*1j)))
    Z_complex = solution_resistance + Z_parallel
    return Z_complex


def cir_RsRQRQ(angular_freq, **circuit_elements):
    '''
    Function that simulates the impedance response of a solution resistor in
    series with two sets of a resistor in parallel with a constant phase
    elements.
    String representation for this circuit: -Rs-(RQ)-(RQ)-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]


   **circuit_elements : dictionary or keyword arguments

        solution_resistance : single value (int or float)
                              Solution resistance [ohm]
        parallel_resistance_1 : single value (int or float)
                                first combination of resistor in parallel with
                                constant phase element [ohm]
        constant_phase_element_1 : single value (int or float)
                                   First constant phas angle [s^(alpha-1)/ohm]
        alpha_1 : single value -float
                  Exponent of the first constant phase element.
                  Should be a value between 0 and 1 [-]
        parallel_resistance_2 : single value (int or float)
                                Second combination of resistor in parallel with
                                constant phase element [ohm]
        constant_phase_element_2 : single value (int or float)
                                  Second Constant phase angle [s^(alpha-1)/ohm]
        alpha_2 : single value -float
                  Exponent of the second constant phase element.
                  Should be a value between 0 and 1 [-]

    Returns
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
    '''
    circuit_string = '-Rs-(RQ)-(RQ)-'

    if len(circuit_elements) != 7:
        raise AssertionError('The wrong number of circuit elements was+\
                              inputted')
    solution_resistance = circuit_elements['Rs']
    parallel_resistance_1 = circuit_elements['Rp1']
    constant_phase_element_1 = circuit_elements['Q1']
    alpha_1 = circuit_elements['alpha1']
    parallel_resistance_2 = circuit_elements['Rp2']
    constant_phase_element_2 = circuit_elements['Q2']
    alpha_2 = circuit_elements['alpha2']

    # compute the impedance response as a complex array
    Z_parallel_1 = (parallel_resistance_1 /
                    (1+parallel_resistance_1*constant_phase_element_1
                     * (angular_freq*1j)**alpha_1))
    Z_parallel_2 = (parallel_resistance_2 /
                    (1+parallel_resistance_2*constant_phase_element_2
                     * (angular_freq*1j)**alpha_2))
    Z_complex = solution_resistance + Z_parallel_1 + Z_parallel_2

    return Z_complex


def cir_RsRCRC(angular_freq, **circuit_elements):
    '''
    Function that simulates the impedance response of a solution resistor in
    series with two sets of a resistor in parallel with a capacitor.
    String representation for this circuit: -Rs-(RC)-(RC)-


    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]

    **circuit_elements : dictionary or keyword arguments

        solution_resistance : single value (int or float)
                              Solution resistance [ohm]
        parallel_resistance_1 : single value (int or float)
                                first combination of resistor in parallel with
                                capacitor [ohm]
        capacitance_1 : single value (int or float)
                        Capacitance of an electrode surface whichi is part of
                         the first combination of RC in parallel [F]
        parallel_resistance_2 : single value (int or float)
                                second combination of resistor in parallel with
                                capacitor [ohm]
        capacitance_2 : single value (int or float)
                        Capacitance of an electrode surface whichi is part of
                        the second combination of RC in parallel [F]

    Returns
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
    '''
    circuit_string = '-Rs-(RC)-(RC)-'

    if len(circuit_elements) != 5:
        raise AssertionError('The wrong number of circuit elements was+\
                              inputted')
    solution_resistance = circuit_elements['Rs']
    parallel_resistance_1 = circuit_elements['Rp1']
    capacitance_1 = circuit_elements['C1']
    parallel_resistance_2 = circuit_elements['Rp2']
    capacitance_2 = circuit_elements['C2']

    # compute the impedance response as a complex array
    Z_parallel_1 = (parallel_resistance_1/(1 + parallel_resistance_1 *
                                           capacitance_1*(angular_freq*1j)))
    Z_parallel_2 = (parallel_resistance_2/(1 + parallel_resistance_2 *
                                           capacitance_2*(angular_freq*1j)))
    Z_complex = solution_resistance + Z_parallel_1 + Z_parallel_2

    return Z_complex


def cir_Randles_simplified(angular_freq, **circuit_elements):
    '''
    Return the impedance of a Randles circuit with a simplified Warburg element
    This form of the Randles circuit is only meant for to simulate
    semi-infinate linear diffusion
    String representation for this circuit: -Rs-(Q-(RW)-)-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]

    **circuit_elements : dictionary or keyword arguments

        solution_resistance : single value (int or float)
                              Solution resistance [ohm]
        parallel_resistance : single value (int or float)
                              resistance of the element in parallel with
                              the capacitor [ohm]
        constant_phase_element : single value (int or float)
                                   Constant phase angle [s^(alpha-1)/ohm]
        alpha : single value (float)
                  Exponent of the constant phase element.
                  Should be a value between 0 and 1 [-]
        sigma: single value (float)

    Returns
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
    '''
    circuit_string = '-Rs-(Q-(RW))-'

    if len(circuit_elements) != 5:
        raise AssertionError('The wrong number of circuit elements was+\
                              inputted')
    solution_resistance = circuit_elements['Rs']
    parallel_resistance = circuit_elements['Rp']
    constant_phase_elemen = circuit_elements['Q']
    alpha = circuit_elements['alpha']
    sigma = circuit_elements['sigma']

    # compute the impedance response as a complex array
    Z_Q = 1/(constant_phase_element*(angular_freq*1j)**alpha)
    Z_R = parallel_resistance
    Z_w = sigma*(angular_freq**(-0.5))-1j*sigma*(angular_freq**(-0.5))
    Z_complex = solution_resistance + 1/(1/Z_Q + 1/(Z_R+Z_w))

    return Z_complex
