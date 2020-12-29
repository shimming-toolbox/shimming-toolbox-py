#!usr/bin/env python3
# -*- coding: utf-8

from distutils.dir_util import copy_tree

import goop
import json
import numpy as np
import os
import re
import sys
import subprocess
import dcm2bids
# from dcm2bids.scaffold import scaffold
import shutil

from shimmingtoolbox import __dir_config_dcm2bids__


def dicom_to_nifti(path_dicom, path_nifti, subject_id='sub-01', path_config_dcm2bids=__dir_config_dcm2bids__, remove_tmp=False):
    """ Converts dicom files into nifti files by calling dcm2bids

    Args:
        path_dicom (str): path to the input dicom folder
        path_nifti (str): path to the output nifti folder

    """

    # Create the folder where the nifti files will be stored
    if not os.path.exists(path_dicom):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path_config_dicom)
        #No dicom path found at



    if not os.path.exists(path_config_dcm2bids):
        #error_message = "No dcm2bids config file found at:" #TODO: Charlotte can I put error_message back in?
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path_config_dcm2bids)
        #error_message = None
    if not os.path.exists(path_nifti):
        os.makedirs(path_nifti)

    # dcm2bids is broken for windows as a python package so using CLI
    # Create bids structure for data
    subprocess.run(['dcm2bids_scaffold', '-o', path_nifti], check=True)

    #
    # # Copy original dicom files into nifti_path/sourcedata
    copy_tree(path_dicom, os.path.join(path_nifti, 'sourcedata'))
    #
    # # Call the dcm2bids_helper
    subprocess.run(['dcm2bids_helper', '-d', path_dicom, '-o', path_nifti], check=True)
    #
    # Check if the helper folder has been created
    path_helper = os.path.join(path_nifti, 'tmp_dcm2bids', 'helper')
    if not os.path.isdir(path_helper):
        error_message ='dcm2bids_helper could not create directory helper'
        raise ValueError(error_message)
        error_message = None

    #TODO: Charlotte: put all these errors in a languae file! otherwise good luck with localizations. Clear it but leave it in globally
    # Make sure there is data in nifti_path / tmp_dcm2bids / helper
    helper_file_list = os.listdir(path_helper)
    if not helper_file_list:
        error_message = 'No data to process'
        raise ValueError(error_message)
        error_message = None

    subprocess.run(['dcm2bids', '-d', path_dicom, '-o', path_nifti, '-p', subject_id, '-c', path_config_dcm2bids],
                   check=True)

    # In the special case where a phasediff should be created but the filename is phase instead. Find the file and
    # rename it
    # Go in the fieldmap folder
    path_fmap = os.path.join(path_nifti, subject_id, 'fmap')
    if os.path.exists(path_fmap):
        # Make a list of the json files in fmap folder
        file_list = []

        for file in glob.glob("*.json", recursive=False):
            file_list.append(os.path.join(path_fmap, file)) for file in os.listdir(path_fmap)
            file_list = sorted(file_list)

        for fname_json in file_list:
            is_renaming = False
            # Open the json file
            with open(fname_json) as json_file:
                json_data = json.load(json_file)
                # Make sure it is a phase data and that the keys EchoTime1 and EchoTime2 are defined and that
                # sequenceName's last digit is 2 (refers to number of echoes when using dcm2bids)


#TODO Charlotte clean this up.
                if ('ImageType' in json_data) and ('P' in json_data['ImageType']) and \
                   ('EchoTime1' in json_data) and ('EchoTime2' in json_data) and \
                   ('SequenceName' in json_data) and (int(json_data['SequenceName'][-1]) == 2):
                        fname_new_json = fname_json =  re.sub('[0-9]', '', fname)
                        is_renaming = True
            # Rename the json file an nifti file 
            if is_renaming:
                #TODO: Charlotte I dont't like splittext
                if os.path.exists(os.path.splitext(fname_json)[0] + '.nii.gz'):
                    fname_nifti_new = os.path.splitext(fname_new_json)[0] + '.nii.gz'
                    fname_nifti_old = os.path.splitext(fname_json)[0] + '.nii.gz'
                    os.rename(fname_nifti_old, fname_nifti_new)
                    os.rename(fname_json, fname_new_json)

    if remove_tmp:
        shutil.rmtree(os.path.join(path_nifti, 'tmp_dcm2bids'))
