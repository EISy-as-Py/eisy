import matplotlib.pyplot as plt

def plot_nyquist(response, save_image='None'):
    """
    """
    fig = plt.figure()
    plt.plot(response['Re_Z [Ohm]'], -response['Im_Z [Ohm]'], 'o')
    plt.ticklabel_format(style='sci', scilimits=(0, 0))
    plt.xlabel('Z$_{real}$ [$\Omega$]')
    plt.ylabel('-Z$_{imag}$ [$\Omega$]')
    plt.show()

    if save_image:
        plt.savefig('image_name.png')
