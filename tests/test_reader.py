import os
import numpy as np
from nd2 import ND2File
from nis2pyr.reader import read_nd2file
from nis2pyr.metadata import get_nd2_voxelsize_um, get_nd2_channels_info
from conftest import TRUTH


# Read ND2 test files, and compare specific pixels values against values
# measured in NIS-Elements Viewer.

def test_read(input_dir, any_nd2):
    filename = any_nd2
    truth = TRUTH[filename]['nd2']
    with ND2File(os.path.join(input_dir, filename)) as nd:
        # Check metadata
        assert nd.is_rgb == truth['is_rgb']
        assert get_nd2_voxelsize_um(nd) == truth['voxelsize']
        assert get_nd2_channels_info(nd) == truth['channels']

        # Check image data
        image = read_nd2file(nd)
        assert image.shape == truth['shape']
        assert image.dtype == truth['dtype']
        for coords, values in truth['pixels']:
            assert np.array_equal(image[coords], values)
