def plot_nyquist(response):
    """
    """
    fig = plt.figure()
    plt.plot(response['Re_Z [Ohm]'], -response['Im_Z [Ohm]'], 'o')
    plt.ticklabel_format(style = 'sci', scilimits=(0,0))
    plt.xlabel('Z$_{real}$ [$\Omega$]')
    plt.ylabel('-Z$_{imag}$ [$\Omega$]')
    plt.show()