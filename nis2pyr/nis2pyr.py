import argparse
import nd2
import time
from writer import write_pyramidal_ome_tiff


VERSION = '0.4.0'


def _parse_args():
    parser = argparse.ArgumentParser(description="Convert Nikon ND2 image files to tiled pyramidal OME TIFF files.")
    parser.add_argument('--version', action='version', version=f'{VERSION}')
    parser.add_argument('--compression', type=str, default=None, help="the algorithm used for compressing the image data; if this flag is not specified the data will not be compressed; currently 'zlib' is the only useful algorithm, 'lzw' is not supported")
    parser.add_argument('--pyramid-levels', type=int, default=6, help='the maximum number of resolution levels in the pyramidal OME TIFF, including the full resolution image; successive pyramid levels are downsampled by a factor 2 (default: %(default)d)')
    parser.add_argument('--tile-size', type=int, default=256, help='width in pixels of the tiles in the pyramidal OME TIFF; the tiles are square; tile size must be a multiple of 16 (default: %(default)d)')
    parser.add_argument('nd2_filename', type=str, help="full filename of the input ND2 file")
    parser.add_argument('pyramid_filename', type=str, help="full filename of resulting pyramidal OME TIFF file; typically ends in .ome.tif")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    print(f'nis2pyr v{VERSION}')
    
    t1 = time.time()
    with nd2.ND2File(args.nd2_filename) as nd2file:
        write_pyramidal_ome_tiff(nd2file, 
                                args.pyramid_filename, 
                                compression=args.compression,
                                tile_size=args.tile_size,
                                max_levels=args.pyramid_levels)
    t2 = time.time()

    print(f'Conversion took {t2-t1:.1f} seconds.')
