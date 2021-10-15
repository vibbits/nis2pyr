# nis2pyr

[![License](https://img.shields.io/pypi/l/nis2pyr.svg?color=green)](https://github.com/vibbits/nis2pyr/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/nis2pyr.svg?color=green)](https://pypi.org/project/nis2pyr)
[![Python Version](https://img.shields.io/pypi/pyversions/nis2pyr.svg?color=green)](https://python.org)

The `nis2pyr` utility converts [Nikon](https://www.microscope.healthcare.nikon.com/products/software/nis-elements) .nd2 files to tiled pyramidal [OME](https://www.openmicroscopy.org/) TIFF files. These TIFF files can then be opened in [QuPath](https://qupath.github.io/) for interactive viewing.

## System requirements

The instructions below assume Windows 10, but they should work with only minor changes on other platforms such as Linux.

## Setting up a development environment

First get the source code:

```text
git clone https://github.com/vibbits/nis2pyr.git
```

Then create a Conda environment:

```text
conda env create -f environment.yml
conda activate nis2pyr
```

## Packaging nis2pyr

### Packaging into a stand-alone directory

The `nis2pyr.py` program requires a Python environment to execute. This complicates deploying it on non-development machines where Python is not installed. It is however possible to bundle `nis2pyr.py` with all its dependencies and a Python interpreter into a stand-alone directory, which contains a `nis2pyr.exe` executable that runs the program. This can be accomplished with [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/index.html). 

First install pyinstaller:

```text
pip install pyinstaller
```

Then `cd` into the directory which contains the `nis2pyr.py` file and run pyinstaller:

```text
pyinstaller --collect-all pims_nd2 --collect-all ome_types --collect-all xmlschema nis2pyr.py
```

The `--collect-all` options are needed to give `pyinstaller` a hand finding modules needed by nis2pyr.

The dist\nis2pyr directory is now self-contained and holds a `nis2pyr.exe` which can be executed on the command line outside a Python development environment.

### Packaging into a stand-alone executable

Instead of bundling nis2pyr in a directory containing the executable as well as all its dependencies, it is also possible to bundle everything in a single executable which is basically a self-extracting archive holding the same files. This is done by passing the `--onefile` option to `pyinstaller`:

```text
pyinstaller --onefile --collect-all pims_nd2 --collect-all ome_types --collect-all xmlschema nis2pyr.py
```

The resulting single file `nis2pyr.exe` is now even easier to deploy. However, starting it will be a bit slower because behind the scenes its contents are first unpacked into a temporary folder every time nis2pyr is run.

## Running nis2pyr

To generate an uncompressed pyramidal file with the default options, run `nis2pyr.exe` specifying the .nd2 input image file, and the name of the pyramidal OME TIFF to which it needs to be converted:

```text
nis2pyr.exe input.nd2 pyramid.ome.tif
```

It is also possible to specify the compression algorithm, number of pyramid levels and the tile size of the output pyramidal OME TIFF.

```text
usage: nis2pyr [-h] [--version] [--compression COMPRESSION] [--pyramid-levels PYRAMID_LEVELS] [--tile-size TILE_SIZE] nd2_filename pyramid_filename

Convert Nikon .nd2 image files to tiled pyramidal OME TIFF files.

positional arguments:
  nd2_filename          full filename of the input ND2 file
  pyramid_filename      full filename of resulting pyramidal OME TIFF file; typically ends in .ome.tif

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --compression COMPRESSION
                        the algorithm used for compressing the image data; if this flag is not specified the data will not be compressed; currently
                        'zlib' is the only useful algorithm, 'lzw' is not supported
  --pyramid-levels PYRAMID_LEVELS
                        the maximum number of resolution levels in the pyramidal OME TIFF, including the full resolution image; successive pyramid
                        levels are downsampled by a factor 2 (default: 6)
  --tile-size TILE_SIZE
                        width in pixels of the tiles in the pyramidal OME TIFF; the tiles are square; tile size must be a multiple of 16 (default: 256)
```

## Limitations

Known limitations of the current version of `nis2py`:

- ND2 files with multiple z-planes are not supported.
- ND2 files with multiple timepoints are not supported.
- ND2 metadata is lost, except for pixel size and channel names and colors.
