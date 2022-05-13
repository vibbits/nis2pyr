import argparse
import glob
import os
import sys
import time
from pathlib import Path
from typing import Optional
from nis2pyr.convertor import convert_nd2_to_pyramidal_ome_tiff
from nis2pyr import __version__


def _parse_args():
    parser = argparse.ArgumentParser(
        prog='nis2pyr',
        description="Convert Nikon ND2 image files to tiled pyramidal "
                    "OME TIFF files.")

    parser.add_argument(
        '--version',
        action='version',
        version=f'{__version__}')

    parser.add_argument(
        '--compression',
        type=str,
        default=None,
        help="the algorithm used for compressing the image data; currently "
             "'zlib' is the only supported compression algorithm "
             "(default: no compression)")

    parser.add_argument(
        '--pyramid-levels',
        type=int,
        default=6,
        help='the maximum number of resolution levels in the pyramidal '
             'OME TIFF, including the full resolution image; successive '
             'pyramid levels are downsampled by a factor 2 '
             '(default: %(default)d)')

    parser.add_argument(
        '--tile-size',
        type=int,
        default=256,
        help='width in pixels of the tiles in the pyramidal OME TIFF; '
             'the tiles are square; tile size must be a multiple of 16 '
             '(default: %(default)d)')

    parser.add_argument(
        'input_file_pattern',
        type=str,
        help="either the filename of a single ND2 file that needs to be "
             "converted, or a filename pattern ('glob') to convert multiple "
             "files. This filename pattern can be used for example to convert "
             "all ND2 files in a given directory.")

    parser.add_argument(
        'pyramid_filename',
        type=str,
        nargs='?',
        help="if only a single filename is specified as input file pattern, "
             "pyramid_filename is the full filename of the resulting "
             "pyramidal OME TIFF file; if no pyramid filename is provided, or "
             "if multiple files are converted, the pyramidal OME TIFF(s) will "
             "be written to the same directory as the original ND2 and with "
             "the same filename but with an .ome.tif extension")

    return parser.parse_args()


def _get_pyramid_filename(nd2_filename: str,
                          pyramid_filename: Optional[str]) -> str:
    if pyramid_filename is not None:
        return pyramid_filename
    else:
        # If we have no pyramid filename, then we use the same directory
        # and the same filename of the ND2 file, but with .ome.tiff
        # as extension instead of .nd2.
        dirname = os.path.dirname(nd2_filename)
        filename = os.path.basename(Path(nd2_filename).with_suffix('.ome.tif'))
        return os.path.join(dirname, filename)


def main() -> int:
    args = _parse_args()

    print(f'nis2pyr v{__version__}')

    # Figure out which files to convert, and what output filename to use.
    if os.path.isfile(args.input_file_pattern):
        nd2_filenames = [args.input_file_pattern]
        suggested_pyramid_filename = args.pyramid_filename
    else:
        pattern = args.input_file_pattern
        if os.path.isdir(pattern):
            pattern = os.path.join(pattern, '*.nd2')
        nd2_filenames = glob.glob(pattern)
        suggested_pyramid_filename = None

    if len(nd2_filenames) > 1 and args.pyramid_filename is not None:
        print(f'Warning: the specified output filename '
              f'{args.pyramid_filename} is ignored because multiple ND2 files '
              f'were specified for conversion.')

    # Convert the files one by one to pyramidal OME TIFF.
    for nd2_filename in nd2_filenames:
        t1 = time.time()
        pyramid_filename = _get_pyramid_filename(nd2_filename,
                                                 suggested_pyramid_filename)
        convert_nd2_to_pyramidal_ome_tiff(nd2_filename,
                                          pyramid_filename,
                                          args.compression,
                                          args.tile_size,
                                          args.pyramid_levels)
        t2 = time.time()
        print(f'Converting {nd2_filename} took {t2-t1:.1f} seconds.')

    return 0


if __name__ == '__main__':
    sys.exit(main())
