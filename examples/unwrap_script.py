#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" This script will:
- download 2-echo phase fieldmap data
- do the subtraction
- unwrap phase difference
- save wrapped and unwrapped plot of first X,Y volume as myplot.png in current directory
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from zipfile import ZipFile
import glob
import requests

import nibabel as nib

from shimmingtoolbox.unwrap import prelude


def main():

    # Download example data
    url = 'https://github.com/shimming-toolbox/data-testing/archive/r20200709.zip'
    filename = 'data-testing.zip'

    r = requests.get(url)
    open(filename, 'wb').write(r.content)

    with ZipFile(filename, 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall()
    os.remove(filename)
    # TODO: use systematic name for data-testing (could be in metadata of shimmingtoolbox
    path_data = glob.glob('data-test*')[0]

    # Open phase data
    fname_phases = glob.glob(os.path.join(path_data, 'sub-fieldmap', 'fmap', '*phase*.nii.gz'))
    if len(fname_phases) > 2:
        raise IndexError('Phase data parsing is wrongly parsed')

    nii_phase_e1 = nib.load(fname_phases[0])
    nii_phase_e2 = nib.load(fname_phases[1])

    # Scale to phase to radians
    phase_e1 = nii_phase_e1.get_fdata() / 4096 * 2 * np.pi - np.pi
    phase_e2 = nii_phase_e2.get_fdata() / 4096 * 2 * np.pi - np.pi

    # Open mag data
    fname_mags = glob.glob(os.path.join(path_data, 'sub-fieldmap', 'fmap', '*magnitude*.nii.gz'))

    if len(fname_mags) > 2:
        raise IndexError('Mag data parsing is wrongly parsed')

    nii_mag_e1 = nib.load(fname_mags[0])
    nii_mag_e2 = nib.load(fname_mags[1])

    # TODO: Convert to a function b0_map
    # phasediff: (matlab code for 2 echoes)
    # Z1(:,:,:) = mag_data(:,:,:,1).*exp(1i*ph_data(:,:,:,1));
    # Z2(:,:,:) = mag_data(:,:,:,2).*exp(1i*ph_data(:,:,:,2));
    # atan2(imag(Z1(:,:,:).*conj(Z2(:,:,:))),real(Z1(:,:,:).*conj(Z2(:,:,:))));
    # Convert to radians (Assumes there are wraps)

    # TODO: create mask
    # Call SCT or user defined mask
    # mask = np.ones(phase_diff.shape)

    # Call prelude to unwrap the phase
    unwrapped_phase_e1 = prelude(phase_e1, nii_mag_e1.get_fdata(), nii_phase_e1.affine)
    unwrapped_phase_e2 = prelude(phase_e2, nii_mag_e2.get_fdata(), nii_phase_e1.affine)

    # Compute phase difference
    unwrapped_phase = unwrapped_phase_e2 - unwrapped_phase_e1

    # Compute wrapped phase diff
    wrapped_phase = phase_e2 - phase_e1

    # Plot results
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(wrapped_phase[:-1, :-1, 0])
    plt.title("Wrapped")
    plt.colorbar()
    plt.subplot(1, 2, 2)
    plt.imshow(unwrapped_phase[:-1, :-1, 0])
    plt.title("Unwrapped")
    plt.colorbar()
    # plt.show()
    plt.savefig("unwrap_phase_plot.png")


if __name__ == '__main__':
    main()