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
    numt, nump, numz, numc, _, _, nums = nd2_truth['shape']

    # Check pixel values
    for coords, intensity in nd2_truth['pixels']:
        t, p, z, c, y, x, s = coords
        idx = _page_index(t, p, z, c, numt, nump, numz, numc)
        image = tiff.pages[idx].asarray()
        if nums == 1:
            assert image[y, x] == intensity
        else:
            assert image[y, x, s] == intensity


# RGB OME TIFF files are somewhat odd because they have SizeC == 3
# but only one <Channel> tag in the OME XML metadata:
#
# <Image ID="Image:1" Name="">
#   <Pixels ... SizeC="3" ...>
#     <Channel ID="Channel:0:0" ... SamplesPerPixel="3"></Channel>
#   </Pixels>
# </Image>
#
# See the example file on the OME TIFF website:
# https://downloads.openmicroscopy.org/images/OME-TIFF/2016-06/sub-resolutions/Brightfield/Leica-1/Leica-1.ome.tiff
#
# Non RGB image which happens to have 3 channels too:
#
# <Image ID="Image:0" Name="multi-channel-4D-series.ome.tif">
#   <Pixels ... SizeC="3" ...>
#     <Channel ID="Channel:0:0" SamplesPerPixel="1"></Channel>
#     <Channel ID="Channel:0:1" SamplesPerPixel="1"></Channel>
#     <Channel ID="Channel:0:2" SamplesPerPixel="1"></Channel>
#   </Pixels>
# </Image>
#
# Summary
# -------
# For RGB OME TIFFs we have
# - SizeC == 3
# - but only 1 OME Channel tag
# - nums == 3
# - numc == 1
# For non-RGB we have
# - sizeC == numc == n
# - nums == 1
# - n OME Channel tags

def test_ome_image_shape(tiff, nd2_truth):
    numt, nump, numz, numc, height, width, nums = nd2_truth['shape']  # TPZCYXS
    sizec = nums if nd2_truth['is_rgb'] else numc

    ome = ome_types.from_xml(tiff.ome_metadata)

    assert len(ome.images) == nump
    for p in range(nump):
        pixels = ome.images[p].pixels
        assert pixels.size_x == width
        assert pixels.size_y == height
        assert pixels.size_t == numt
        assert pixels.size_z == numz
        assert pixels.size_c == sizec

        ome_channels = ome.images[p].pixels.channels
        assert len(ome_channels) == numc
        for c in range(numc):
            assert ome_channels[c].samples_per_pixel == nums


def test_channels_info(tiff, nd2_truth):
    _, nump, _, numc, _, _, _ = nd2_truth['shape']  # TPZCYXS

    # Check OME channel names and colors
    ome = ome_types.from_xml(tiff.ome_metadata)
    assert len(ome.images) == nump
    for p in range(nump):
        ome_channels = ome.images[p].pixels.channels
        assert len(ome_channels) == numc  # note: for RGB we have numc=1 (not 3)
        if not nd2_truth['is_rgb']:
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
# In the RGB case on the other hand, the R, G and B are treated as 3 components
# of a single RGB channel, and all 3 components are stored pixel-interleaved
# in the same TIFF page. (So for RGB we have numc=1, c always 0, nums=3)

def _page_index(t: int, p: int, z: int, c: int,
                numt: int, _: int, numz: int, numc: int) -> int:
    return c + numc * (z + numz * (t + numt * p))
