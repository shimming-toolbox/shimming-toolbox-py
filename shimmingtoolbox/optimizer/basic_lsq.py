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
        self._error_if(self.coils is None, "No loaded coil profiles!")
        self._error_if(unshimmed.ndim != 3,
                       f"Unshimmed profile has {unshimmed.ndim} dimensions, expected 3 (X, Y, Z)")
        self._error_if(mask.ndim != 3, f"Mask has {mask.ndim} dimensions, expected 3 (X, Y, Z)")
        self._error_if(unshimmed.shape != (self.X, self.Y, self.Z),
                       f"XYZ mismatch -- Coils: {self.coils.shape}, Unshimmed: {unshimmed.shape}")
        for i in range(3):
            self._error_if(mask.shape[i] + mask_origin[i] > (self.X, self.Y, self.Z)[i],
                           f"Mask (shape: {mask.shape}, origin: {mask_origin}) goes out of bounds "
                           f"(coil shape: {(self.X, self.Y, self.Z)}")
        self._error_if(len(bounds) != self.N and bounds is not None, f"Bounds should have the same number of (min, max)"
                                                                     f" tuples as coil channels")

        # Set up mask
        full_mask = np.zeros((self.X, self.Y, self.Z))
        full_mask[mask_origin[0]:mask_origin[0] + mask.shape[0], mask_origin[1]:mask_origin[1] + mask.shape[1], mask_origin[2]:mask_origin[2] + mask.shape[2]] = mask
        full_mask = np.where(full_mask != 0, 1, 0)
        
        masked_unshimmed = unshimmed * full_mask
        masked_coils = self.coils * full_mask.reshape(full_mask.shape + (1,))

        # Set up output currents and optimize
        currents = np.zeros(self.N)

        currents = opt.minimize(self._objective, currents, args=(masked_unshimmed, masked_coils), bounds=bounds).x

        return currents

    def _error_if(self, err_condition, message):
        """
        Helper function throwing errors

        Args:
            err_condition (bool): Condition to throw error on
            message (string): Message to log and throw
        """
        if err_condition:
            self.logger.error(message)
            raise RuntimeError(message)
