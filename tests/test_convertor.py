import os
import ome_types
import pytest
from pathlib import Path
from tifffile import TiffFile, TIFF
from nis2pyr.convertor import convert_nd2_to_pyramidal_ome_tiff


DEFAULT_TILE_SIZE = 256
DEFAULT_PYRAMID_LEVELS = 6


# Fixture that opens an ND2 file, converts it to a pyramidal OME TIFF,
# and pass on the TIFF file to test functions that will check the structure
# and contents of the TIFF file.
@pytest.fixture(scope="module")
def tiff(input_dir, output_dir, any_nd2):
    filename = any_nd2
    nd2_filename = os.path.join(input_dir, filename)
    pyramid_filename = os.path.join(output_dir,
                                    os.path.basename(Path(nd2_filename)
                                                     .with_suffix('.ome.tif')))

    convert_nd2_to_pyramidal_ome_tiff(nd2_filename,
                                      pyramid_filename,
                                      compression='zlib')

    yield TiffFile(pyramid_filename)


def test_not_rgb(nd2_truth):
    # For now the test code below only supports non-RGB images
    assert not nd2_truth['is_rgb']


def test_basic(tiff):
    assert tiff.is_ome
    assert tiff.is_bigtiff


def test_pages(tiff, tiff_truth):
    assert len(tiff.pages) == tiff_truth['pages']        
    for page in tiff.pages:
        assert page.tilewidth == DEFAULT_TILE_SIZE
        assert page.tilelength == DEFAULT_TILE_SIZE
        assert page.compression == TIFF.COMPRESSION.ADOBE_DEFLATE
        assert page.photometric == tiff_truth['photometric']


def test_series(tiff, tiff_truth):
    assert len(tiff.series) == tiff_truth['series']
    for series in tiff.series:
        assert series.is_pyramidal
        assert len(series.levels) == DEFAULT_PYRAMID_LEVELS


def test_pixels(tiff, nd2_truth):
    # Check pixel values
    numt, nump, numz, numc, _, _, _ = nd2_truth['shape']
    for coords, intensity in nd2_truth['pixels']:
        t, p, z, c, _, y, x = coords
        idx = _page_index(t, p, z, c, numt, nump, numz, numc)
        image = tiff.pages[idx].asarray()
        assert image[y, x] == intensity


def test_channels_info(tiff, nd2_truth):
    # Check OME channel names and colors
    _, nump, _, numc, _, _, _ = nd2_truth['shape']
    ome = ome_types.from_xml(tiff.ome_metadata)
    assert len(ome.images) == nump
    for p in range(nump):
        ome_channels = ome.images[p].pixels.channels
        assert len(ome_channels) == numc
        for c in range(numc):
            nd2_channels = nd2_truth['channels']
            if nd2_channels is None:
                assert ome_channels[c].name is None
            else:
                assert ome_channels[c].name == nd2_channels[c][0]
                assert ome_channels[c].color.as_rgb_tuple() == \
                       nd2_channels[c][1]


# Conversion of n-dimensional image coordinates to the OME TIFF page number.
# This is still tentative and needs more extensive testing.
def _page_index(t: int, p: int, z: int, c: int,
                numt: int, _: int, numz: int, numc: int) -> int:
    return c + numc * (z + numz * (t + numt * p))
