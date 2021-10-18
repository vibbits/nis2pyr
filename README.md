# nis2pyr

[![License](https://img.shields.io/pypi/l/nis2pyr.svg?color=green)](https://github.com/vibbits/nis2pyr/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/nis2pyr.svg?color=green)](https://pypi.org/project/nis2pyr)
[![Python Version](https://img.shields.io/pypi/pyversions/nis2pyr.svg?color=green)](https://python.org)

The `nis2pyr` utility converts [Nikon](https://www.microscope.healthcare.nikon.com/products/software/nis-elements) .nd2 files to tiled pyramidal [OME](https://www.openmicroscopy.org/) TIFF files. These TIFF files can then be opened in [QuPath](https://qupath.github.io/) for interactive viewing.

## System Requirements

The instructions below assume Windows 10, but they should work with only minor changes on other platforms such as Linux.

## Installation

Installation is straightforward:

```text
pip install nis2pyr
```

This installs the nis2pyr Python package which provides a simple function to convert ND2 files to OME TIFF. It also installs the `nis2pyr` program to convert ND2 files to OME TIFF from the command line.

## Using nis2pyr in a Python program

Converting an ND2 file to pyramidal OME TIFF in Python is easy:

```python
from nis2pyr.convertor import convert_nd2_to_pyramidal_ome_tiff

convert_nd2_to_pyramidal_ome_tiff('original.nd2', 'pyramidal.ome.tif', compression='zlib')
```

The number of pyramid levels and the tile size can be specified as well (see the `convert_nd2_to_pyramidal_ome_tiff` docstring) but there is typically no need to do so.

## Running nis2pyr on the command line

To generate an uncompressed pyramidal file with the default options, run `nis2pyr` on the command line, specifying the .nd2 input image file and the name of the pyramidal OME TIFF to which it needs to be converted:

```text
nis2pyr input.nd2 pyramid.ome.tif
```

It is also possible to specify the compression algorithm, number of pyramid levels and the tile size of the output pyramidal OME TIFF.

```text
usage: nis2pyr [-h] [--version] [--compression COMPRESSION]
               [--pyramid-levels PYRAMID_LEVELS] [--tile-size TILE_SIZE]
               nd2_filename pyramid_filename

Convert Nikon .nd2 image files to tiled pyramidal OME TIFF files.

positional arguments:
  nd2_filename          full filename of the input ND2 file
  pyramid_filename      full filename of resulting pyramidal OME TIFF file; 
                        typically ends in .ome.tif

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --compression COMPRESSION
                        the algorithm used for compressing the image data; if this flag
                        is not specified the data will not be compressed; currently
                        'zlib' is the only useful algorithm, 'lzw' is not supported
  --pyramid-levels PYRAMID_LEVELS
                        the maximum number of resolution levels in the pyramidal OME TIFF,
                        including the full resolution image; successive pyramid
                        levels are downsampled by a factor 2
                        (default: 6)
  --tile-size TILE_SIZE
                        width in pixels of the tiles in the pyramidal OME TIFF;
                        the tiles are square; tile size must be a multiple of 16
                        (default: 256)
```

## Limitations

Known limitations of the current version of `nis2pyr`:

- ND2 files with [multiple z-planes](https://github.com/vibbits/nis2pyr/issues/1) are not supported.
- ND2 files with [multiple timepoints](https://github.com/vibbits/nis2pyr/issues/5) are not supported.
- ND2 metadata is lost, except for pixel size and channel names and colors.
