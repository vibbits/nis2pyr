import ome_types
import tifffile
import pydantic.color
from typing import List, Tuple
from nd2.nd2file import ND2File
from nd2.structures import Metadata


# Type alias
Rgb = Tuple[int, int, int]


def ome_set_channels_info(ome_filename: str,
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
    for i in range(nd2_num_channels):
        # Get channel name and color from original .nd2 file metadata.
        name, color = nd2_channels_info[i]

        # Update the OME channel name and color
        channel = ome.images[0].pixels.channels[i]
        channel.name = name
        channel.color = pydantic.color.Color(color)
        ome.images[0].pixels.channels[i] = channel

    # Write back OME tags to the TIFF file.
    ome_xml = ome.to_xml()
    tifffile.tiffcomment(ome_filename, ome_xml)


def get_nd2_channels_info(nd2file: ND2File) -> List[Tuple[str, Rgb]]:
    metadata = nd2file.metadata
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
