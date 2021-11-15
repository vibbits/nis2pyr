import nd2
import numpy as np
from typing import Tuple


def read_nd2file(nd2file: nd2.ND2File) -> np.ndarray:
    print(f'ND2 dimensions: {nd2file.sizes}; RGB: {nd2file.is_rgb}; '
          f'datatype: {nd2file.dtype}; legacy: {nd2file.is_legacy}')

    axes = ''.join(nd2file.sizes.keys())

    image = nd2file.asarray()

    # Reshape image to be of shape (num t, num p, num z, num channels, height, width, num components).
    # (For non-RGB num components is 1; for RGB num channels is 1 and num components is 3.)
    # This is needed because the precise shape influences how TiffWriter (in writer.py) will
    # store the channels, and we want storage to be similar to what Bioformat's
    # bfconvert produces since that format plays well with for example QuPath.
    return _reshape_to_7d(image, axes, nd2file.is_rgb, nd2file.is_legacy)


def _determine_7d_dimensions(image: np.ndarray, axes: str) -> Tuple[int, int,
                                                                    int, int,
                                                                    int, int,
                                                                    int]:

    dims = [1, 1, 1, 1, 0, 0, 1]  # default values for [t, p, z, c, y, x, s]
    dim_names = 'TPZCYXS'

    # image.shape[i] is the dimension of the image along the axis
    # with name axes[i]. We find the corresponding dimension position
    # j in dims which corresponds to the same axis, and overwrite the
    # default dimension value with the actual value from image.shape[i].
    for i, axis_name in enumerate(axes):
        j = dim_names.find(axis_name)
        if j >= 0:
            dims[j] = image.shape[i]
        else:
            raise ValueError(f'The image has an unsupported axis {axis_name}.')

    return tuple(dims)


def _reshape_to_7d(image: np.ndarray,
                   axes: str,
                   is_rgb: bool,
                   is_legacy: bool) -> np.ndarray:

    t, p, z, c, y, x, s = _determine_7d_dimensions(image, axes)

    if (s > 1) and (s != 3):   # Possible in practice?
        raise ValueError(f'The ND2 file has S={s}. '
                         f'This is not supported.')

    if (s > 1) and (c > 1):    # Possible in practice?
        raise ValueError(f'The ND2 file has S={s} and C={c}. '
                         f'This is not supported.')

    image = image.reshape(t, p, z, c, y, x, s)

    if is_rgb and not is_legacy:
        # Old ND2 RGB files (which use JPEG2000) have channels stored
        # in R, G, B order and do not need changing. Newer ND2 RGB files
        # however store RGB color values in B, G, R order. For those files
        # we swap the R and B channels so they are also interpreted
        # correctly as RGB.
        print('Swapping RGB channels')
        image = _reorder_bgr_channels_to_rgb(image)

    return image


def _reorder_bgr_channels_to_rgb(image: np.ndarray) -> np.ndarray:
    assert len(image.shape) == 7  # TPZCYXS
    assert image.shape[3] == 1  # 1 channel (RGB)
    assert image.shape[6] == 3  # 3 samples (R, G and B)
    image[:, :, :, :, :, :, [0, 2]] = image[:, :, :, :, :, :, [2, 0]]
    return image
