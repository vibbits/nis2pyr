from pims import ND2Reader_SDK
import numpy as np

def read_nd2(nd2_input_filename: str):  # TODO return type
    print(f'Reading {nd2_input_filename} with ND2Reader_SDK')
    with ND2Reader_SDK(nd2_input_filename) as frames:
        metadata = frames.metadata
        print('ND2 file: #frames={}, #components={}, #planes={}, bits per component={}, is RGB={}, pixel size={} um, frames.sizes={}'
              .format(len(frames), 
                      metadata['components'], 
                      metadata['plane_count'],
                      metadata['bitsize_memory'],
                      is_rgb_image(metadata),
                      metadata['calibration_um'],
                      frames.sizes))

        # TODO: check that len(frames) == 1; raise otherwise
        # TODO: for frames.sizes we only expect 'x', 'y' and optionally 'c' as entries here (so no 'z' or 't' or something) - CHECK THIS AND ERROR OUT OTHERWISE
        axes = None
        if ('x' in frames.sizes) and ('y' in frames.sizes):
            if 'c' in frames.sizes:
                axes = 'yxc'
            else:
                axes = 'yx'
        # TODO: raise if axes is None

        # The nd2 reader seems to have issues with some types of .nd2 images, 
        # try to warn the user of potentially incorrect output.
        _warn_for_potential_problems(frames, metadata)

        # Extract image data
        print('Reading image')
        frames.bundle_axes = axes
        image = frames[0]

        # Insert a singleton dimension if needed. This is so we represent single plane
        # grayscale images as a 3D numpy array too, just like RGB and multichannel images.
        image = np.atleast_3d(image)

        # Apparenty the channels in the "RGB" images are in BGR order instead of RGB,
        # so we reorder them here.
        if is_rgb_image(metadata):
            image = _reorder_rgb_channels(image)

        # REMOVE - FOR TESTING ONLY
        # print('=======> IMAGE CROPPED <======')
        # image = image[4096:4096+512,4096:4096+1024,:]

        return image, metadata


def _reorder_rgb_channels(image):
    # Testfile: "g:\NISMakePyramidal\Testfiles\BF\RGB-8bit\B-1981946 1-1.2.nd2"
    # (Visualization in QuPath 0.3.0 and NIS Viewer 5.21.00)
    print('Correcting RGB channel order')
    image[:,:,[0,2]] = image[:,:,[2,0]]
    return image


def _warn_for_potential_problems(frames, metadata) -> None:
    width_in_pixels = frames.sizes['x']
    num_components = metadata['components']
    bits_per_component = metadata['bitsize_memory']
    width_bytes = metadata['width_bytes']
    tile_height = metadata['tile_height']
    warned = False

    if width_bytes != width_in_pixels * num_components * bits_per_component / 8: 
        print('WARNING: padding suspected; nd2 reader potentially does not handle this correctly')
        warned = True

    if tile_height != 1:
        print(f'WARNING: tile height is {tile_height} instead of 1; nd2 reader potentially does not handle this correctly')
        warned = True

    if warned:
        print(metadata)


def is_rgb_image(nd2_metadata) -> bool:
    num_components = nd2_metadata['components']
    num_planes = nd2_metadata['plane_count']

    # For the ND2 files that we inspected:
    # RGB images have plane_count=1 and components=3;
    # multi-channel files have plane_count=components (=5 for example)
    return (num_planes == 1) and (num_components == 3)