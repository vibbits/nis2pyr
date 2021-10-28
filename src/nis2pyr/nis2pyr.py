import argparse
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
        'nd2_filename',
        type=str,
        help="full filename of the input ND2 file")

    parser.add_argument(
        'pyramid_filename',
        type=str,
        nargs='?',
        help="full filename of the resulting pyramidal OME TIFF file; "
             "if no pyramid filename is provided the pyramidal OME TIFF will "
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

    # The pyramid filename is optional. Determine a reasonable default
    # filename if it's missing.
    pyramid_filename = _get_pyramid_filename(args.nd2_filename,
                                             args.pyramid_filename)

    t1 = time.time()
    convert_nd2_to_pyramidal_ome_tiff(args.nd2_filename,
                                      pyramid_filename,
                                      args.compression,
                                      args.tile_size,
                                      args.pyramid_levels)
    t2 = time.time()
    print(f'Conversion took {t2-t1:.1f} seconds.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
