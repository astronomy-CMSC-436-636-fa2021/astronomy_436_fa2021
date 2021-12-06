import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
# plt.style.use(astropy_mpl_style)
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
import copy

full_evt_data = []
full_sum_energy = 0
start_week = 0
end_week = 0
full_weights = []


def do_some_prompts():
    # Todo - make this better prompt, probably with GUI
    # in this file, I want to prompt the user for a date range
    okay = False
    while (not (okay)):
        # todo: convert to a GUI picking actual weeks rather than numerically
        week_start = int(input("What week would you like to start (009 minimum)"))
        week_end = int(input("What week would you like to end? (700 max)"))
        temp = input("There will be approximately {} MB for those files, is that ok?(y/n)".format(
            60 * (week_end - week_start + 1)))
        if (temp == 'y'):
            okay = True
        #return week_start, week_end, 0, 0
    okay = False
    while (not (okay)):
        print("Getting values for bounds of energy, measured in MeV. Enter 0 for both if you don't want to use Energy Filtering")
        energy_start = float(input("What is your lower bound for the energy? (Recommend no lower than 20)"))
        energy_end = float(input("What is your upper bound for the energy (Recommend no higher than 3500)"))
        if energy_end > energy_start or (energy_end == 0 and energy_start == 0):
            okay = True
        else:
            print("That range does not make sense, please put them in order.")
    return week_start, week_end, energy_start, energy_end


def int_to_string(i):
    if (i <= 9):
        return "00" + str(i)
    if (i < 99):
        return "0" + str(i)
    else:
        return str(i)


def download_some_files(week_strt, week_end):
    dl_root = "https://heasarc.gsfc.nasa.gov/FTP/fermi/data/lat/weekly/photon/"
    dl_path = os.path.join("fits", "archive")
    ssl._create_default_https_context = ssl._create_unverified_context
    for i in range(week_strt, week_end + 1):
        # print()
        dl_link = dl_root + "lat_photon_weekly_w{fname}_p305_v001.fits".format(fname=int_to_string(i))
        # print(dl_link)
        urllib.request.urlretrieve(dl_link, "lat_photon_weekly_w{}_p305_v001.fits".format(int_to_string(i)))


def procedural_gen_full(start_week, end_week, energy_start, energy_end):
    full_evt_data = list()
    total_sum = 0
    # user_input=input("enter fit file\n")
    for i in range(start_week, end_week + 1):
        file_to_open = str(Path().absolute()) + "\\lat_photon_weekly_w" + int_to_string(i) + "_p305_v001.fits"
        image_file = fits.open(file_to_open, memmap=True)
        my_table = Table(image_file[1].data)
        image_file.close()
        # dropping these rows makes the future sort much faster
        del (my_table['THETA'])
        del (my_table['PHI'])
        del (my_table['ZENITH_ANGLE'])
        del (my_table['EARTH_AZIMUTH_ANGLE'])
        del (my_table['TIME'])
        del (my_table['EVENT_ID'])
        del (my_table['RUN_ID'])
        del (my_table['RECON_VERSION'])
        del (my_table['CALIB_VERSION'])
        del (my_table['EVENT_CLASS'])
        del (my_table['EVENT_TYPE'])
        del (my_table['LIVETIME'])
        del (my_table['DIFRSP0'])
        del (my_table['DIFRSP1'])
        del (my_table['DIFRSP2'])
        del (my_table['DIFRSP3'])
        del (my_table['DIFRSP4'])
        # we are going to use the weights argument in hist2d to do the cutoffs
        my_weights = copy.deepcopy(my_table['ENERGY'])
        for loop_through_weights in range(len(my_weights)):
            item = my_weights[loop_through_weights]
            if energy_start == 0 or energy_end == 0:
                continue
            if item < energy_start or item > energy_end:
                my_weights[loop_through_weights] = 0 # if the item is outside the range, we replace it with 0

        full_weights.extend(my_weights)
        #my_table.show_in_browser()
        #myTable.remove_rows()
        full_evt_data.append(my_table)  # add opened table to collection
        hist_plot_occurrences(my_table, i,my_weights)
        energy_hist(my_table, i,my_weights)
    # now that those are done, we can do it for the full image
    concat_table = vstack(full_evt_data)
    hist_plot_occurrences(concat_table, -1,full_weights)
    energy_hist(concat_table, -1,full_weights)


