# feature_trace

Created on: 2022-Nov-08
Last changes on: 2022-Nov-09

@author: Mateusz Fido, mateusz.fido@org.chem.ethz.ch
ETH Zürich

This script iterates over files in a list of .mzml files,
resamples their intensities over a common m/z axis and then
writes them into .csv files together with the total ion current
and the m/z of the feature on index 0.

References:
===========
Python Code "preprocess.py" by Mateusz Fido
https://pyteomics.readthedocs.io/en/latest/index.html
