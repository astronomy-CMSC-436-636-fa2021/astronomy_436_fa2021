import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
#plt.style.use(astropy_mpl_style)
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
from astropy.table import Table
from astropy.utils.data import download_file
import numpy as np

from astropy.io import fits

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
def main():
    user_input=input("enter fit file\n")
    image_file=fits.open(user_input, memmap= True)
    image_file.info()
    evt_data=Table(image_file[1].data)
    # showing scatter plot
    energy_hist = plt.scatter(evt_data["RA"],evt_data['ENERGY'])
    plt.show()
    # showing 2 d histagram
    ii = np.in1d(evt_data['CONVERSION_TYPE'], [0, 1])
    np.sum(ii)
    NBINS = (500,500)
    img_zero, yedges, xedges = np.histogram2d(evt_data['RA'][ii], evt_data['DEC'][ii], NBINS)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.imshow(img_zero)
    plt.show()

    #showing plt hist2d 
    NBINS = (100,100)
    img_zero_mpl = plt.hist2d(evt_data['RA'][ii], evt_data['DEC'][ii], NBINS, cmap='viridis', norm=LogNorm())

    cbar = plt.colorbar(ticks=[1.0,3.0,6.0])
    cbar.ax.set_yticklabels(['1','3','6'])

    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()





    

main()
