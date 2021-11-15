import math
import nd2
import numpy as np
import tifffile  # https://github.com/cgohlke/tifffile

from typing import Optional, Tuple

from nis2pyr.metadata import update_channels_info, get_ome_voxelsize
from nis2pyr.reader import read_nd2file
from nis2pyr import __version__


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

    # The image MUST be of shape TPZCYXS (for both RGB and non-RGB)
    assert len(image.shape) == 7
    _, num_positions, _, _, height, width, _ = image.shape

    is_rgb = nd2file.is_rgb

    # Figure out the number of pyramid levels we will need
    image_size: Tuple[int, int] = (width, height)
    num_levels: int = min(_num_pyramid_levels(image_size), max_levels)

    # Collect OME metadata
    ome_metadata = {}
    ome_metadata['Creator'] = _creator()
    ome_metadata.update(get_ome_voxelsize(nd2file))

    photometric, planarconfig = _determine_storage_parameters(is_rgb)

    options = dict(tile=(tile_size, tile_size),
                   photometric=photometric,
                   planarconfig=planarconfig,
                   compression=compression,
                   metadata=ome_metadata,
                   software=_creator())

    _write_tiff_pyramid(image, pyramid_filename, num_positions, num_levels,
                        options)

    # Update OME channel names and colors info.
    # This is not needed for RGB images, as they
    # do not have named channels with custom colors.
    if not is_rgb:
        update_channels_info(nd2file, pyramid_filename, num_positions)


def _write_tiff_pyramid(image: np.ndarray,
                        pyramid_filename: str,
                        num_positions: int,
                        num_levels: int,
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
            print(f'Writing level 0: {_to_string(img.shape)}')
            tif.write(img, subifds=num_levels-1, **options)

            # Save downsampled pyramid images to the subifds
            for level in range(1, num_levels):
                img = _downsample(img)
                print(f'Writing level {level}: {_to_string(img.shape)}')
                tif.write(img, subfiletype=1, **options)


def _creator() -> str:
    return f'nis2pyr v{__version__}'


def _to_string(dims) -> str:
    assert len(dims) == 6
    return f'TZCYXS={dims}'


def _determine_storage_parameters(is_rgb_image: bool):
    if is_rgb_image:
        photometric = 'rgb'
        planarconfig = None
    else:
        photometric = 'minisblack'
        planarconfig = 'contig'
    return photometric, planarconfig


def _downsample(image: np.ndarray) -> np.ndarray:
    # For now use numpy ::2 for (nearest neighbor) downsampling, but later
    # replace it with repeated cv2.pyrDown() for higher quality downsampling.
    # (pyrDown() cannot handle multiple z or t though)
    assert len(image.shape) == 6
    # image is of shape TZCYXS
    return image[:, :, :, ::2, ::2, :]


def _num_pyramid_levels(image_size: Tuple[int, int]) -> int:
    x_levels = int(math.log2(image_size[0]))
    y_levels = int(math.log2(image_size[1]))
    return max(x_levels, y_levels)
