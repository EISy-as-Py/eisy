import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rcParams

rcParams['figure.figsize'] = (8, 6)
rcParams['savefig.dpi'] = 300
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12
# rcParams['font.serif'] = 'Times New Roman'
# rcParams['font.sans-serif'] = 'Arial'
# rcParams['font.monospace'] = 'Courier New'
# rcParams['mathtext.default'] = 'rm'
# rcParams['mathtext.fontset'] = 'stix'
rcParams['xtick.labelsize'] = 16
rcParams['ytick.labelsize'] = 16
rcParams['axes.titlesize'] = 20
rcParams['axes.labelsize'] = 18
rcParams['figure.subplot.hspace'] = 0.5
rcParams['figure.subplot.wspace'] = 0.5
rcParams['legend.numpoints'] = 1  # the number of points in the legend line
rcParams['legend.fontsize'] = 16
# the relative size of legend markers vs. original
rcParams['legend.markerscale'] = 1
rcParams['lines.linewidth'] = 1
rcParams['lines.markeredgewidth'] = 1
rcParams['lines.markersize'] = 4
rcParams['axes.unicode_minus'] = True


def nyquist_plot(response, filename=None, save_location=None,
                 save_image=None, **kwargs):
    """
    Funciton that returns the nyquist plot of an impedance response.

    Parameters
    ----------
    response : pandas.DataFrame
               a dataframe containing the impedance response to be plotted.
    filename : st
               The filename contains a serial number composed by the date
               the funciton was run and the number of simuation for that day.
               The filename will be the same as the .csv file created from the
               impedance response used to create this plot.
    save_location : str
                       String containing the path of the forlder to use when
                       saving the data and the image. Default option is a
                       folder called  'simulation_data' which will be created
                       in the current working directory.
    save_image : True/False
                 Option to save the output of the simuation as a plot
                 in a .png file format.
                 The filename used for the file will be the same
                 as the raw data file created in this function.

    **kwargs : optional arguments supported by matplotlib.pyplot

    Output
    ----------
    The nyquist plot of the impedance response to be investigated.
    """
    fig, ax = plt.subplots()
    ax.plot(response['Re_Z [ohm]'], -response['Im_Z [ohm]'], 'o--', **kwargs)
    # plt.ticklabel_format(style='sci', scilimits=(0, 0))
    ax.set_xlabel(r'Z$_{real}$ [$\Omega$]')
    ax.set_ylabel(r'-Z$_{imag}$ [$\Omega$]')
    ax.set_xlim([0, 600])
    ax.set_ylim([0, 200])
    ax.set_aspect('equal')
    # ax.xticks(np.arange(min(),
    #                     max(response['Re_Z [Ohm]'])+1, 10))
    if save_image:
        filename = str(save_location+filename)
        plt.savefig('{}.png'.format(filename), layout='tight',
                    bbox_inches='tight')
    plt.show()
    return
