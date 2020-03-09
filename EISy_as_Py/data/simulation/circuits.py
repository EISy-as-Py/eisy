import numpy as np


def freq_gen(high_freq, low_freq, decades=7):
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
              is set to be 7 [-]

    Output
    ----------
    [0] = frequency range [Hz]
    [1] = Angular frequency range [1/s]
    '''
    f_decades = np.log10(high_freq) - np.log10(low_freq)
    f_range = np.logspace(np.log10(high_freq), np.log10(low_freq),
                          np.around(decades*f_decades), endpoint=True)
    w_range = 2 * np.pi * f_range
    return f_range, w_range


def cir_RC_parallel(angular_freq, resistance='none', capacitance='none',
                    peak_frequency='none'):
    '''
    Function that simulates the impedance response of a resistor and a
    capacitor in a parallel configuration.
    String representation for this circuit: -(RC)-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]
    resistance : single value (int or float)
                 Solution resistance [ohm]
    capacitance : single value (int or float)
                  Electrode capacitance [F]
    peak_frequency : single value (int or float)
                     Peak frequency of RC circuit [Hz]

    Output
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [ohm]
    '''
    circuit = '-(RC)-'
    if resistance == 'none':
        resistance = (1/(capacitance*(2*np.pi*peak_frequency)))
    elif capacitance == 'none':
        capacitance = (1/(resistance*(2*np.pi*peak_frequency)))
    # compute the impedance response as a complex array
    Z_complex = (resistance/(1+resistance*capacitance*(angular_freq*1j)))
    return Z_complex


def cir_RC_series(angular_freq, resistance='none', capacitance='none',
                  peak_frequency='none'):
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
    resistance : single value (int or float)
                 Solution resistance [ohm]
    capacitance : single value (int or float)
                  Capacitance of an electrode surface [F]
    peak_frequency : single value (int or float)
                     Peak frequency of RC circuit [Hz]

    Output
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [ohm]
    '''
    circuit = '-R-C-'
    if (resistance, capacitance, peak_frequency) == 'none':
        raise AssertionError('No circuit element value was provided. Cannot\
                              compute the impedance response')
    elif (resistance, capacitance) == 'none':
        raise AssertionError('Not enough circuit element values were provided.\
                              Cannot compute the impedance response')
    elif resistance == 'none':
        resistance = (1/(capacitance*(2*np.pi*peak_frequency)))
    elif capacitance == 'none':
        capacitance = (1/(resistance*(2*np.pi*peak_frequency)))
    # compute the impedance response as a complex array
    Z_complex = resistance + 1/(capacitance*(angular_freq*1j))
    return Z_complex


def cir_RQ_parallel(angular_freq, resistance='none',
                    constant_phase_element='none', alpha='none',
                    peak_frequency='none'):
    '''
    Function that simulates the impedance response of a resistor and a
    constant phase element in a parallel configuration.
    String representation for this circuit: -(RQ)-
    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]
    resistance : single value (int or float)
                 Solution resistance [Ohm]
    constant_phase_element : single value (int or float)
                             Constant phase angle [s^(alpha-1)/ohm]
    alpha : single value -float
            Exponent of the constant phase element. Should be a value between
            0 and 1 [-]
    peak_frequency : single value (int or float)
                     Peak frequency of RC circuit [Hz]

    Output
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
    '''
    circuit = '-(RQ)-'
    if (resistance, constant_phase_element, alpha, peak_frequency) == 'none':
        raise AssertionError('No circuit element value was provided. Cannot\
                              compute the impedance response')
    elif (resistance, constant_phase_element, alpha) == 'none':
        raise AssertionError('Not enough circuit element values were provided.\
                              Cannot compute the impedance response')
    elif resistance == 'none':
        resistance = (1/(constant_phase_element*(2*np.pi*peak_frequency
                                                 ) ** alpha))
    elif constant_phase_element == 'none':
        constant_phase_element = (1/(resistance*(2*np.pi*peak_frequency
                                                 ) ** alpha))
    elif alpha == 'none':
        alpha = np.log(constant_phase_element *
                       resistance)/np.log(1/(2*np.pi * peak_frequency))
    Z_complex = (resistance/(1+resistance*constant_phase_element*(
                 angular_freq*1j)**alpha))
    return Z_complex


