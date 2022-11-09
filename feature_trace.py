'''
Created on: 2022-Nov-08
Last changes on:

@author: Mateusz Fido, mateusz.fido@org.chem.ethz.ch
ETH Zürich

This script iterates over files in a list of .mzml files,
resamples their intensities over a common m/z axis and then
looks for and plots time-traces of a given set of features.

References:
===========
Python Code "preprocess.py" by Mateusz Fido
https://pyteomics.readthedocs.io/en/latest/index.html
'''

import os, time
from pathlib import Path
import numpy as np
from pyteomics import mzml
import matplotlib.pyplot as plt
from preprocess import read_mzml

st = time.time()    # log execution time

'''Hardcoded data paths for debugging'''
#
# Windows data path: 
# PATH = Path('C:\\Users\\drago\\OneDrive - ETH Zurich\\Kispi\\data-analysis\\test_mzml')
#
# MacOS data path: 
PATH = Path('/Users/mateuszfido/OneDrive - ETH Zurich/Kispi/data/test_kispi/')

'''Constants used for the new mz_axis'''
MZ_MIN = 50
MZ_MAX = 500
RES = 0.001
DATA_POINTS = int((MZ_MAX - MZ_MIN)/RES)

MZ_AXIS = np.linspace(MZ_MIN, MZ_MAX, DATA_POINTS, dtype=float)

'''Constants used for feature trace search'''
FEATURES_POS = [55.03897, 100.07569, 279.15909, 371.10124, 445.12004]
FEATURES_NEG  = [91.00368, 255.23295, 283.26425]

def find_nearest(array, value):
    '''
    Helper function for finding closest absolute value to the input in a given array.

    Input: array, value
   
    Returns: index of closest value to the input
    '''

    array = np.array(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def trace_features(file, features):
    '''
    Finds a list of features closest to a list of given within 5 steps of resolution on m/z axis, i.e. 
    if the resolution is 0.001 it return the maximum intensity between -0.005 and +0.005 of the given value.
    Graphs the output using the matplotlib library.

    Input: Path to .mzml file, list of features (integers or floats)
    
    Returns: None
    '''
    
    tic = []                            # Placeholder data structures 
    fig, ax = plt.subplots(2, 1)
    legend = []

    for feature in features:            # Iterate over all features in list 

        scans = mzml.MzML(str(PATH / file))

        feature_ints = []
        peak_idx = find_nearest(MZ_AXIS, feature)   # Find the closest value on the MZ_AXIS 
        
        for scan in scans:
            if len(tic) < len(scans):
                tic.append(scan['total ion current'])
            mz_array = np.ndarray.tolist(scan['m/z array'])
            intensity_array = np.ndarray.tolist(scan['intensity array'])
            int_interp = np.interp(MZ_AXIS, mz_array, intensity_array, left = 0, right = 0)
            int_range = int_interp[peak_idx - 5 : peak_idx + 5]
            feature_ints.append(max(int_range))

        ax[1].plot(feature_ints)
        legend.append(feature_ints)

    '''Graphing interface'''

    ax[0].plot(tic, color='red')
    ax[0].set_title("Total Ion Current")
    ax[1].set_title("m/z features")
    ax[1].legend(features, loc="upper right")
    plt.xlabel("Scan number")
    plt.ylabel("Counts")
    plt.tight_layout()
    plt.show()

    ''''''

def main():
    '''
    Traces features for all .mzml files found on path. Uses the read_mzml module from preprocess.py.
    Input: None
    Returns: None
    '''
    
    filelist = read_mzml(PATH)
    count = 1

    for file in filelist:
        print(f"Tracing features for file {count} out of {len(filelist)}: {file}...")
        count += 1

        if "_pos" in str(file):
            trace_features(PATH / file, FEATURES_POS)
        else:
            trace_features(PATH / file, FEATURES_NEG)


main()

et = time.time()
elapsed_time = et - st
print("Execution time: ", round(elapsed_time, 2), " seconds.")  # Log script running time