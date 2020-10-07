#!/bin/bash
#
# This function will generate static and dynamic (due to respiration) Gz components based on a fieldmap time series
# (magnitude and phase images) and respiratory trace information obtained from Siemens bellows. An additional
# multi-gradient echo (MGRE) magnitude image is used to generate an ROI and resample the static and dynaminc Gz
# component maps to match the MGRE image. Lastly the average Gz values within the ROI are computed for each slice.

# Download example data
st_download_data testing_data

# Go inside folder
cd testing_data/realtime_zshimming_data

# dcm2bids -d . -o nifti -p sub-example -c ../../config/dcm2bids.json
st_dicom_to_nifti -i . -o nifti -sub sub-example
cd nifti/sub-example/fmap

# Calling FSL directly
fsl_prepare_fieldmap SIEMENS sub-example_phasediff.nii.gz sub-example_magnitude1.nii.gz sub-example_phasediff_unwrapped.nii.gz 2.46 --nocheck
fslmaths sub-example_phasediff_unwrapped.nii.gz -div 0.00246 sub-example_fieldmap.nii.gz

# Not implemented:
# <<
# Using our CLI:
#st_unwrap_prelude -phase sub-example_phasediff.nii.gz -mag sub-example_magnitude1.nii.gz
# default output will be -phase with suffix _unwrapped
#st_compute_b0field -phase sub-example_phasediff_unwrapped.nii.gz -o sub-example_fieldmap.nii.gz
# fieldmap.nii is a 4d file, with the 4th dimension being the time. Ie: one B0 field per time point.
# >>

# Mask anatomical image
# Calling FSL directly
fslmaths sub-example_T2star_echo-1.nii.gz -thr 500 mask.nii.gz
fslmaths mask.nii.gz -bin mask.nii.gz
# Not implemented:
# <<
#st_mask -method sct
# Alternatively, you could run it with arbitrary shape:
# st_mask -method shape -shape cube -size 5 -o mask.nii
# >>

# Generate a coil profile based on the spherical harmonics basis
st_generate_profile_spherical_harmonics -i sub-example_fieldmap.nii.gz -order 2 -o coil_profile.nii.gz
# Alternatively: use custom coil geomtry:
#st_generate_profile_custom
# Alternatively: Use already-available profiles
#st_download_data coil_profile_my_awesome_coil

# Note: the original realtime z-shimming implemented did not use the coil profile because it directly computed the Gz
# from the estimated static and dynamic (riro) fieldmaps_Gz:
# https://github.com/shimming-toolbox/shimming-toolbox-matlab/blob/master/example/realtime_zshim.m#L356

st_shim -fmap fieldmap.nii [-coil-profile $SHIM_DIR/coils/siemens_terra.nii] -mask mask.nii -physio XX -method {volumewise, slicewise}
# st_shim will:
# - resample coil profile into the space of fieldmap.nii
# - resample (in time) the physio trace to the 4d fieldmap data so that each time point of the fieldmap has its corresponding respiratory probe value.
# - run optimizer within mask.nii
# - outputs:
#   - fieldmap_shimmed.nii
#   - coefficients.csv
#   - figures

# Output text file to be read by syngo console
# TODO