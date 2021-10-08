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

In the source folder of the git repo, run `nis2pyr`, specifying the .nd2 input image file, and the name of the pyramidal OME TIFF to which it needs to be converted:

```
python nis2pyr.py input.nd2 pyramid.ome.tif
```