def cir_RQ_series(angular_freq, resistance='none',
                  constant_phase_element='none', alpha='none',
                  peak_frequency='none'):
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
    resistance : single value (int or float)
                 Solution resistance [ohm]
    constant_phase_element : single value (int or float)
                             Constant phas angle [s^(alpha-1)/ohm]
    alpha : single value -float
            Exponent of the constant phase element. Should be a value between
            0 and 1 [-]
    peak_frequency : single value (int or float)
                     Peak frequency of RC circuit [Hz]

    Output
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Oom]
    '''
    circuit = '-R-Q-'
    if (resistance, constant_phase_element, alpha, peak_frequency) == 'none':
        raise AssertionError('No circuit element value was provided. Cannot\
                              compute the impedance response')
    elif (resistance, capacitance, constant_phase_element, alpha) == 'none':
        raise AssertionError('Not enough circuit element values were provided.\
                              Cannot compute the impedance response')
    elif resistor == 'none':
        resistor = (1/(constant_phase_element*(2*np.pi*peak_frequency)**alpha))
    elif constant_phase_element == 'none':
        constant_phase_element = (1/(resistor*(2*np.pi*peak_frequency)**alpha))
    elif alpha == 'none':
        alpha = np.log(constant_phase_element *
                       resistor)/np.log(1/(2*np.pi * peak_frequency))
    # compute the impedance response as a complex array
    Z_complex = resistance + 1/(constant_phase_element*(
                                angular_freq*1j)**alpha)
    return Z_complex


def cir_RsRC(angular_freq, solution_resistance,
             parallel_resistance='none', capacitance='none',
             peak_frequency='none'):
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
    solution_resistance : single value (int or float)
                          Solution resistance [ohm]
    parallel_resistance : single value (int or float)
                          resistance of the element in parallel with
                          the capacitor [ohm]
    capacitance : single value (int or float)
                  Capacitance of an electrode surface [F]
    peak_frequency : single value (int or float)
                     Peak frequency of the parallel RC circuit [Hz]
    Output
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
    '''
    circuit = '-Rs-(RC)-'
    # compute the impedance response as a complex array
    if (parallel_resistance, capacitance, peak_frequency) == 'none':
        raise AssertionError('No circuit element value was provided. Cannot\
                              compute the impedance response')
    elif (parallel_resistance, capacitance) == 'none':
        raise AssertionError('Not enough circuit element values were provided.\
                              Cannot compute the impedance response')
    elif parallel_resistance == 'none':
        parallel_resistance = (1/(capacitance*(2*np.pi*peak_frequency)))
    elif capacitance == 'none':
        capacitance = (1/(parallel_resistance*(2*np.pi*peak_frequency)))
    Z_parallel = (parallel_resistance/(1 + parallel_resistance *
                                       capacitance * (angular_freq*1j)))
    Z_complex = solution_resistance + Z_parallel
    return Z_complex


def cir_RsRQRQ(angular_freq, solution_resistance='none',
               parallel_resistance_1='none', constant_phase_element_1='none',
               alpha_1='none', parallel_resistance_2='none',
               constant_phase_element_2='none', alpha_2='none',
               peak_frequency_1='none', peak_frequency_2='none'):
    '''
    Function that simulates the impedance response of a solution resistor in
    series with two sets of a resistor in parallel with a constant phase
    elements.
    String representation for this circuit: -Rs-(RQ)-(RQ)-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]
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
                               Second Constant phas angle [s^(alpha-1)/ohm]
    alpha_2 : single value -float
              Exponent of the second constant phase element.
              Should be a value between 0 and 1 [-]
    peak_frequency_1 : single value (int or float)
                     Peak frequency of the first parallel RQ circuit [Hz]
    peak_frequency_2 : single value (int or float)
                       Peak frequency of the second parallel RQ circuit [Hz]
    Output
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
    '''
    circuit = '-Rs-(RQ)-(RQ)-'

    if (parallel_resistance_1, constant_phase_element_1, peak_frequency_1,
       parallel_resistance_2, constant_phase_element_2,
       peak_frequency_2) == 'none':
        raise AssertionError('No circuit element value was provided. Cannot\
                              compute the impedance response')
    elif (parallel_resistance_1, constant_phase_element_1,
          parallel_resistance_2, constant_phase_element_2) == 'none':
        raise AssertionError('Not enough circuit element values were provided.\
                              Cannot compute the impedance response')

    if parallel_resistance_1 == 'none':
        parallel_resistance_1 = (1/(constant_phase_element_1 *
                                 (2*np.pi*peak_frequency_1)**alpha_1))
    elif constant_phase_element_1 == 'none':
        constant_phase_element_1 = (1/(parallel_resistance_1 *
                                    (2*np.pi*peak_frequency_1)**alpha_1))
    if parallel_resistance_2 == 'none':
        parallel_resistance_2 = (1/(constant_phase_element_2 *
                                 (2*np.pi*peak_frequency_2)**alpha_2))
    elif constant_phase_element_2 == 'none':
        constant_phase_element_2 = (1/(parallel_resistance_2 *
                                    (2*np.pi*peak_frequency_2)**alpha_2))

    Z_parallel_1 = (parallel_resistance_1 /
                    (1+parallel_resistance_1*constant_phase_element_1
                     * (angular_freq*1j)**alpha_1))
    Z_parallel_2 = (parallel_resistance_2 /
                    (1+parallel_resistance_2*constant_phase_element_2
                     * (angular_freq*1j)**alpha_2))
    Z_complex = solution_resistance + Z_parallel_1 + Z_parallel_2

    return Z_complex


