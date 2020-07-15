import matplotlib.pyplot as plt
import numpy as np

from .alterations import normalize
from matplotlib import rcParams

# rcParams['figure.figsize'] = (8, 6)
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
    plt.figure(figsize=(6, 6))
    if scatter:
        if alteration:
            plt.scatter(response['Re_Z_noise [ohm]'],
                        -response['Im_Z_noise [ohm]'], c='b', **kwargs)
        else:
            plt.scatter(response['Re_Z [ohm]'], -response['Im_Z [ohm]'], c='b',
                        **kwargs)
    else:
        if alteration:
            plt.plot(response['Re_Z_noise [ohm]'],
                     -response['Im_Z_noise [ohm]'], 'bo--', **kwargs)
        else:
            plt.plot(response['Re_Z [ohm]'], -response['Im_Z [ohm]'],
                     'o--', **kwargs)

    max_real = response['Re_Z [ohm]'].max()
    # plt.axes().set_aspect('auto')

    # plt.xlim([0, max_real+0.1*max_real])
    plt.xlim(left=-0.10)
    plt.ylim(top=max_real+0.1*max_real)
    # , max_real+0.1*max_real])

    if axis_off:
        plt.axis('off')
    else:
        plt.xlabel(r'Z$_{real}$ [$\Omega$]')
        plt.ylabel(r'-Z$_{imag}$ [$\Omega$]')

    if save_image:
        filename = str(save_location+filename)
        plt.savefig('{}.png'.format(filename), dpi=100, bbox_inches='tight',
                    transparent=transparent)
        plt.close()
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
    plt.figure(figsize=(6, 5))
    if alteration:
        plt.semilogx(response['freq [Hz]'], response['Re_Z_noise [ohm]'],
                     'bo--', response['freq [Hz]'],
                     -response['Im_Z_noise [ohm]'], 'ro--', **kwargs)
    else:
        plt.semilogx(response['freq [Hz]'], response['Re_Z [ohm]'], 'bo--',
                     response['freq [Hz]'], -response['Im_Z [ohm]'], 'ro--',
                     **kwargs)

    if axis_off:
        plt.axis('off')
    else:
        plt.xlabel(r'Frequency (Hz)')
        plt.ylabel(r'Impedance [$\Omega$]')
        plt.legend(('Real Z', 'Imag Z'))

    if save_image:
        filename = str(save_location+filename)
        plt.savefig('{}.png'.format(filename), dpi=100, bbox_inches='tight',
                    transparent=transparent)
        plt.close()
    plot_show = plt.show()
    return plot_show


def rgb_plot(red_array=None, green_array=None, blue_array=None,
             plot=True, save_image=None, filename=None,
             save_location=None):
    '''Returns a plot which represents the input data as a color gradient of
    one of the three color channels available: red, blue or green.

    This function represents the data as a color gradient in one of the three
    basic colors: red, blue or green. The color gradient is represented on the
    x-axis, leaving the y-axis as an arbitrary one. This means that the size or
    the scale of the y-axis do not have a numerical significance. The input
    arrays shoudld be of range zero to one. A minimum of one array should be
    provided. The final representation will be a square plot of the combined
    arrays.

    Parameters
    ----------
    red_array : array
                the data array to be plotted in the red channel.
    green_array : array
                  the data array to be plotted in the green channel.
    blue_array : array
                 the data array to be plotted in the blue channel.
    plot : bool
           if True, the color gradient representation of the data will be
           displayed
    filename : str
               The filename will be the same as the .csv containing the data
               used to create this plot.
    save_location : str
                    String containing the path of the forlder to use when
                    saving the data and the image.
    save_image : bool
                 Option to save the output of the simuation as a plot
                 in a .png file format.
                 The filename used for the file will be the same
                 as the raw data file created in this function.
    Returns
    -------
    rbg_plot :  matplotlib plot
                Plot representing the data as a color gradient on the x-axis
                in one of the three basic colors: red, blue or green
    '''
    arrays = {'red_array': red_array, 'blue_array': blue_array,
              'green_array': green_array}

    given = {k: v is not None for i, (k, v) in enumerate(arrays.items())}
    given_arrays = [(k, arrays[k]) for i, (k, v) in enumerate(given.items())
                    if v is True]
    n = []
    for i in range(len(given_arrays)):
        n.append(len(given_arrays[i][1]))
    assert len(given_arrays) != 0, 'no input array was given.'
    assert all(x == n[0] for x in n), 'the given arrays have different length.\
Check that you are using the right inputs'

    not_given = [k for (k, v) in given.items() if v is False]
    for array in not_given:
        arrays[array] = np.zeros(n[0])

    # Normalize Data from 0 to 1 (aka RGB readable)
    red_array = normalize(arrays['red_array'])
    green_array = normalize(arrays['green_array'])
    blue_array = normalize(arrays['blue_array'])

    arbitrary_axis = np.linspace(0, 1, n[0])

    r_big, a = np.meshgrid(red_array, arbitrary_axis)
    g_big, a = np.meshgrid(green_array, arbitrary_axis)
    b_big, a = np.meshgrid(blue_array, arbitrary_axis)

    rgb_plot = np.ndarray(shape=(n[0], n[0], 3))

    rgb_plot[:, :, 0] = r_big
    rgb_plot[:, :, 1] = g_big
    rgb_plot[:, :, 2] = b_big

    if plot:
        big, bax = plt.subplots(1, 1, figsize=[6, 6])
        bax.imshow(rgb_plot)
        bax.axis('off')

    if save_image:
        filename = str(save_location+filename)
        plt.savefig('{}.png'.format(filename), dpi=100, bbox_inches='tight')
        plt.close()
    return rgb_plot
