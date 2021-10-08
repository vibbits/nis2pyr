import argparse
import time
from reader import read_nd2
from writer import write_pyramidal_ome_tiff

# TODO: make environment.yaml / requirements.txt
# Development environment
# conda create -n nis python=3.8
# conda activate nis
# pip install pims_nd2
# pip install opencv-python
# pip install imagecodecs
# pip install tifffile
# pip install ome_types

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
#   showinf.abt pyramidal.ome.tif
#
# Inspecting OME XML atrributes in an OME TIFF file: 
#   tiffcomment.bat pyramidal.ome.tif
#

# TODO: use logger instead of hard-coded print statement
# TODO: provide command line flag with logging level

VERSION = '0.3.0'


def _parse_args():
    parser = argparse.ArgumentParser()
    # TODO: add info about what this tool does
    parser.add_argument('--version', action='version', version=f'{VERSION}')
    parser.add_argument('nd2_filename', type=str, help="full filename of the input ND2 file")
    parser.add_argument('pyramid_filename', type=str, help="full filename of resulting pyramidal OME TIFF file; typically ends in .ome.tif")
    # TODO: add tilesize
    # TODO: add pyramid levels
    # TODO: add compression
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    t1 = time.time()
    image, metadata = read_nd2(args.nd2_filename)
    write_pyramidal_ome_tiff(image, 
                             metadata, 
                             args.pyramid_filename, 
                             compression=None, 
                             max_levels=6)
    t2 = time.time()
    print(f'Image conversion took {t2-t1:.1f} seconds.')
