import math
import nd2
import numpy as np
import tifffile  # https://github.com/cgohlke/tifffile

from typing import Optional, Tuple

from nis2pyr.metadata import update_channels_info, get_ome_voxelsize
from nis2pyr.reader import read_nd2file


def write_pyramidal_ome_tiff(nd2file: nd2.ND2File,
                             pyramid_filename: str,
                             compression: Optional[str],
                             tile_size: int,
                             max_levels: int) -> None:
    """Convert an ND2 file to a tiled pyramidal OME TIFF file.

    Args:
        nd2file: The ND2 file that needs to be converted to pyramidal OME TIFF.
        pyramid_filename: The filename of pyramidal OME TIFF file to write.
        compression: Compression algorithm used for compressing the TIFF data
          stream; None means no compression; otherwise only 'zlib' is
          supported.
        tile_size: The width in pixels of the (square) image tiles in the
          pyramid. Must be a multiple of 16.
        max_levels: The maximum number of pyramid levels to add to the pyramid,
          including the full resolution original.
    """

    # Read ND2 file
    print(f'Reading {nd2file.path}')
    image = read_nd2file(nd2file)

    # The image MUST be of shape TPZC1YX (for non RGB) or TPZ1YXS (for RGB)
    assert len(image.shape) == 7

    is_rgb = nd2file.is_rgb
    if is_rgb:
        # image axes: TPZ1YXS
        _, num_positions, _, _, height, width, _ = image.shape
    else:
        # image axes: TPZC1YX
        _, num_positions, _, _, _, height, width = image.shape

    # Figure out the number of pyramid levels we will need
    image_size: Tuple[int, int] = (width, height)
    num_levels: int = min(_num_pyramid_levels(image_size), max_levels)

    ome_metadata = get_ome_voxelsize(nd2file)
    photometric, planarconfig = _determine_storage_parameters(is_rgb)

    options = dict(tile=(tile_size, tile_size),
                   photometric=photometric,
                   planarconfig=planarconfig,
                   compression=compression,
                   metadata=ome_metadata)

    _write_tiff_pyramid(image, pyramid_filename, num_positions, num_levels,
                        is_rgb, options)

    # Update OME channel names and colors info.
    # This is not needed for RGB images, as they
    # do not have named channels with custom colors.
    if not is_rgb:
        update_channels_info(nd2file, pyramid_filename, num_positions)


def _write_tiff_pyramid(image: np.ndarray,
                        pyramid_filename: str,
                        num_positions: int,
                        num_levels: int,
                        is_rgb: bool,
                        options) -> None:
    print(f'Saving pyramidal OME TIFF file {pyramid_filename}')
    with tifffile.TiffWriter(pyramid_filename, ome=True, bigtiff=True) as tif:
        for p in range(num_positions):
            # First extract the p-th position image. (ND2 files can have
            # images for multiple positions. OME TIFF does not have a specific
            # way to store these different positions, so they are simply
            # written to the TIFF file one after, as an image series.)
            img = image[:, p, :, :, :, :, :]

            if num_positions > 1:
                print(f'Position {p}')

            # Write full resolution image
            print(f'Writing level 0: {_to_string(img.shape, is_rgb)}')
            tif.write(img, subifds=num_levels-1, **options)

            # Save downsampled pyramid images to the subifds
            for level in range(1, num_levels):
                img = _downsample(img, is_rgb)
                print(f'Writing level {level}: {_to_string(img.shape, is_rgb)}')
                tif.write(img, subfiletype=1, **options)


def _to_string(dims, is_rgb: bool) -> str:
    assert len(dims) == 6
    if is_rgb:
        return f'TZ1YXS={dims}'
    else:
        return f'TZC1YX={dims}'


def _determine_storage_parameters(is_rgb_image: bool):
    if is_rgb_image:
        photometric = 'rgb'
        planarconfig = None
    else:
        photometric = 'minisblack'
        planarconfig = 'separate'
    return photometric, planarconfig


def _downsample(image: np.ndarray, is_rgb: bool) -> np.ndarray:
    # For now use numpy ::2 for (nearest neighbor) downsampling, but later
    # replace it with repeated cv2.pyrDown() for higher quality downsampling.
    # (pyrDown() cannot handle multiple z or t.)
    assert len(image.shape) == 6
    if is_rgb:
        # image is of shape TZ1YXS
        return image[:, :, :, ::2, ::2, :]
    else:
        # image is of shape TZC1YX
        return image[:, :, :, :, ::2, ::2]


def _num_pyramid_levels(image_size: Tuple[int, int]) -> int:
    x_levels = int(math.log2(image_size[0]))
    y_levels = int(math.log2(image_size[1]))
    return max(x_levels, y_levels)
