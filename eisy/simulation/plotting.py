import matplotlib.pyplot as plt
import numpy as np

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
    """
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

    Output
    ----------
    The nyquist plot of the impedance response to be investigated.
    """
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
    # plt.ticklabel_format(style='sci', scilimits=(0, 0))
    max_real = response['Re_Z [ohm]'].max()
    ax.set_aspect('equal')

    ax.set_xlim([0, max_real+0.1*max_real])
    ax.set_ylim([0, max_real+0.1*max_real])

    if axis_off:
        ax.axis('off')
        # ax.set_yticks([])
        # ax.set_yticklabels([])
        # ax.set_xticks([])
        # ax.set_xticklabels([])
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
    """
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

    Output
    ----------
    The bode plot of the impedance response to be investigated.
    """
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