def cir_RsRCRC(angular_freq, solution_resistance,
               parallel_resistance_1='none', capacitance_1='none',
               parallel_resistance_2='none', capacitance_2='none',
               peak_frequency_1='none', peak_frequency_2='none'):
    '''
    Function that simulates the impedance response of a solution resistor in
    series with two sets of a resistor in parallel with a capacitor.
    String representation for this circuit: -Rs-(RC)-(RC)-


    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]
    solution_resistance : single value (int or float)
                          Solution resistance [ohm]
    parallel_resistance_1 : single value (int or float)
                            first combination of resistor in parallel with
                            capacitor [ohm]
    capacitance_1 : single value (int or float)
                    Capacitance of an electrode surface whichi is part of the
                    first combination of RC in parallel [F]
    parallel_resistance_2 : single value (int or float)
                            second combination of resistor in parallel with
                            capacitor [ohm]
    capacitance_2 : single value (int or float)
                    Capacitance of an electrode surface whichi is part of the
                    second combination of RC in parallel [F]
    peak_frequency_1 : single value (int or float)
                       Peak frequency of the first parallel RC circuit [Hz]
    peak_frequency_2 : single value (int or float)
                       Peak frequency of the second parallel RC circuit [Hz]
    Output
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
    '''
    circuit = '-Rs-(RC)-(RC)-'

    if (parallel_resistance_1, capacitance_1, peak_frequency_1,
       parallel_resistance_2, capacitance_2, peak_frequency_2) == 'none':
        raise AssertionError('No circuit element value was provided. Cannot\
                              compute the impedance response')
    elif (parallel_resistance_1, capacitance_1,
          parallel_resistance_2, capacitance_2) == 'none':
        raise AssertionError('Not enough circuit element values were provided.\
Cannot compute the impedance response')

    if parallel_resistance_1 == 'none':
        parallel_resistance_1 = (1/(capacitance_1*(2*np.pi *
                                                   peak_frequency_1)))
    elif capacitance_1 == 'none':
        capacitance_1 = (1/(parallel_resistance_1*(2*np.pi *
                                                   peak_frequency_1)))
    if parallel_resistance_2 == 'none':
        parallel_resistance_2 = (1/(capacitance_2*(2*np.pi *
                                                   peak_frequency_2)))
    elif capacitance_2 == 'none':
        capacitance_2 = (1/(parallel_resistance_2*(2*np.pi *
                                                   peak_frequency_2)))

    Z_parallel_1 = (parallel_resistance_1/(1 + parallel_resistance_1 *
                                           capacitance_1*(angular_freq*1j)))
    Z_parallel_2 = (parallel_resistance_2/(1 + parallel_resistance_2 *
                                           capacitance_2*(angular_freq*1j)))
    Z_complex = solution_resistance + Z_parallel_1 + Z_parallel_2
    return Z_complex


def cir_Randles_simplified(angular_freq, solution_resistance,
                           parallel_resistance, alpha, sigma,
                           Q='none', fs='none'):
    '''
    Return the impedance of a Randles circuit with a simplified Warburg element
    This form of the Randles circuit is only meant for to simulate
    semi-infinate linear diffusion
    String representation for this circuit: -Rs-(Q-(RW)-)-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]
    solution_resistance : single value (int or float)
                          Solution resistance [ohm]
    parallel_resistance : single value (int or float)
                          resistance of the element in parallel with
                          the capacitor [ohm]
    capacitance : single value (int or float)
                  Capacitance of an electrode surface [F]
    [[Need to add new parameters!!!!]]
    Output
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
    '''
    circuit = '-Rs-(Q-(RW)-)-'
    if R == 'none':
        R = (1/(Q*(2*np.pi*fs)**n))
    elif Q == 'none':
        Q = (1/(R*(2*np.pi*fs)**n))
    elif n == 'none':
        n = np.log(Q*R)/np.log(1/(2*np.pi*fs))

    Z_Q = 1/(Q*(w*1j)**n)
    Z_R = R
    Z_w = sigma*(w**(-0.5))-1j*sigma*(w**(-0.5))

    return Rs + 1/(1/Z_Q + 1/(Z_R+Z_w))