def hist_plot_occurrences(evt_data, i, my_weights):
    # produces the plot_occurrences histogram, for Radial and Declination Coords
    # image_file.info() debug info about the FITS
    # starting plt hist2d -
    my_start_week = start_week
    my_end_week = end_week
    nbins = (500, 500)
    fig, ax = plt.subplots(1)
    ii = np.in1d(evt_data['CONVERSION_TYPE'], [0, 1])
    img_zero_mpl = plt.hist2d(evt_data['RA'][ii], evt_data['DEC'][ii], nbins, cmap='viridis', norm=LogNorm(), weights=np.ceil(np.tanh(my_weights)))
    cbar = plt.colorbar(ticks=[1.0, 3.0, 6.0])
    cbar.ax.set_yticklabels(['1', '3', '6'])
    if i < 0:
        save_title = f"OccurrenceWeighted_RADEC_weeks_{int_to_string(start_week)}_to_{int_to_string(end_week)}"
        plt.title(f"Occurrence Weighted Time Averaged from week {int_to_string(my_start_week)} to {int_to_string(my_end_week)}")
    else:
        save_title = f"OccurrenceWeighted_RADEC_week_{int_to_string(i)}"
        plt.title("Occurrence Weighted - week " + int_to_string(i))
    plt.xlabel('RA')
    plt.ylabel('DEC')
    plt.savefig(fname=str(Path().absolute())+f"\\outputs\\{save_title}.svg",format='svg')
    plt.show()
    fig, ax = plt.subplots(1)
    img_one_mpl = plt.hist2d(evt_data['L'][ii], evt_data['B'][ii], nbins, cmap='viridis', norm=LogNorm(), weights=np.ceil(np.tanh(my_weights)))
    cbar = plt.colorbar(ticks=[1.0, 3.0, 6.0])
    cbar.ax.set_yticklabels(['1', '3', '6'])
    if i < 0:
        save_title = f"OccurrenceWeighted_LB_weeks_{int_to_string(start_week)}_to_{int_to_string(end_week)}"
        plt.title(f"Occurrence Weighted Time from week {int_to_string(start_week)} to {int_to_string(end_week)}")
    else:
        save_title = f"OccurrenceWeighted_LB_week_{int_to_string(i)}"
        plt.title("Occurrence Weighted - week" + int_to_string(i))
    plt.xlabel('L')
    plt.ylabel('B')
    plt.savefig(fname=str(Path().absolute()) + f"\\outputs\\{save_title}.svg", format='svg')
    plt.show()


def energy_hist(evt_data, i, my_weights):
    # uses the sum of energy to create a scatter plot with the scaling being the current event_data/sum
    sum_energy = sum(evt_data['ENERGY'])
    # print (sum_energy)
    nbins = (500, 500)
    fig, ax = plt.subplots(1)
    ii = np.in1d(evt_data['CONVERSION_TYPE'], [0, 1])
    img_two_mpl = plt.hist2d(evt_data['RA'][ii], evt_data['DEC'][ii],nbins,cmap='cividis', weights=my_weights/sum_energy, norm=LogNorm())
    # cbar = plt.colorbar(ticks=[1.0, 3.0, 6.0])
    # cbar.ax.set_yticklabels(['1', '3', '6'])
    if i < 0:
        save_title = f"EnergyWeighted_RADEC_weeks_{int_to_string(start_week)}_to_{int_to_string(end_week)}"
        plt.title(save_title := f"Energy Weighted Averaged from week {int_to_string(start_week)} to {int_to_string(end_week)}")
    else:
        save_title = f"OccurrenceWeighted_RADEC_week_{int_to_string(i)}"
        plt.title(save_title := "Energy Weighted - week" + int_to_string(i))
    plt.xlabel('RA')
    plt.ylabel('DEC')
    plt.savefig(fname=str(Path().absolute()) + f"\\outputs\\{save_title}.svg", format='svg')
    plt.show()
    fig, ax = plt.subplots(1)
    img_three_mpl = plt.hist2d(evt_data['L'][ii], evt_data['B'][ii],nbins,cmap='cividis', weights=my_weights/sum_energy,norm=LogNorm())
    # cbar = plt.colorbar(ticks=[1.0, 3.0, 6.0])
    # cbar.ax.set_yticklabels(['1', '3', '6'])
    if i < 0:
        save_title = f"EnergyWeighted_LB_weeks_{int_to_string(start_week)}_to_{int_to_string(end_week)}"
        plt.title(save_title := f"Energy Weighted, Time Averaged from week {int_to_string(start_week)} to {int_to_string(end_week)}")
    else:
        save_title = f"OccurrenceWeighted_LB_week_{int_to_string(i)}"
        plt.title(save_title := "Energy Weighted,lat_photon_weekly_w" + int_to_string(i) + "_p305_v001.fits")
    plt.xlabel('L')
    plt.ylabel('B')
    plt.savefig(fname=str(Path().absolute()) + f"\\outputs\\{save_title}.svg", format='svg')
    plt.show()


def main():
    global start_week, end_week, start_eng_range, end_eng_range
    start_week, end_week, start_eng_range, end_eng_range = do_some_prompts()
    download_some_files(start_week, end_week)
    try:
        if os.path.isdir(str(Path().absolute()) + f"\\outputs\\"):
            pass
        else:
            os.makedirs(str(Path().absolute()) + f"\\outputs\\")
    except:
        print("Raised Exception")
    procedural_gen_full(start_week, end_week, start_eng_range, end_eng_range)


main()
