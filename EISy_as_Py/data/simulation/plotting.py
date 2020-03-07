import matplotlib.pyplot as plt
import numpy as np


def nyquist_plot(response, axis_limits=None, filename=None, save_image=None,
                 **kwargs):
    """
    """
    fig, ax = plt.figure()
    ax.plot(response['Re_Z [Ohm]'], -response['Im_Z [Ohm]'], 'o--', **kwargs)
    # plt.ticklabel_format(style='sci', scilimits=(0, 0))
    ax.xlabel(r'Z$_{real}$ [$\Omega$]')
    ax.ylabel(r'-Z$_{imag}$ [$\Omega$]')
    ax.set_xlim([0, 500])
    ax.set_ylim([0, 200])
    ax.set_aspect('equal')
    # ax.xticks(np.arange(min(),
    #                     max(response['Re_Z [Ohm]'])+1, 10))
    # if save_image:
    plt.savefig('{}.png'.format(filename), layout='tight',
                bbox_inches='tight')
    if axis_limits:
        plt.xlim(axis_limits[0])
        plt.ylim(axis_limits[1])
    plt.show()
    return
