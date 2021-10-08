import cv2          # OpenCV for building the image pyramid
import imagecodecs  # for compressing the TIFF data stream
import math
import tifffile     # https://github.com/cgohlke/tifffile
import ome_types
import numpy as np
import pydantic.color
from typing import Tuple, Optional
from reader import is_rgb_image


def write_pyramidal_ome_tiff(image,     # TODO add type
                             nd2_metadata,  # TODO add type
                             pyramid_filename: str,
                             compression: Optional[str]='zlib',  # TODO: check which compression is used by bioformats bfconvert; is it reported by tiffcomment/showinfo? Is zlib the LZW of bfconvert?
                             tile_size: int=256,
                             max_levels: int=6) -> None:
    """xxxx

    Args:
        input_filename: The filename of the RGB original TIFF image that needs to be converted 
          to pyramidal TIFF file.
        pyramid_filename: The filename of pyramidal TIFF file to write.
        compression: None means no compression; otherwise stick to using 'zlib'. 
        tile_size: The width in pixels of the (square) image tiles in the pyramid. Must be a multiple of 16.
        max_levels: The maximum number of pyramid levels to add to the pyramid, including 
          the full resolution original.

    Returns:
        xxxx
    """

    height, width, num_channels = image.shape
    print(f'_write_pyramidal_ome_tiff: image.shape={image.shape} height={height} width={width} num_channels={num_channels} dtype={image.dtype}')

    # Figure out the number of pyramid levels we will need
    image_size: Tuple[int, int] = (width, height)
    num_levels: int = min(_num_pyramid_levels(image_size), max_levels)

    # OME XML atrributes.
    pixel_size_um = nd2_metadata['calibration_um']
    ome_metadata = {'PhysicalSizeX': pixel_size_um, 'PhysicalSizeXUnit': 'µm',
                    'PhysicalSizeY': pixel_size_um, 'PhysicalSizeYUnit': 'µm'}

    photometric, planarconfig = _determine_storage_parameters(nd2_metadata)
    reshape = _determine_reshape_function(nd2_metadata)

    options = dict(tile=(tile_size, tile_size),
                   photometric=photometric, 
                   planarconfig=planarconfig,
                   compression=compression, 
                   metadata=ome_metadata)
                       
    # Write pyramidal file
    print(f'Saving {pyramid_filename} as pyramidal OME TIFF file')
    with tifffile.TiffWriter(pyramid_filename, ome=True, bigtiff=True) as tif:
        # Write full resolution image
        print(f'Writing level 0: {image.shape}')
        tif.write(reshape(image), subifds=num_levels-1, **options)

        # Save downsampled pyramid images to the subifds
        for level in range(1, num_levels):
            image = np.atleast_3d(cv2.pyrDown(image))
            print(f'Writing level {level}: {image.shape}')
            tif.write(reshape(image), subfiletype=1, **options)

    # Update OME channel names and colors info
    _update_ome_channel_info(pyramid_filename, nd2_metadata)


def _determine_storage_parameters(nd2_metadata):
    is_rgb: bool = is_rgb_image(nd2_metadata)
    if is_rgb:
        photometric = 'rgb'
        planarconfig = None
    else:
        photometric = 'minisblack'
        planarconfig = 'separate'
    return photometric, planarconfig


def _determine_reshape_function(nd2_metadata):
    if is_rgb_image(nd2_metadata):
        return lambda x: x  # identity function
    else:
        return _reshape_multiplane_image


def _reshape_multiplane_image(image):
    # Reshape image to be of shape (t=1, z=1, num_channels, 1, height, width)
    # This is needed because the precise shape influences how TiffWriter will store the channels,
    # and we want storage to be similar to what Bioformat's bfconvert produces
    # since it plays well with for example QuPath.
    height, width, num_channels = image.shape
    tmp = np.transpose(image, [2, 0, 1])   # move channel dimension to the front
    return np.reshape(tmp, (1, 1, num_channels, 1, height, width))  # add singleton dimensions


def _update_ome_channel_info(pyramid_filename, nd2_metadata):
    # No tags changes are needed for RGB images:
    # they do not have channel names and colors that need updating.
    if is_rgb_image(nd2_metadata):
        return 

    print('Updating OME XML channel names and colors')

    # Read existing OME tags from TIFF file.
    ome_xml = tifffile.tiffcomment(pyramid_filename)
    ome = ome_types.from_xml(ome_xml)

    # Update tags.
    num_channels = len(ome.images[0].pixels.channels)
    for i in range(num_channels):
        # Get channel name and color from original .nd2 file metadata.
        name, rgb = _get_plane_info(nd2_metadata, i)

        # Update the OME channel name and color
        channel = ome.images[0].pixels.channels[i]
        channel.name = name
        channel.color = pydantic.color.Color((int(rgb[0]*255.0), int(rgb[1]*255.0), int(rgb[2]*255.0)))
        ome.images[0].pixels.channels[i] = channel
    
    # Write back OME tags to the TIFF file.
    ome_xml = ome.to_xml()
    tifffile.tiffcomment(pyramid_filename, ome_xml)


def _get_plane_info(nd2_metadata, plane_index):   
    # TODO: make more robust in case info is not present?
    key = f'plane_{plane_index}'
    plane_info = nd2_metadata[key]
    return plane_info['name'], plane_info['rgb_value']


def _num_pyramid_levels(image_size: Tuple[int, int]) -> int:
    """xxxx

    Args:
        image_size: The (width, height) of the image for which we want to determine 
          the number of pyramid levels to calculate.

    Returns:
        xxxx
    """    
    x_levels = int(math.log2(image_size[0]))
    y_levels = int(math.log2(image_size[1]))
    return max(x_levels, y_levels)
