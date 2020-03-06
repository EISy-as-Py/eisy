import numpy as np


def freq_gen(f_start, f_stop, pts_decade=7):
    '''
    Frequency Generator with logspaced freqencies

    Inputs
    ----------
    f_start = frequency start [Hz]
    f_stop = frequency stop [Hz]
    pts_decade = Points/decade, default 7 [-]

    Output
    ----------
    [0] = frequency range [Hz]
    [1] = Angular frequency range [1/s]
    '''
    f_decades = np.log10(f_start) - np.log10(f_stop)
    f_range = np.logspace(np.log10(f_start), np.log10(f_stop),
                          num=np.around(pts_decade*f_decades), endpoint=True)
    w_range = 2 * np.pi * f_range
    return f_range, w_range


def cir_RC(w, R='none', C='none', fs='none'):
    '''
    Simulation Function: -RC-
    Returns the impedance of an RC circuit, using RQ definations where n=1.
    see cir_RQ() for details
    Author:Kristian B. Knudsen (kknu@berkeley.edu ||
                                kristianbknudsen@gmail.com)
    Modified: Abdul Moeez (add email)
    Inputs
    ----------
    w = Angular frequency [1/s]
    R = Resistance [Ohm]
    C = Capacitance [F]
    fs = Summit frequency of RC circuit [Hz]
    '''
    if R == 'none':
        R = (1/(C*(2*np.pi*fs)))
    elif C == 'none':
        C = (1/(R*(2*np.pi*fs)))
    return (R/(1+R*C*(w*1j)))


def cir_RC_series(w, R, C, fs=fs):
    '''
    '''
    if R == 'none':
        R = (1/(C*(2*np.pi*fs)))
    elif C == 'none':
        C = (1/(R*(2*np.pi*fs)))
    return R+1/(C*(w*1j))


def cir_RQ(w, R='none', Q='none', n='none', fs='none'):
    '''
    Simulation Function: -RQ-
    Return the impedance of an Rs-RQ circuit. See details for RQ under
    cir_RQ_fit()
    Kristian B. Knudsen (kknu@berkeley.edu / kristianbknudsen@gmail.com)
    Inputs
    ----------
    w = Angular frequency [1/s]
    R = Resistance [Ohm]
    Q = Constant phase element [s^n/ohm]
    n = Constant phase elelment exponent [-]
    fs = Summit frequency of RQ circuit [Hz]
    '''
    if R == 'none':
        R = (1/(Q*(2*np.pi*fs)**n))
    elif Q == 'none':
        Q = (1/(R*(2*np.pi*fs)**n))
    elif n == 'none':
        n = np.log(Q*R)/np.log(1/(2*np.pi*fs))
    return (R/(1+R*Q*(w*1j)**n))


def cir_RsRC(w, Rs, R, C):
    ''''
    Simulation Function: -Rs-RC-

    Author: Maria Politi

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
