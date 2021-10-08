import argparse
import time
from reader import read_nd2
from writer import write_pyramidal_ome_tiff


# Inspecting the original .nd2 files:
#   NIS-Elements Viewer
#   https://www.microscope.healthcare.nikon.com/en_EU/products/software/nis-elements/viewer
#
# The Bioformats command line tools (bfconvert, showinf, tiffcomment) are very useful.
#   https://www.openmicroscopy.org/bio-formats/downloads/
#
# Converting .nd2 to pyramidal OME TIFF with bfconvert:
#   set BF_MAX_MEM=4g
#   bfconvert.bat -no-upgrade -bigtiff -pyramid-scale 2 -pyramid-resolutions 6 -noflat -tilex 256 -tiley 256 foo.nd2 pyramidal.ome.tif
#
# Inspecting the OME TIFF file:
#   showinf.bat pyramidal.ome.tif
#
# Inspecting OME XML atrributes in an OME TIFF file: 
#   tiffcomment.bat pyramidal.ome.tif
#

# TODO: use logger instead of hard-coded print statements
# TODO: provide command line flag with logging level

VERSION = '0.3.2'


def _parse_args():
    parser = argparse.ArgumentParser(description="Convert Nikon .nd2 image files to tiled pyramidal OME TIFF files.")
    parser.add_argument('--version', action='version', version=f'{VERSION}')
    parser.add_argument('nd2_filename', type=str, help="full filename of the input ND2 file")
    parser.add_argument('pyramid_filename', type=str, help="full filename of resulting pyramidal OME TIFF file; typically ends in .ome.tif")
    parser.add_argument('--tile-size', type=int, default=256, help='width in pixels of the tiles in the pyramidal OME TIFF; the tiles are square; tile size must be a multiple of 16')
    parser.add_argument('--pyramid-levels', type=int, default=6, help='the maximum number of resolution levels in the pyramidal OME TIFF, including the full resolution image; subsequent pyramid levels are downsampled by a factor 2')
    # TODO: add compression
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    print(args)
    t1 = time.time()
    image, metadata = read_nd2(args.nd2_filename)
    write_pyramidal_ome_tiff(image, 
                             metadata, 
                             args.pyramid_filename, 
                             compression='None',
                             tile_size=args.tile_size,
                             max_levels=args.pyramid_levels)
    t2 = time.time()
    print(f'Image conversion took {t2-t1:.1f} seconds.')
