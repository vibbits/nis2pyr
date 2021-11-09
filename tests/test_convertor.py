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
    if nd2_truth['is_rgb']:
        numt, _, numz, _, _, _, numc = nd2_truth['shape']
    else:
        numt, _, numz, numc, _, _, _ = nd2_truth['shape']

    # Check pixel values
    for coords, intensity in nd2_truth['pixels']:
        if nd2_truth['is_rgb']:
            t, p, z, _, y, x, c = coords
            idx = _page_index_rgb(t, p, z, numt, numz)
            image = tiff.pages[idx].asarray()
            assert image[y, x, c] == intensity
        else:
            t, p, z, c, _, y, x = coords
            idx = _page_index_nonrgb(t, p, z, c, numt, numz, numc)
            image = tiff.pages[idx].asarray()
            assert image[y, x] == intensity


def test_channels_info(tiff, nd2_truth):
    if nd2_truth['is_rgb']:
        _, nump, _, _, _, _, numc = nd2_truth['shape']
    else:
        _, nump, _, numc, _, _, _ = nd2_truth['shape']

    # Check OME channel names and colors
    ome = ome_types.from_xml(tiff.ome_metadata)
    assert len(ome.images) == nump
    for p in range(nump):
        ome_channels = ome.images[p].pixels.channels
        if nd2_truth['is_rgb']:
            assert len(ome_channels) == 1
            assert ome_channels[0].samples_per_pixel == 3
        else:
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
# In the non-RGB case, the pixels for each channel are stored in a separate page.
# In the RGB case on the other hand, the R, G and B "channels" are seen as 
# 3 components of one channel, and all 3 components are stored pixel-interleaved
# in the same TIFF page.

def _page_index_nonrgb(t: int, p: int, z: int, c: int,
                       numt: int, numz: int, numc: int) -> int:
    return c + numc * (z + numz * (t + numt * p))


def _page_index_rgb(t: int, p: int, z: int,
                    numt: int, numz: int) -> int:
    return z + numz * (t + numt * p)
