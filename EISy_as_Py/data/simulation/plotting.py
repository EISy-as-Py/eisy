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
