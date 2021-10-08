# nis2pyr

The `nis2pyr` utility converts [Nikon](https://www.microscope.healthcare.nikon.com/products/software/nis-elements) .nd2 files to tiled pyramidal [OME](https://www.openmicroscopy.org/) TIFF files. These TIFF files can then be opened in [QuPath](https://qupath.github.io/) for interactive viewing.

## Setting up a development environment

First get the source code:
```
git clone https://github.com/vibbits/nis2pyr.git
```

Then create a Conda environment:
```
conda env create -f environment.yml
conda activate nis2pyr
```

## Running nis2pyr

To generate an uncompressed pyramidal file with the default options, first move to the source folder of your cloned nis2pyr git repo. Then run `nis2pyr`, specifying the .nd2 input image file, and the name of the pyramidal OME TIFF to which it needs to be converted:

```
python nis2pyr.py input.nd2 pyramid.ome.tif
```

It is also possible to specify the compression algorithm, number of pyramid levels and the tile size of the output pyramidal OME TIFF.

```
usage: nis2pyr.py [-h] [--version] [--compression COMPRESSION] [--pyramid-levels PYRAMID_LEVELS] [--tile-size TILE_SIZE] nd2_filename pyramid_filename

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