# This file contains the ground truth information for the test images.

# The info in the 'nd2' dicts was obtained or validated with NIS-Elements
# Viewer. The 'pixels' entry is a list of (image coordinates, pixel
# intensity) pairs, where the image coordinates are the 7D image
# coordinates TPZCYXS.

# The 'tiff' dicts describe the structure of the OME TIFF obtained after
# converting the ND2 file. The 'series' value is equal to the number of
# positions in the ND2 file (the P-axis).

from tifffile import TIFF


TRUTH = {
    'BF007.nd2':
    {'nd2': {'shape': (1, 1, 1, 1, 156, 164, 1),  # TPZCYXS
             'is_rgb': False,
             'is_legacy': False,
             'dtype': 'uint16',
             'voxelsize': (0.158389678930686, 0.158389678930686, None),
             'channels': [('405/488/561/633nm', (0, 30, 255))],
             'pixels': [((0, 0, 0, 0, 15, 105, 0), 53635),
                        ((0, 0, 0, 0, 89, 26, 0), 14093)]},
     'tiff': {'pages': 1,
              'series': 1,
              'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

    'Time%20sequence%2024.nd2':  # JPEG 2000 based file, see NOTES.md
    {'nd2': {'shape': (60, 1, 1, 1, 1024, 1280, 3),  # TPZCYXS
             'is_rgb': True,
             'is_legacy': True,
             'dtype': 'uint8',
             'voxelsize': (0.15, 0.15, None),
             'channels': None,
             # component order is R, G, B
             'pixels': [((0, 0, 0, 0, 0, 0, 0), 0),
                        ((0, 0, 0, 0, 0, 0, 1), 135),
                        ((0, 0, 0, 0, 0, 0, 2), 217),
                        ((0, 0, 0, 0, 0, 1, 0), 0),
                        ((0, 0, 0, 0, 0, 1, 1), 135),
                        ((0, 0, 0, 0, 0, 1, 2), 220),
                        ((0, 0, 0, 0, 0, 4, 0), 0),
                        ((0, 0, 0, 0, 0, 4, 1), 136),
                        ((0, 0, 0, 0, 0, 4, 2), 228),
                        ((9, 0, 0, 0, 397, 990, 0), 0),
                        ((9, 0, 0, 0, 397, 990, 1), 18),
                        ((9, 0, 0, 0, 397, 990, 2), 34),
                        ((59, 0, 0, 0, 618, 696, 0), 14),
                        ((59, 0, 0, 0, 618, 696, 1), 117),
                        ((59, 0, 0, 0, 618, 696, 2), 204),
                        ((59, 0, 0, 0, 618, 697, 0), 2),
                        ((59, 0, 0, 0, 618, 697, 1), 138),
                        ((59, 0, 0, 0, 618, 697, 2), 235),
                        ((59, 0, 0, 0, 618, 698, 0), 0),
                        ((59, 0, 0, 0, 618, 698, 1), 156),
                        ((59, 0, 0, 0, 618, 698, 2), 242),
                        ((59, 0, 0, 0, 222, 930, 0), 0),
                        ((59, 0, 0, 0, 222, 930, 1), 124),
                        ((59, 0, 0, 0, 222, 930, 2), 205)]},
     'tiff': {'pages': 60,
              'series': 1,
              'photometric': TIFF.PHOTOMETRIC.RGB}},

    'MeOh_high_fluo_007.nd2':
    {'nd2': {'shape': (13, 1, 1, 1, 600, 800, 1),  # TPZCYXS
             'is_rgb': False,
             'is_legacy': False,
             'dtype': 'uint16',
             'voxelsize': (0.37, 0.37, None),
             'channels': [('pdt-405', (255, 0, 0))],
             'pixels': [((0, 0, 0, 0, 74, 657, 0), 4095),
                        ((0, 0, 0, 0, 250, 101, 0), 1822),
                        ((7, 0, 0, 0, 419, 542, 0), 27),
                        ((12, 0, 0, 0, 131, 142, 0), 1703)]},
     'tiff': {'pages': 13,
              'series': 1,
              'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

    '130606_JCC719_003.nd2':
    {'nd2': {'shape': (20, 1, 8, 1, 232, 304, 1),  # TPZCYXS
             'is_rgb': False,
             'is_legacy': False,
             'dtype': 'uint16',
             'voxelsize': (0.214990421455938, 0.214990421455938, 0.5),
             'channels': [('GFP', (28, 255, 0))],
             'pixels': [((0, 0, 0, 0, 143, 54, 0), 224),
                        ((0, 0, 0, 0, 172, 179, 0), 249),
                        ((8, 0, 0, 0, 138, 242, 0), 221),
                        ((8, 0, 7, 0, 187, 151, 0), 272),
                        ((19, 0, 0, 0, 132, 200, 0), 190),
                        ((19, 0, 7, 0, 103, 107, 0), 243)]},
     'tiff': {'pages': 20 * 8,
              'series': 1,
              'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

    'b16_14_12.nd2':  # note: channel "40x1" is mostly but not all zeros
    {'nd2': {'shape': (50, 1, 1, 2, 1024, 1280, 1),  # TPZCYXS
             'is_rgb': False,
             'is_legacy': True,
             'dtype': 'uint8',
             'voxelsize': (0.154798761609907, 0.154798761609907, None),
             'channels': None,
             'pixels': [((0, 0, 0, 0, 308, 962, 0), 89),
                        ((0, 0, 0, 1, 308, 962, 0), 2),
                        ((21, 0, 0, 0, 308, 962, 0), 89),
                        ((21, 0, 0, 1, 308, 962, 0), 4),
                        ((21, 0, 0, 0, 308, 963, 0), 88),
                        ((21, 0, 0, 1, 308, 963, 0), 1),
                        ((37, 0, 0, 0, 739, 31, 0), 180),
                        ((37, 0, 0, 1, 739, 31, 0), 0),
                        ((49, 0, 0, 0, 442, 576, 0), 165),
                        ((49, 0, 0, 1, 442, 576, 0), 0)]},
     'tiff': {'pages': 50 * 2,
              'series': 1,
              'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

    'but3_cont200-1.nd2':
    {'nd2': {'shape': (1, 5, 1, 2, 1040, 1392, 1),  # TPZCYXS
             'is_rgb': False,
             'is_legacy': True,
             'dtype': 'uint16',
             'voxelsize': (50.0, 50.0, None),
             'channels': None,
             'pixels': [((0, 0, 0, 0, 412, 640, 0), 3552),
                        ((0, 0, 0, 1, 412, 640, 0), 4522),
                        ((0, 0, 0, 0, 760, 606, 0), 14267),
                        ((0, 0, 0, 1, 760, 606, 0), 2168),
                        ((0, 2, 0, 0, 600, 257, 0), 11025),
                        ((0, 2, 0, 1, 600, 257, 0), 2007),
                        ((0, 4, 0, 0, 748, 1160, 0), 5924),
                        ((0, 4, 0, 1, 748, 1160, 0), 1414)]},
     'tiff': {'pages': 5 * 2,
              'series': 5,
              'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

    'sample_image.nd2':
    {'nd2': {'shape': (1, 1, 21, 5, 1019, 1019, 1),  # TPZCYXS
             'is_rgb': False,
             'is_legacy': False,
             'dtype': 'uint16',
             'voxelsize': (1.0153102411107793, 1.0153102411107793, 5.0),
             'channels': [('CSU far red RNA', (255, 255, 255)),
                          ('CSU red RNA', (255, 0, 0)),
                          ('CSU green RNA', (0, 255, 0)),
                          ('CSU blue RNA', (0, 0, 255)),
                          ('CSU BF', (255, 255, 255))],
             'pixels': [((0, 0, 10, 0, 304, 530, 0), 400),
                        ((0, 0, 10, 1, 304, 530, 0), 4112),
                        ((0, 0, 10, 2, 304, 530, 0), 4432),
                        ((0, 0, 10, 3, 304, 530, 0), 1535),
                        ((0, 0, 10, 4, 304, 530, 0), 4946),
                        ((0, 0, 0, 0, 304, 530, 0), 359),
                        ((0, 0, 0, 1, 304, 530, 0), 1452),
                        ((0, 0, 0, 2, 304, 530, 0), 368),
                        ((0, 0, 0, 3, 304, 530, 0), 184),
                        ((0, 0, 0, 4, 304, 530, 0), 2034)]},
     'tiff': {'pages': 21 * 5,
              'series': 1,
              'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

    'multipoint.nd2':
    {'nd2': {'shape': (11, 4, 5, 1, 1040, 1392, 1),  # TPZCYXS
             'is_rgb': False,
             'is_legacy': True,
             'dtype': 'uint16',
             'voxelsize': (0.094731235788473, 0.094731235788473, 0.5),
             'channels': None,
             'pixels': [((0, 0, 0, 0, 793, 1107, 0), 11126),
                        ((0, 0, 4, 0, 782, 1143, 0), 554),
                        ((5, 0, 0, 0, 507, 752, 0), 2842),
                        ((5, 0, 4, 0, 837, 1094, 0), 7849),
                        ((10, 0, 0, 0, 916, 1097, 0), 11848),
                        ((10, 0, 4, 0, 918, 1101, 0), 15571),
                        ((0, 3, 0, 0, 576, 182, 0), 12558),
                        ((0, 3, 4, 0, 854, 1281, 0), 12657),
                        ((10, 3, 0, 0, 347, 233, 0), 8076),
                        ((10, 3, 4, 0, 718, 195, 0), 607)]},
     'tiff': {'pages': 11 * 4 * 5,
              'series': 4,
              'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

    # The file control003.nd2 is peculiar. We decided to test that the nd2
    # library returns the basic ND2 file contents, not the apparently
    # undocumented behavior of NIS-Elements. See NOTES.md for details.
    'control003.nd2':
    {'nd2': {'shape': (1, 10, 17, 3, 1200, 1600, 1),  # TPZCYXS
             'is_rgb': False,
             'is_legacy': False,
             'dtype': 'uint16',
             'voxelsize': (0.12254901960784287, 0.12254901960784287, 0.2),
             'channels': [('dapi-uv', (111, 40, 255)),
                          ('cy3', (255, 128, 0)),
                          ('cy3_25', (255, 196, 0))],
             'pixels': [((0, 0, 0, 0, 0, 0, 0), 0),  # NIS-Elements: 263
                        ((0, 0, 0, 1, 0, 0, 0), 238),
                        ((0, 0, 0, 2, 0, 0, 0), 93),
                        ((0, 0, 0, 0, 0, 1, 0), 0),  # NIS-Elements: 287
                        ((0, 0, 0, 1, 0, 1, 0), 238),
                        ((0, 0, 0, 2, 0, 1, 0), 105),
                        ((0, 0, 0, 0, 0, 2, 0), 0),  # NIS-Elements: 295
                        ((0, 0, 0, 1, 0, 2, 0), 271),
                        ((0, 0, 0, 2, 0, 2, 0), 101),
                        ((0, 0, 8, 0, 0, 0, 0), 263),
                        ((0, 0, 8, 0, 0, 1, 0), 287),
                        ((0, 0, 8, 0, 0, 2, 0), 295),
                        ((0, 9, 8, 0, 436, 1221, 0), 1038),
                        ((0, 9, 8, 1, 436, 1221, 0), 3739),
                        ((0, 9, 8, 2, 436, 1221, 0), 973),
                        ((0, 9, 16, 0, 462, 1256, 0), 0),  # NIS-Elements: 957
                        ((0, 9, 16, 1, 462, 1256, 0), 2430),
                        ((0, 9, 16, 2, 462, 1256, 0), 578)]},
     'tiff': {'pages': 10 * 17 * 3,
              'series': 10,
              'photometric': TIFF.PHOTOMETRIC.MINISBLACK}}
}
