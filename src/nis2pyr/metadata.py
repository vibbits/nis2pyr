import ome_types
import tifffile
from typing import Any, Dict, List, Optional, Tuple
from nd2.nd2file import ND2File
from nd2.structures import Metadata


# Type alias
Rgb = Tuple[int, int, int]


def update_channels_info(nd2file: ND2File,
                         pyramid_filename: str,
                         num_positions: int) -> None:
    print('Updating OME XML channel names and colors')
    channels_info = get_nd2_channels_info(nd2file)
    if channels_info is not None:
        ome_set_channels_info(pyramid_filename,
                              num_positions, channels_info)
    else:
        print('Warning: legacy ND2 file. '
              'Could not extract channel names and colors!')


def ome_set_channels_info(ome_filename: str,
                          nd2_num_positions: int,
                          nd2_channels_info: List[Tuple[str, Rgb]]) -> None:
    # Read existing OME tags from TIFF file.
    ome_xml = tifffile.tiffcomment(ome_filename)
    ome = ome_types.from_xml(ome_xml)

    # Check if metadata is "compatible"
    nd2_num_channels = len(nd2_channels_info)
    ome_num_channels = len(ome.images[0].pixels.channels)

    if nd2_num_channels != ome_num_channels:
        print(f'Cannot update OME XML channel info due to a metadata '
              f'conflict: the OME XML has {ome_num_channels} channels but '
              f'the ND2 metadata has {nd2_num_channels}.')
        return

    # Update OME tags.
    # Note that ND2 files can hold images acquired at multiple positions,
    # but for identical channels. In the OME TIFFs that we write, these images
    # are simply stored one after another, but each of them has their own OME
    # XML information. So we need to duplicate the ND2 channel information in
    # the OME XML blob for each image.
    for p in range(nd2_num_positions):
        for i in range(nd2_num_channels):
            # Get channel name and color from original .nd2 file metadata.
            name, color = nd2_channels_info[i]

            # Update the OME channel name and color
            channel = ome.images[p].pixels.channels[i]
            channel.name = name
            channel.color = ome_types.model.simple_types.Color(color)
            ome.images[p].pixels.channels[i] = channel

    # Write back OME tags to the TIFF file.
    ome_xml = ome.to_xml()
    tifffile.tiffcomment(ome_filename, ome_xml)


def get_nd2_channels_info(nd2file: ND2File) -> Optional[List[Tuple[str, Rgb]]]:
    metadata = nd2file.metadata
    if isinstance(metadata, dict):
        # Legacy ND2 file, no (easy) way to extract the
        # channel names and colors.
        return None
    else:
        num_channels = metadata.contents.channelCount
        return [_get_channel_info(metadata, channel)
                for channel in range(num_channels)]


def _get_channel_info(nd2_metadata: Metadata,
                      channel_index: int) -> Tuple[str, Rgb]:
    channel = nd2_metadata.channels[channel_index].channel
    name = channel.name
    color = _parse_int_color(channel.colorRGB)
    return name, color


def _parse_int_color(color: int) -> Rgb:
    # color is an integer representation of the RGB color 0xBBGGRR
    _, b, g, r = [byte for byte in color.to_bytes(4, byteorder='big')]
    return r, g, b


def get_nd2_voxelsize_um(nd2file: ND2File) -> Tuple[Optional[float],
                                                    Optional[float],
                                                    Optional[float]]:
    voxel_size_um = nd2file.voxel_size()

    nd2_metadata = nd2file.metadata
    if isinstance(nd2_metadata, dict):
        # Legacy file format. There does not seem to be info on whether
        # the axes are 'calibrated', so assume they are.
        calibrated = (True, True, True)
    else:
        calibrated = nd2_metadata.channels[0].volume.axesCalibrated

    has_z = 'Z' in nd2file.sizes  # does the ND2 file have Z-slices?

    size_x = voxel_size_um.x if calibrated[0] else None
    size_y = voxel_size_um.y if calibrated[1] else None
    size_z = voxel_size_um.z if calibrated[2] and has_z else None
    return size_x, size_y, size_z


def get_ome_voxelsize(nd2file: ND2File) -> Dict[str, Any]:
    voxel_size_um = get_nd2_voxelsize_um(nd2file)

    ome_metadata = {}
    if voxel_size_um[0]:
        ome_metadata['PhysicalSizeX'] = voxel_size_um[0]
        ome_metadata['PhysicalSizeXUnit'] = 'µm'

    if voxel_size_um[1]:
        ome_metadata['PhysicalSizeY'] = voxel_size_um[1]
        ome_metadata['PhysicalSizeYUnit'] = 'µm'

    if voxel_size_um[2]:
        ome_metadata['PhysicalSizeZ'] = voxel_size_um[2]
        ome_metadata['PhysicalSizeZUnit'] = 'µm'

    return ome_metadata
