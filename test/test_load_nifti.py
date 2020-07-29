#!usr/bin/env python3
# -*- coding: utf-8

import pytest
import logging
import shutil
import os
import numpy as np
import nibabel as nib
import json

from shimmingtoolbox.load_nifti import load_nifti
from pathlib import Path

__testing_url__ = ""

class TestCore(object):
    _data = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                      [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
                      [[19, 20, 21], [22, 23, 24], [25, 26, 27]]])
    _aff  = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
    _json = {"Modality": "MR",
             "MagneticFieldStrength": 3,
             "ImagingFrequency": 123.259,
             "Manufacturer": "Siemens",
             "ManufacturersModelName": "Prisma_fit",
             "InstitutionName": "IUGM",
             "InstitutionAddress": "Chemin_Queen-Mary_4565_Montreal_District_CA_H3W_1W5",
             "DeviceSerialNumber": "167006",
             "StationName": "MRC35049",
             "BodyPartExamined": "BRAIN",
             "PatientPosition": "HFS",
             "ProcedureStepDescription": "dev_acdc",
             "SoftwareVersions": "syngo_MR_E11",
             "MRAcquisitionType": "2D",
             "SeriesDescription": "a_gre_DYNshim",
             "ProtocolName": "a_gre_DYNshim",
             "ScanningSequence": "GR",
             "SequenceVariant": "SP",
             "SequenceName": "fl2d6",
             "ImageType": ["ORIGINAL", "PRIMARY", "M", "ND"],
             "SeriesNumber": 6,
             "AcquisitionTime": "16:21:2.480000",
             "AcquisitionNumber": 1,
             "SliceThickness": 3,
             "SpacingBetweenSlices": 3,
             "SAR": 0.00453667,
             "EchoNumber": 1,
             "EchoTime": 0.0025,
             "RepetitionTime": 0.5,
             "FlipAngle": 25,
             "PartialFourier": 1,
             "BaseResolution": 128,
             "ShimSetting": [620, -7194, -9127, 77, 28, -20, -10, -23],
             "TxRefAmp": 222.944,
             "PhaseResolution": 1,
             "ReceiveCoilName": "HeadNeck_64",
             "ReceiveCoilActiveElements": "HC7;NC1,2",
             "PulseSequenceDetails": "%CustomerSeq%_a_gre_DYNshim",
             "ConsistencyInfo": "N4_VE11C_LATEST_20160120",
             "PercentPhaseFOV": 59.375,
             "EchoTrainLength": 6,
             "PhaseEncodingSteps": 76,
             "AcquisitionMatrixPE": 76,
             "ReconMatrixPE": 76,
             "PixelBandwidth": 600,
             "PhaseEncodingDirection": "j-",
             "ImageOrientationPatientDICOM": [1, 0, 0, 0, 1, 0],
             "InPlanePhaseEncodingDirectionDICOM": "COL",
             "ConversionSoftware": "dcm2niix",
             "ConversionSoftwareVersion": "v1.0.20181125  (JP2:OpenJPEG) GCC9.3.0",
             "Dcm2bidsVersion": "2.1.4"}

    def setup_method(self):
        """
        Setup documents for testing of load_nifti
        :return:
        """
        self.full_path = Path(__file__).resolve().parent
        self.test_path = self.full_path

        self.tmp_path = self.test_path / '__temp__'
        if not self.tmp_path.exists():
            self.tmp_path.mkdir()
        self.toolbox_path = self.test_path.parent

        self.data_path = self.tmp_path / 'test_data'
        self.data_path.mkdir()

        dummy_data = nib.nifti1.Nifti1Image(dataobj=self._data, affine=self._aff)
        nib.save(dummy_data, os.path.join(self.data_path, 'dummy.nii'))
        with open(os.path.join(self.data_path, 'data.json'), 'w') as json_file:
            json.dump(self._json, json_file)


    def teardown_method(self):
        """
        Tear down for testing of load_nifti
        :return:
        """
        if self.tmp_path.exists():
            shutil.rmtree(self.tmp_path)
            pass


