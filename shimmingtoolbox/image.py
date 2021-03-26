#!/usr/bin/python3
# -*- coding: utf-8 -*

import numpy as np
import nibabel as nib
from typing import List

ListNii = List[nib.Nifti1Image]


def concat_data(list_nii: ListNii, dim, pixdim=None):
    """
    Concatenate data

    Args:
        list_nii: list of Nifti1Image
        dim: dimension: 0, 1, 2, 3.
        pixdim: pixel resolution to join to image header
    Returns:
        ListNii: concatenated image
    """
    # WARNING: calling concat_data in python instead of in command line causes a non-understood issue (results are
    # different with both options) from numpy import concatenate, expand_dims

    dat_list = []
    data_concat_list = []

    for i, nii_im in enumerate(list_nii):
        # if there is more than 100 images to concatenate, then it does it iteratively to avoid memory issue.
        if i != 0 and i % 100 == 0:
            data_concat_list.append(np.concatenate(dat_list, axis=dim))
            dat = nii_im.get_fdata()
            # if image shape is smaller than asked dim, then expand dim
            if len(nii_im.shape) <= dim:
                dat = _expand_dims(dat, dim)
            dat_list = [dat]
            del nii_im
            del dat
        else:
            dat = nii_im.get_fdata()
            # if image shape is smaller than asked dim, then expand dim
            if len(nii_im.shape) <= dim:
                dat = _expand_dims(dat, dim)
            dat_list.append(dat)
            del nii_im
            del dat
    if data_concat_list:
        data_concat_list.append(np.concatenate(dat_list, axis=dim))
        data_concat = np.concatenate(data_concat_list, axis=dim)
    else:
        data_concat = np.concatenate(dat_list, axis=dim)

    im_in_first = list_nii[0]
    nii_out = nib.Nifti1Image(data_concat, im_in_first.affine, im_in_first.header)

    if pixdim is not None:
        cur_pixdim = list_nii[0].header['pixdim']
        cur_pixdim[dim + 1] = pixdim
        nii_out.header['pixdim'] = cur_pixdim

    # TODO: the line below fails because .dim is immutable. We should find a solution to update dim accordingly
    #  because as of now, this field contains wrong values (in this case, the dimension should be changed). Also
    #  see mean()
    # im_out.dim = im_out.data.shape[:dim] + (1,) + im_out.data.shape[dim:]

    return nii_out


def _expand_dims(data, axis):
    """
    Expand the shape of an array.

    Wrapper to np.expand_dims allowing axis to be any dimension greater than 0

    Args:
        data (numpy.ndarray): Input array.
        axis (int): axis

    Returns:
        numpy.ndarray: Expanded array

    """

    while len(data.shape) <= axis:
        data = np.expand_dims(data, len(data.shape))

    return data
