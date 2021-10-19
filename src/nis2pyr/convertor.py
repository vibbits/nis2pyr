import nd2
from typing import Optional
from nis2pyr.writer import write_pyramidal_ome_tiff


def convert_nd2_to_pyramidal_ome_tiff(nd2_filename: str,
                                      pyramid_filename: str,
                                      compression: Optional[str] = None,
                                      tile_size: int = 256,
                                      max_levels: int = 6) -> None:
    """Convert an ND2 file to a tiled pyramidal OME TIFF file.

    Args:
        nd2file: The filename of the ND2 file that needs to be converted to
          pyramidal OME TIFF.
        pyramid_filename: The filename of pyramidal OME TIFF file to write.
        compression: Compression algorithm used for compressing the TIFF data
          stream; None means no compression; otherwise only 'zlib' is
          supported.
        tile_size: The width in pixels of the (square) image tiles in the
          pyramid. Must be a multiple of 16.
        max_levels: The maximum number of pyramid levels to add to the pyramid,
        including the full resolution original.
    """
    with nd2.ND2File(nd2_filename) as nd2file:
        write_pyramidal_ome_tiff(nd2file,
                                 pyramid_filename,
                                 compression,
                                 tile_size,
                                 max_levels)
