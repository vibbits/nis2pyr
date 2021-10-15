import cv2
import imagecodecs  # for compressing the TIFF data stream
import math
import nd2
import numpy as np
import tifffile  # https://github.com/cgohlke/tifffile

from typing import Tuple, Optional

from metadata import get_nd2_channels_info, ome_set_channels_info
from reader import read_nd2file


def write_pyramidal_ome_tiff(nd2file: nd2.ND2File,
                             pyramid_filename: str,
                             compression: Optional[str], 
                             tile_size: int,
                             max_levels: int) -> None:
    """Convert an ND2 file to a tiled pyramidal OME TIFF file.

    Args:
        nd2file: The ND2 file that needs to be converted to pyramidal OME TIFF. 
        pyramid_filename: The filename of pyramidal OME TIFF file to write.
        compression: Compression algorithm used for compressing the TIFF data stream; 
          None means no compression; otherwise only 'zlib' is supported. 
        tile_size: The width in pixels of the (square) image tiles in the pyramid. Must be a multiple of 16.
        max_levels: The maximum number of pyramid levels to add to the pyramid, including 
          the full resolution original.
    """

    # Read ND2 file
    print(f'Reading {nd2file.path}')
    image = read_nd2file(nd2file)
        
    height, width, num_channels = image.shape

    # Figure out the number of pyramid levels we will need
    image_size: Tuple[int, int] = (width, height)
    num_levels: int = min(_num_pyramid_levels(image_size), max_levels)

    # OME XML atrributes.
    voxel_size_um = nd2file.voxel_size()
    ome_metadata = {'PhysicalSizeX': voxel_size_um.x, 'PhysicalSizeXUnit': 'µm',
                    'PhysicalSizeY': voxel_size_um.y, 'PhysicalSizeYUnit': 'µm'}

    photometric, planarconfig = _determine_storage_parameters(nd2file.is_rgb)
    reshape = _determine_reshape_function(nd2file.is_rgb)

    options = dict(tile=(tile_size, tile_size),
                   photometric=photometric, 
                   planarconfig=planarconfig,
                   compression=compression, 
                   metadata=ome_metadata)
                       
    # Write pyramidal file
    print(f'Saving pyramidal OME TIFF file {pyramid_filename}')
    with tifffile.TiffWriter(pyramid_filename, ome=True, bigtiff=True) as tif:
        # Write full resolution image
        print(f'Writing level 0: {_to_string(image.shape)}')
        tif.write(reshape(image), subifds=num_levels-1, **options)

        # Save downsampled pyramid images to the subifds
        for level in range(1, num_levels):
            image = np.atleast_3d(cv2.pyrDown(image))
            print(f'Writing level {level}: {_to_string(image.shape)}')
            tif.write(reshape(image), subfiletype=1, **options)

    # Update OME channel names and colors info.
    # This is not needed for RGB images, as they 
    # do not have named channels with custom colors.
    if not nd2file.is_rgb:
        print('Updating OME XML channel names and colors')
        channels_info = get_nd2_channels_info(nd2file)
        ome_set_channels_info(pyramid_filename, channels_info)


def _to_string(dims):
    return f'{dims[1]} x {dims[0]} x {dims[2]}'


def _determine_storage_parameters(is_rgb_image: bool):
    if is_rgb_image:
        photometric = 'rgb'
        planarconfig = None
    else:
        photometric = 'minisblack'
        planarconfig = 'separate'
    return photometric, planarconfig


def _determine_reshape_function(is_rgb_image: bool):
    if is_rgb_image:
        return lambda x: x  # identity function
    else:
        return _reshape_multiplane_image


def _reshape_multiplane_image(image: np.ndarray) -> np.ndarray:
    # Reshape image to be of shape (t=1, z=1, num_channels, 1, height, width)
    # This is needed because the precise shape influences how TiffWriter will store the channels,
    # and we want storage to be similar to what Bioformat's bfconvert produces
    # since it plays well with for example QuPath.
    height, width, num_channels = image.shape
    tmp = np.transpose(image, [2, 0, 1])   # move channel dimension to the front
    return np.reshape(tmp, (1, 1, num_channels, 1, height, width))  # add singleton dimensions


def _num_pyramid_levels(image_size: Tuple[int, int]) -> int:  
    x_levels = int(math.log2(image_size[0]))
    y_levels = int(math.log2(image_size[1]))
    return max(x_levels, y_levels)
