import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
#plt.style.use(astropy_mpl_style)
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits
from astropy.table import Table
from astropy.table import vstack
from astropy.utils.data import download_file
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os
import urllib
import ssl
from pathlib import Path
def do_some_prompts():
    #Todo - make this better prompt, probably with GUI
    #in this file, I want to prompt the user for a date range
    okay = False
    while (not (okay)):
        # todo: convert to a GUI picking actual weeks rather than numerically
        week_start = int(input("What week would you like to start (009 minimum)"))
        week_end = int(input("What week would you like to end? (700 max)"))
        temp = input("There will be approximately {} MB for those files, is that ok?(y/n)".format(60 * (week_end-week_start + 1) ))
        if (temp == 'y'):
            okay = True
        return  week_start, week_end
    okay = False
    while (not (okay)):
        print("Getting values for bounds of energy, measured in MeV")
        energy_start = float(input("What is your lower bound for the energy? (Recommend no lower than 20)"))
        energy_end = float(input("What is your upper bound for the energy (Recommend no higher than 3500)"))
        if (energy_end > energy_start):
            okay = True
    return week_start, week_end, energy_start, energy_end

def int_to_string(i):
    if (i <= 9):
        return "00" + str(i)
    if (i < 99):
        return "0"+str(i)
    else:
        return str(i)

def download_some_files(week_strt, week_end):
    dl_root = "https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/"
    dl_path = os.path.join("fits","archive")
    ssl._create_default_https_context = ssl._create_unverified_context
    for i in range(week_strt, week_end+1):
        #print()
        dl_link = dl_root +"lat_photon_weekly_w{fname}_p305_v001.fits".format(fname=int_to_string(i))
        #print(dl_link)
        urllib.request.urlretrieve(dl_link,"lat_photon_weekly_w{}_p305_v001.fits".format(int_to_string(i)) )
def main():
    start_week, end_wk = do_some_prompts()
    # now we go out and download the files
    download_some_files(start_week,end_wk)
    full_evt_data = list()
    #user_input=input("enter fit file\n")
    for i in range (start_week, end_wk+1):
        file_to_open = str(Path().absolute()) + "\\lat_photon_weekly_w" + int_to_string(i) + "_p305_v001.fits"
        image_file=fits.open(file_to_open, memmap= True)
        #image_file.info() debug info about the FITS
        full_evt_data.append(Table(image_file[1].data)) #add opened table to collection
        evt_data = full_evt_data[i - start_week] # give it evt_data name for backwards compatability


        #np.sum(ii)
        #NBINS = (500,500)
        #img_zero, yedges, xedges = np.histogram2d(evt_data['RA'][ii], evt_data['DEC'][ii], NBINS)
        # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        #plt.imshow(img_zero)
        #plt.show()

        # showing plt hist2d
        nbins = (100,100)
        fig, ax = plt.subplots(1)
        ii = np.in1d(evt_data['CONVERSION_TYPE'], [0, 1])
        img_zero_mpl = plt.hist2d(evt_data['RA'][ii], evt_data['DEC'][ii], nbins, cmap='viridis', norm=LogNorm())
        cbar = plt.colorbar(ticks=[1.0,3.0,6.0])
        cbar.ax.set_yticklabels(['1','3','6'])
        plt.title("lat_photon_weekly_w" + int_to_string(i) + "_p305_v001.fits")
        plt.xlabel('RA')
        plt.ylabel('DEC')
        plt.show()
        fig, ax = plt.subplots(1)
        img_one_mpl = plt.hist2d(evt_data['L'][ii], evt_data['B'][ii], nbins, cmap='viridis', norm=LogNorm())
        cbar = plt.colorbar(ticks=[1.0, 3.0, 6.0])
        cbar.ax.set_yticklabels(['1', '3', '6'])
        plt.title("lat_photon_weekly_w" + int_to_string(i) + "_p305_v001.fits")
        plt.xlabel('L')
        plt.ylabel('B')
        plt.show()
    concat_table = vstack(full_evt_data)
    ii = np.in1d(concat_table['CONVERSION_TYPE'], [0, 1])
    NBINS = (100, 100)
    # Start on collective rad/dec
    fig, ax = plt.subplots(1)
    img_zero_mpl = plt.hist2d(concat_table['RA'][ii], concat_table['DEC'][ii], NBINS, cmap='viridis', norm=LogNorm())
    cbar = plt.colorbar(ticks=[1.0, 3.0, 6.0])
    cbar.ax.set_yticklabels(['1', '3', '6'])
    plt.title("Time Averaged from week" + int_to_string(start_week) + "to" + int_to_string(end_wk))
    plt.xlabel('RA')
    plt.ylabel('DEC')
    plt.show()
    # start on collection L/B
    fig, ax = plt.subplots(1)
    img_one_mpl = plt.hist2d(concat_table['L'][ii], concat_table['B'][ii], NBINS, cmap='viridis', norm=LogNorm())
    cbar = plt.colorbar(ticks=[1.0, 3.0, 6.0])
    cbar.ax.set_yticklabels(['1', '3', '6'])
    plt.title("Time Averaged from week " + int_to_string(start_week) + " to " + int_to_string(end_wk))
    plt.xlabel('L')
    plt.ylabel('B')
    plt.show()
main()
