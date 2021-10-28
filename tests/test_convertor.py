import os
from pathlib import Path
from tifffile import TiffFile, TIFF
from nis2pyr.convertor import convert_nd2_to_pyramidal_ome_tiff
from conftest import TRUTH


DEFAULT_TILE_SIZE = 256
DEFAULT_PYRAMID_LEVELS = 6


# Conversion of n-dimensional image coordinates to the OME TIFF page number.
# This is still tentative and needs more extensive testing.
def page_index(t: int, p: int, z: int, c: int,
               numt: int, _: int, numz: int, numc: int) -> int:
    return c + numc * (z + numz * (t + numt * p))


def test_convert(input_dir, output_dir, any_nd2):
    filename = any_nd2
    nd2_filename = os.path.join(input_dir, filename)
    pyramid_filename = os.path.join(output_dir,
                                    os.path.basename(Path(nd2_filename)
                                                     .with_suffix('.ome.tif')))

    # Convert the ND2 to OME TIFF
    convert_nd2_to_pyramidal_ome_tiff(nd2_filename,
                                      pyramid_filename,
                                      compression='zlib')

    assert os.path.exists(pyramid_filename)

    # Read the OME TIFF and check that it is structured as expected,
    # and also that a set of test pixels have the correct values.

    tif_truth = TRUTH[filename]['tiff']
    nd2_truth = TRUTH[filename]['nd2']

    with TiffFile(pyramid_filename) as tif:
        assert tif.is_ome
        assert tif.is_bigtiff

        assert len(tif.pages) == tif_truth['pages']        
        for page in tif.pages:
            assert page.tilewidth == DEFAULT_TILE_SIZE
            assert page.tilelength == DEFAULT_TILE_SIZE
            assert page.compression == TIFF.COMPRESSION.ADOBE_DEFLATE
            assert page.photometric == tif_truth['photometric']

        assert len(tif.series) == tif_truth['series']
        for series in tif.series:
            assert series.is_pyramidal
            assert len(series.levels) == DEFAULT_PYRAMID_LEVELS

        # For now the test code below only supports non-RGB images
        assert not nd2_truth['is_rgb']

        # Check pixel values
        numt, nump, numz, numc, _, _, _ = nd2_truth['shape']
        for coords, intensity in nd2_truth['pixels']:
            t, p, z, c, _, y, x = coords
            idx = page_index(t, p, z, c, numt, nump, numz, numc)
            image = tif.pages[idx].asarray()
            assert image[y, x] == intensity
