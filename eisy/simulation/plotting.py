import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd

from .alterations import normalize
from matplotlib import rcParams

rcParams['figure.figsize'] = (8, 6)
rcParams['savefig.dpi'] = 100
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12
rcParams['xtick.labelsize'] = 16
rcParams['ytick.labelsize'] = 16
rcParams['axes.titlesize'] = 20
rcParams['axes.labelsize'] = 18
rcParams['figure.subplot.hspace'] = 0.5
rcParams['figure.subplot.wspace'] = 0.5
rcParams['legend.numpoints'] = 1
rcParams['legend.fontsize'] = 16
rcParams['legend.markerscale'] = 1
rcParams['lines.linewidth'] = 1
rcParams['lines.markeredgewidth'] = 1
rcParams['lines.markersize'] = 4
rcParams['axes.unicode_minus'] = True


def nyquist_plot(response, filename=None, save_location=None, alteration=None,
                 save_image=None, axis_off=None, transparent=None,
                 scatter=None, **kwargs):
    '''
    Funciton that returns the nyquist plot of an impedance response.

    Parameters
    ----------
    response : pandas.DataFrame
               a dataframe containing the impedance response to be plotted.
    filename : str
               The filename contains a serial number composed by the date
               the funciton was run and the number of simuation for that day.
               The filename will be the same as the .csv file created from the
               impedance response used to create this plot.
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    save_location : str
                    String containing the path of the forlder to use when
                    saving the data and the image. Default option is a
                    folder called  'simulation_data' which will be created
                    in the current working directory.
    save_image : bool
                 Option to save the output of the simuation as a plot
                 in a .png file format.
                 The filename used for the file will be the same
                 as the raw data file created in this function.
    axis_off : bool
               Option to remove the axis from a plot. This will allow to
               display only the datapoints. This format is preferred for CNN
               input.
    plot_type : str
                string indicating teh desired plot to use to visualize the data
                Te options are 'nyquist', 'log_freq' or 'both', if both
                representations are desired. An individual file per each type
                of plot will be generated and saved in a separate folder.
    scatter : bool
              Changes the type of matplotlib fuction to use from 'plot' to
              'scatter'.
    transparent : bool
                  Removes thebackground of the plot in the saving step. The
                  resulting .png file(s) will have a transparent background.

    **kwargs : optional arguments supported by matplotlib.pyplot

    Returns
    -------
    The nyquist plot of the impedance response to be investigated.
    '''
    fig, ax = plt.subplots()
    if scatter:
        if alteration:
            ax.scatter(response['Re_Z [ohm]'], -response['Im_Z_noise [ohm]'],
                       **kwargs)
        else:
            ax.scatter(response['Re_Z [ohm]'], -response['Im_Z [ohm]'],
                       **kwargs)
    else:
        if alteration:
            ax.plot(response['Re_Z [ohm]'], -response['Im_Z_noise [ohm]'],
                    'o--', **kwargs)
        else:
            ax.plot(response['Re_Z [ohm]'], -response['Im_Z [ohm]'],
                    'o--', **kwargs)

    max_real = response['Re_Z [ohm]'].max()
    ax.set_aspect('equal')

    ax.set_xlim([0, max_real+0.1*max_real])
    ax.set_ylim([0, max_real+0.1*max_real])

    if axis_off:
        ax.axis('off')
    else:
        ax.set_xlabel(r'Z$_{real}$ [$\Omega$]')
        ax.set_ylabel(r'-Z$_{imag}$ [$\Omega$]')

    if save_image:
        filename = str(save_location+filename)
        plt.savefig('{}.png'.format(filename), dpi=100, bbox_inches='tight',
                    transparent=transparent)

    plt.show()
    return


