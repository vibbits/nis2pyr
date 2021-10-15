import nd2
import numpy as np


def read_nd2file(nd2file: nd2.ND2File) -> np.ndarray:
    print(f'ND2 dimensions: {nd2file.sizes}; RGB: {nd2file.is_rgb}; datatype: {nd2file.dtype}')

    axes = ''.join(nd2file.sizes.keys())

    for unsupported_axis in ['T', 'Z']:
        if unsupported_axis in axes:
            raise ValueError(f'The ND2 file has a {unsupported_axis} dimension, but T and Z dimensions are not supported yet.')

    if (axes != 'YX') and (axes != 'YXS') and (axes != 'CYX'):
        raise ValueError(f'The ND2 file has axes {axes} but only YX, YXS and CYX are currently supported.')

    image = nd2file.asarray()

    if axes == 'YX':
        # We represent single plane grayscale images as a 3D numpy array too, 
        # just like RGB and multichannel images, so we insert a singleton dimension in the image.
        image = np.atleast_3d(image)
    elif axes == 'CYX':
        # We want the channel color to be the last dimension,
        # so we can pass the data easily to tifffile.
        image = image.transpose((1, 2, 0))

    # Reorder BGR channels to RGB
    if nd2file.is_rgb:
        print('Correcting RGB channel order')
        image = _reorder_rgb_channels(image)

    return image


def _reorder_rgb_channels(image: np.ndarray) -> np.ndarray:
    image[:,:,[0,2]] = image[:,:,[2,0]]
    return image
