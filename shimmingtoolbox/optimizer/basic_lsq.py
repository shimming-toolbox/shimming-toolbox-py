#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import scipy.optimize as opt

from shimmingtoolbox.optimizer.basic_optimizer import Optimizer


class BasicLSQ(Optimizer):

    def _objective(self, coef, masked_unshimmed, masked_coils):
        """
        Objective function to minimize
        Args:
            coef (numpy.ndarray): 1D array of channel coefficients
            masked_unshimmed (numpy.ndarray): 3D array of the masked unshimmed map
            masked_coils (numpy.ndarray): 4D array (X, Y, Z, channel) of masked coils

        Returns:
            float: Result that shows the performance on the coef inputs

        """
        shimmed = masked_unshimmed + np.sum(masked_coils * coef, axis=3, keepdims=False)
        objective = np.std(shimmed) + np.sum(coef)/100000
        return objective

    def optimize(self, unshimmed, mask, mask_origin=(0, 0, 0), bounds=None):
        """
        Optimize unshimmed volume by varying current to each channel

        Args:
            unshimmed (numpy.ndarray): 3D B0 map
            mask (numpy.ndarray): 3D integer mask used for the optimizer (only consider voxels with non-zero values).
            mask_origin (tuple): Mask origin if mask volume does not cover unshimmed volume
            bounds (list): List of ``(min, max)`` pairs for each coil channels. None
               is used to specify no bound.

        Returns:
            numpy.ndarray: Coefficients corresponding to the coil profiles that minimize the objective function
                           (coils.size)
        """

        # Check for sizing errors
        self._check_sizing(unshimmed, mask, mask_origin=mask_origin, bounds=bounds)

        mx, my, mz = mask_origin
        mX, mY, mZ = mask.shape

        # Set up masked submatrices
        masked_unshimmed = np.where(mask != 0, unshimmed[mx:mx+mX, my:my+mY, mz:mz+mZ], 0)
        masked_coils = np.where(mask.reshape(mask.shape + (1,)) != 0, self.coils[mx:mx+mX, my:my+mY, mz:mz+mZ, :], 0)

        # Set up output currents and optimize
        currents = np.zeros(self.N)

        currents = opt.minimize(self._objective, currents, args=(masked_unshimmed, masked_coils), bounds=bounds).x

        return currents
