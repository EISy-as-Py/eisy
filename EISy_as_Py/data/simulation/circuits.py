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
                 Solution resistance [Ohm]
    capacitance : single value (int or float)
                  Electrode capacitance [F]
    peak_frequency : single value (int or float)
                     Peak frequency of RC circuit [Hz]

    Output
    ---------
    Z_complex : array-like
                impedance response of the circuit under investigation [Ohm]
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
                impedance response of the circuit under investigation [Ohm]
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
                             Constant phase angle [s^n/ohm]
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
    if (resistance, constant_phase_element, alpha, peak_frequency) == 'none':
        raise AssertionError('No circuit element value was provided. Cannot\
                              compute the impedance response')
    elif (resistance, capacitance, constant_phase_element, alpha) == 'none':
        raise AssertionError('Not enough circuit element values were provided.\
                              Cannot compute the impedance response')
    if resistor == 'none':
        resistor = (1/(constant_phase_element*(2*np.pi*peak_frequency)**alpha))
    elif constant_phase_element == 'none':
        constant_phase_element = (1/(resistor*(2*np.pi*peak_frequency)**alpha))
    elif alpha == 'none':
        alpha = np.log(constant_phase_element*resistor)/np.log(1/(2*np.pi *
                                                               peak_frequency))
    Z_complex = (resistor/(1+resistor*constant_phase_element*(
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
    String representation for this circuit: -RQ-

    Parameters
    ----------
    angular_freq : array-like
                   Angular frequency [1/s]
    resistance : single value (int or float)
                 Solution resistance [ohm]
    constant_phase_element : single value (int or float)
                             Constant phas angle [s^n/ohm]
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
    circuit = '-RC-'
    if resistance == 'none':
        resistance = (1/(capacitance*(2*np.pi*peak_frequency)))
    elif capacitance == 'none':
        capacitance = (1/(resistance*(2*np.pi*peak_frequency)))
    # compute the impedance response as a complex array
    Z_complex = resistance + 1/(capacitance*(angular_freq*1j))
    return Z_complex


def cir_RsRC(w, Rs, R, C):
    ''''
    Simulation Function: -RsR/C-

    Author: Maria Politi [politim@uw.edu]

    Inputs
    ----------
    Rs = Series resistance [Ohm]
    R = Resistance [Ohm]
    C = Capacitance [F]
    '''
    return Rs + (R/(1+R*C*(w*1j)))


def cir_Randles_simplified(w, Rs, R, n, sigma, Q='none', fs='none'):
    '''
    Simulation Function: Randles -Rs-(Q-(RW)-)-
    Return the impedance of a Randles circuit with a simplified
    NOTE: This Randles circuit is only meant for semi-infinate linear diffusion

    Author:Kristian B. Knudsen (kknu@berkeley.edu ||
                                kristianbknudsen@gmail.com)
    Modified: Maria Politi (politm@uw.edu)
    '''
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


def cir_RsRQRQ(w, Rs, R='none', Q='none', n='none', fs='none', R2='none',
               Q2='none', n2='none', fs2='none'):
    '''

    Simulation Function: -Rs-RQ-RQ-
    Return the impedance of an Rs-RQ-RQ circuit.

    Author:Kristian B. Knudsen (kknu@berkeley.edu ||
                                kristianbknudsen@gmail.com)
    Modified: Maria Politi (politm@uw.edu)
    Inputs
    ----------
    w = Angular frequency [1/s]
    Rs = Series Resistance [Ohm]
    R = Resistance [Ohm]
    Q = Constant phase element [s^n/ohm]
    n = Constant phase element exponent [-]
    fs = Summit frequency of RQ circuit [Hz]
    R2 = Resistance [Ohm]
    Q2 = Constant phase element [s^n/ohm]
    n2 = Constant phase element exponent [-]
    fs2 = Summit frequency of RQ circuit [Hz]
    '''

    if R == 'none':
        R = (1/(Q*(2*np.pi*fs)**n))
    elif Q == 'none':
        Q = (1/(R*(2*np.pi*fs)**n))
    elif n == 'none':
        n = np.log(Q*R)/np.log(1/(2*np.pi*fs))

    if R2 == 'none':
        R2 = (1/(Q2*(2*np.pi*fs2)**n2))
    elif Q2 == 'none':
        Q2 = (1/(R2*(2*np.pi*fs2)**n2))
    elif n2 == 'none':
        n2 = np.log(Q2*R2)/np.log(1/(2*np.pi*fs2))

    return Rs + (R/(1+R*Q*(w*1j)**n)) + (R2/(1+R2*Q2*(w*1j)**n2))
