# nis2pyr

[![License](https://img.shields.io/pypi/l/nis2pyr.svg?color=green)](https://github.com/vibbits/nis2pyr/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/nis2pyr.svg?color=green)](https://pypi.org/project/nis2pyr)
[![Python Version](https://img.shields.io/pypi/pyversions/nis2pyr.svg?color=green)](https://python.org)
[![Test](https://github.com/vibbits/nis2pyr/actions/workflows/test.yml/badge.svg)](https://github.com/vibbits/nis2pyr/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/vibbits/nis2pyr/branch/main/graph/badge.svg?token=Q73CFI8FEH)](https://codecov.io/gh/vibbits/nis2pyr)

nis2pyr converts [Nikon](https://www.microscope.healthcare.nikon.com/products/software/nis-elements) .nd2 files to tiled pyramidal [OME](https://www.openmicroscopy.org/) TIFF files. The conversion is straightforward and can be performed via the `nis2pyr` command line tool, or via a simple one-liner in Python using the nis2pyr package. 

## System Requirements

nis2pyr was [tested](https://github.com/vibbits/nis2pyr/actions/workflows/test.yml) on these platforms:

- Windows 10
- Windows Server 2019
- Ubuntu 18.04
- Ubuntu 20.04
- macOS 10.15
- macOS 11

## Installation

Installation is straightforward:

```text
pip install nis2pyr
```

This installs the nis2pyr Python package which provides an easy to use function to convert ND2 files to OME TIFF. It also installs the `nis2pyr` program to convert ND2 files to OME TIFF from the command line.

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
               input_file_pattern [pyramid_filename]

Convert Nikon ND2 image files to tiled pyramidal OME TIFF files.

positional arguments:
  input_file_pattern    either the filename of a single ND2 file that needs to 
                        be converted, or a filename pattern ('glob') to convert 
                        multiple files. This filename pattern can be used for
                        example to convert all ND2 files in a given directory.
  pyramid_filename      if only a single filename is specified as input file 
                        pattern, pyramid_filename is the full filename of the
                        resulting pyramidal OME TIFF file; if no pyramid filename
                        is provided, or if multiple files are converted, the 
                        pyramidal OME TIFF(s) will be written to the same directory 
                        as the original ND2 and with the same filename but 
                        with an .ome.tif extension

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --compression COMPRESSION
                        the algorithm used for compressing the image data; currently
                        'zlib' is the only supported compression algorithm
                        (default: no compression)
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

- ND2 metadata is lost, except for pixel size and channel names and colors.
