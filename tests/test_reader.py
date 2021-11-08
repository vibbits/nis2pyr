import os
import numpy as np
import pytest
from nd2 import ND2File
from nis2pyr.reader import read_nd2file
from nis2pyr.metadata import get_nd2_voxelsize_um, get_nd2_channels_info


# Fixture that will open an ND2 file and pass it on to the actual
# test functions.
@pytest.fixture(scope="module")
def nd(input_dir, any_nd2):
    with ND2File(os.path.join(input_dir, any_nd2)) as nd:
        yield nd


def test_metadata(nd, nd2_truth):
    assert nd.is_rgb == nd2_truth['is_rgb']
    assert nd.is_legacy == nd2_truth['is_legacy']
    assert get_nd2_voxelsize_um(nd) == nd2_truth['voxelsize']
    assert get_nd2_channels_info(nd) == nd2_truth['channels']


# Test which compares specific pixel values in the image read with the nd2
# library, with ground truth values measured in NIS-Elements Viewer.
def test_pixels(nd, nd2_truth):
    image = read_nd2file(nd)
    assert image.shape == nd2_truth['shape']
    assert image.dtype == nd2_truth['dtype']
    for coords, values in nd2_truth['pixels']:
        assert np.array_equal(image[coords], values)
