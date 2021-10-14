# Useful ND2 and OME TIFF tools

## ND2 SDK

Nikon's official [ND2SDK](https://www.nd2sdk.com/).

## NIS-Elements Viewer

The [NIS-Elements Viewer](https://www.microscope.healthcare.nikon.com/en_EU/products/software/nis-elements/viewer) is a baseline ND2 file viewer. It can serve as a reference for visual inspection of ND2 test files.

## ND2 to OME-TIFF Converter

An ND2 to OME-TIFF Converter application can be downloaded from the Nikon [ND2SDK](https://www.nd2sdk.com/) website. The current version (NIS_ND2ToOMETIFFConverter_Setup_5.40.00_1611.exe) does not create *pyramidal* OME TIFF files however.

## Bioformats

The [Bioformats](https://www.openmicroscopy.org/bio-formats/downloads/) command line tools (bfconvert, showinf, tiffcomment) are useful for inspecting OME TIFF file structure and metadata, and as a baseline for converting ND2 files to OME TIFF using an alternative (Java-based) library.

Here are a few typical use cases:

### Converting ND2 to tiled pyramidal OME TIFF with bfconvert

```text
set BF_MAX_MEM=4g
bfconvert.bat -no-upgrade -bigtiff -pyramid-scale 2 -pyramid-resolutions 6 -noflat -tilex 256 -tiley 256 input_image.nd2 pyramidal.ome.tif
```

### Inspecting the structure of an OME TIFF file

```text
showinf.bat pyramidal.ome.tif
```

### Inspecting the OME XML atrributes in an OME TIFF file

```text
tiffcomment.bat pyramidal.ome.tif
```