def log_freq_plot(response, filename=None, axis_off=None, scatter=None,
                  save_location=None, alteration=None, transparent=None,
                  save_image=None, **kwargs):
    '''
    Funciton that returns the bode plot of an impedance response.

    Parameters
    ----------
    response : pandas.DataFrame
               a dataframe containing the impedance response to be plotted.
    filename : str
               The filename contains a serial number composed by the date
               the funciton was run and the number of simuation for that day.
               The filename will be the same as the .csv file created from the
               impedance response used to create this plot.
    alteration : str
                 string indicating if the data simulated has been modified to
                 add noise or other instrument artifacts. If present, this
                 string will also be added to the file name to help keeping
                 the data correctly labeled.
    save_location : str
                    String containing the path of the forlder to use when
                    saving the data and the image. Default option is a
                    folder called  'simulation_data' which will be created
                    in the current working directory.
    save_image : bool
                 Option to save the output of the simuation as a plot
                 in a .png file format.
                 The filename used for the file will be the same
                 as the raw data file created in this function.
    axis_off : bool
               Option to remove the axis from a plot. This will allow to
               display only the datapoints. This format is preferred for CNN
               input.
    plot_type : str
                string indicating teh desired plot to use to visualize the data
                Te options are 'nyquist', 'log_freq' or 'both', if both
                representations are desired. An individual file per each type
                of plot will be generated and saved in a separate folder.
    scatter : bool
              Changes the type of matplotlib fuction to use from 'plot' to
              'scatter'.
    transparent : bool
                  Removes thebackground of the plot in the saving step. The
                  resulting .png file(s) will have a transparent background.

    **kwargs : optional arguments supported by matplotlib.pyplot

    Returns
    --------
    log_freq_plot: matplotlib plot
                   plot of the real and imaginary parts of the impedance
                   response to be investigated versus the frequency.
    '''
    fig, ax = plt.subplots()
    if alteration:
        ax.semilogx(response['freq [Hz]'], response['Re_Z [ohm]'], 'o--',
                    response['freq [Hz]'], -response['Im_Z_noise [ohm]'],
                    'o--', **kwargs)
    else:
        ax.semilogx(response['freq [Hz]'], response['Re_Z [ohm]'], 'o--',
                    response['freq [Hz]'], -response['Im_Z [ohm]'], 'o--',
                    **kwargs)

    if axis_off:
        ax.axis('off')
    else:
        ax.set_xlabel(r'Frequency (Hz)')
        ax.set_ylabel(r'Impedance [$\Omega$]')
        ax.legend(('Real Z', 'Imag Z'))

    if save_image:
        filename = str(save_location+filename)
        plt.savefig('{}.png'.format(filename), dpi=100, bbox_inches='tight',
                    transparent=transparent)

    plt.show()
    return


def rgb_plot(red_array, green_array=[0, 0], blue_array=[0, 0], plot=True):
    '''Returns a plot which represents the input data as a color gradient of
    one of the three color channels available: red, blue or green.

    This function represents the data as a color gradient in one of the three
    basic colors: red, blue or green. The color gradient is represented on the
    x-axis, leaving the y-axis as an arbitrary one. This means that the size or
    the scale of the y-axis do not have a numerical significance. The input
    arrays shoudld be of range zero to one. A minimum of one array should be
    provided. The final representation will be a square plot of the combined
    arrays. An optional feature to add o the plot is to have three smaller
    bar plot which represent the individual color arrays.

    Parameters
    ----------
    red_array : array
                the data array to be plotted in the red channel.
    green_array : array
                  the data array to be plotted in the green channel.
    blue_array : array
                 the data array to be plotted in the blue channel.

    Returns
    -------
    rbg_plot :  matplotlib plot
                Plot representing the data as a color gradient on the x-axis
                in one of the three basic colors: red, blue or green
    '''
    r = len(red_array)
    g = len(green_array)
    b = len(blue_array)

    if r != g:
        green_array = red_array * 0
        print("Green Array Failed? (Or none given)")
    if r != b:
        blue_array = red_array * 0
        print("Blue  Array Failed? (Or none given)")

    # Normalize Data from 0 to 1 (aka RGB readable)
    red_array = normalize(red_array)
    green_array = normalize(green_array)
    blue_array = normalize(blue_array)

    # Two types of Meshes: One 10 larger than the other
    # (Smaller used for Individual 1D arrays, Larger for combined)
    # FOR LATER--> MAKE BIG MATRIX A SQUARE! EASY TO COMBINE
    arb_big = np.linspace(0, 1, r)
    arb_small = np.linspace(0, 1, int(r/10))
    # x_later = np.linspace(0, r, r)

    r_small, a = np.meshgrid(red_array, arb_small)
    g_small, a = np.meshgrid(green_array, arb_small)
    b_small, a = np.meshgrid(blue_array, arb_small)

    r_big, a = np.meshgrid(red_array, arb_big)
    g_big, a = np.meshgrid(green_array, arb_big)
    b_big, a = np.meshgrid(blue_array, arb_big)

    big_plot = np.ndarray(shape=(r, r, 3))
    r_plot = np.ndarray(shape=(int(r/10), r, 3))
    g_plot = np.ndarray(shape=(int(r/10), r, 3))
    b_plot = np.ndarray(shape=(int(r/10), r, 3))

    big_plot[:, :, 0] = r_big
    big_plot[:, :, 1] = g_big
    big_plot[:, :, 2] = b_big

    r_plot[:, :, 0] = r_small
    g_plot[:, :, 1] = g_small
    b_plot[:, :, 2] = b_small

    r_plot[:, :, 1] = r_plot[:, :, 2] = r_small*0
    g_plot[:, :, 0] = g_plot[:, :, 2] = g_small*0
    b_plot[:, :, 0] = b_plot[:, :, 1] = b_small*0

    if plot:
        big, bax = plt.subplots(1, 1, figsize=[6, 6])
        # fig,ax = plt.subplots(3,1,figsize=[6,2])

        bax.imshow(big_plot)
        # ax[0].imshow(r_plot)
        # ax[1].imshow(g_plot)
        # ax[2].imshow(b_plot)
        # ax[0].plot(x_later,red_array)

        bax.axis('off')
        # for i in [0,1,2]:
        #    ax[i].axis('off')
    # big_plot = rgb2hsv(big_plot)

    return big_plot
