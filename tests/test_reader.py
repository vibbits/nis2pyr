import os
import numpy as np
import pytest
from nd2 import ND2File
from nis2pyr.reader import read_nd2file
from nis2pyr.metadata import get_nd2_voxelsize_um, get_nd2_channels_info
from conftest import TRUTH


# Fixture that will open an ND2 file and pass it on to the actual
# test functions.
@pytest.fixture(scope="module")
def nd(input_dir, any_nd2):
    with ND2File(os.path.join(input_dir, any_nd2)) as nd:
        yield nd


def test_metadata(nd):
    filename = os.path.basename(nd.path)
    truth = TRUTH[filename]['nd2']
    assert nd.is_rgb == truth['is_rgb']
    assert get_nd2_voxelsize_um(nd) == truth['voxelsize']
    assert get_nd2_channels_info(nd) == truth['channels']


# Test which compares specific pixel values in the image read with the nd2
# library, with ground truth values measured in NIS-Elements Viewer.
def test_pixels(nd):
    filename = os.path.basename(nd.path)
    image = read_nd2file(nd)
    truth = TRUTH[filename]['nd2']
    assert image.shape == truth['shape']
    assert image.dtype == truth['dtype']
    for coords, values in truth['pixels']:
        assert np.array_equal(image[coords], values)