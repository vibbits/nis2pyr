# Notes concerning the test files

## Test file "control003.nd2"

Detailed analysis of the test file
[control003.nd2](https://downloads.openmicroscopy.org/images/ND2/aryeh/qa-9507/control003.nd2),
where the image data returned by the [nd2 library](https://github.com/tlambert03/nd2)
is inconsistent with what NIS-Elements displays and measures.

### General

The control003.nd2 file has images for 10 XY positions, and 17 Z positions.
The Z-planes are spaced 20 um apart, with Z-position 9/17 corresponding
to Z=0.00 um (indicated in the NIS-Elements UI). The images have 3 channels,
the first channel being "dapi-uv". Careful inspection in NIS-Elements shows
that the contents of the "dapi-uv" channel is actually identical for each of
the Z-planes. The contents of the 2 other channels vary for varying Z, as
expected.

### ND2 file contents

Inspection of the ND2 file contents itself, however, shows that the
"dapi-uv" channel contents are all zero, except for the 9-th Z-plane!
For example, the file contents at file offset 0x00194000
(inside the "ImageDataSeq|0!" chunk) correspond to the first 3 pixels of the image

```text
    00 00 EE 00 5D 00
    00 00 EE 00 69 00
    00 00 0F 01 65 00
```

The values correspond to the first z-plane in the first XY position,
in the top left corner of the image. In NIS-Elements we measure the following
intensity for the 3 channels, the first channel being "dapi-uv":

```text
    x=0 y=0 (263, 238,  93) = (0x0107, 0x00EE, 0x005D)
    x=1 y=0 (287, 238, 105) = (0x011F, 0x00EE, 0x0069)
    x=2 y=0 (295, 271, 101) = (0x0127, 0x010F, 0x0065)
```

The color values from NIS-Elements indeed match those present in the ND2 file,
*except* for the values in the first channel, where we find zeros in the ND2
file but not in NIS-Elements.

So, where does NIS-Elements gets these non-zero, values?! It seems
to be an undocumented feature, where intensity data from the "reference"
Z-plane (for z=0.0 um) is copied into the other Z-planes by NIS-Elements.

### ND2 library

Accessing the ND2 file using the [nd2 library](https://github.com/tlambert03/nd2):

```python
>>> import nd2
>>> import numpy as np

>>> nd = nd2.ND2File('control003.nd2')
>>> nd.sizes
{'P': 10, 'Z': 17, 'C': 3, 'Y': 1200, 'X': 1600}
>>> a = nd.asarray()

>>> # Examine the first pixels for position 0 and Z=0
>>> np.transpose(a[0,0,:,0,0:3])
array([[  0, 238,  93],
       [  0, 238, 105],
       [  0, 271, 101]], dtype=uint16)

>>> # Examine the first pixels for position 0 and Z=8
>>> np.transpose(a[0,8,:,0,0:3])
array([[263, 225,  87],
       [287, 198,  76],
       [295, 267, 136]], dtype=uint16)
```

The nd2 library also returns zeros in the first channel of all z-planes except
for the 9-th, which is consistent with the ND2 file, but not with NIS-Elements.

### Export to TIFF from NIS-Elements

When exporting control003.nd2 to regular TIFFs (one per channel and per position)
using NIS-Elements, the first channel ("dapi-uv") again is *non-zero* for all Z-planes,
consistent with what NIS-Elements shows.

### Conversion to OME TIFF using "ND2 to OMETIFF Converter"

When converting control003.nd2 to OME TIFF using Nikon's "ND2 to OMETIFF Converter"
(downloadable from the Nikon [ND2SDK](https://www.nd2sdk.com/) page, after logging in), the resulting OME TIFF
however again has an empty "dapi-uv" channel, except for z=9 (corresponding to z=0.0 um).
It seems that this tool does not implement the undocumented feature that NIS-Elements
uses to come up with the duplicated image data for the "dapi-uv" channel in the other Z-planes.

## Test file "Time%20sequence%2024.nd2"

RGB image time series, 8 bits/component. Old JPEG2000 based ND2 file format (file magic bytes `00 00 00 0C`).

In NIS-Elements Viewer the images look blue, with the red component zero.

The ND2 file can actually be opened in Gimp as well, since it's a JPEG2000 file. Gimp seems to read only the first "page" (t=0), and also renders it blue (R=0).

The ND2 library also returns the components in R, G, B order. So there is no need to swap color components.

## Test file "Slide2-17-1_ChannelBrightfield_Seq0079.nd2" (private test file)

RGB image, 8 bits/component. New ND2 file format (file magic bytes `DA CE BE 0A`).

In Nis-Elements viewer we measure the following RGB values:

```text
             (red, green, blue)
x=63238, y=0: (192, 191, 166) = hex (C0, BF, A6)
x=63239, y=0: (191, 190, 164) = hex (BF, BE, A4)
x=63240, y=0: (191, 189, 164) = hex (BF, BD, A4)
x=63241, y=0: (192, 190, 166) = hex (C0, BE, A6)
x=63242, y=0: (192, 190, 166) = hex (C0, BE, A6)
x=63243, y=0: (191, 190, 166) = hex (BF, BE, A6)
x=63244, y=0: (191, 190, 166) = hex (BF, BE, A6)
x=63245, y=0: (190, 190, 166) = hex (BE, BE, A6)
x=63246, y=0: (189, 189, 164) = hex (BD, BD, A4)
```

If we search the ND2 file for these color values in R, G, B order:

```text
C0 BF A6 BF BE A4 BF BD A4 C0 BE A6 C0 BE A6 BF BE A6 BF BE A6 BE BE A6 BD BD A4
```

this search string is not found.

If however we search for the string in B, G, R order:

```text
A6 BF C0 A4 BE BF A4 BD BF A6 BE C0 A6 BE C0 A6 BE BF A6 BE BF A6 BE BE A4 BD BD
```

we find this sequence of color values in the .nd2 file at file offset 0x3E512.

This indicates that (at least in this file, and we suspect for all new file format RGB ND2 files) 
RGB color components are stored in BGR order: B G R B G R B G R ... for successive pixels.

This order is also what the ND2 library returns. When converting the ND2 file to
OME TIFF, we will swap the R and B components to the usual RGB order, since that is
also what consumers of the OME TIFF RGB file expect.