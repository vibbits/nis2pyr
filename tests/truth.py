# This file contains the ground truth information for the test images.

# The info in the 'nd2' dicts was obtained or validated with NIS-Elements
# Viewer. The 'pixels' entry is a list of (image coordinates, pixel
# intensities) pairs, where the image coordinates are the 7D image
# coordinates TPZC1YX (for non RGB) or TPZ1YXS (for RGB), and the pixel
# intensities are the pixel values for the channels.

# The 'tiff' dicts describe the structure of the OME TIFF obtained after
# converting the ND2 file. The 'series' value is equal to the number of
# positions in the ND2 file (the P-axis).

from tifffile import TIFF


TRUTH = {'BF007.nd2':
         {'nd2': {'shape': (1, 1, 1, 1, 1, 156, 164),  # TPZC1YX
                  'is_rgb': False,
                  'dtype': 'uint16',
                  'voxelsize': (0.158389678930686, 0.158389678930686, None),
                  'channels': [('405/488/561/633nm', (0, 30, 255))],
                  'pixels': [((0, 0, 0, 0, 0, 15, 105), 53635),
                             ((0, 0, 0, 0, 0, 89, 26), 14093)]},
          'tiff': {'pages': 1,
                   'series': 1,
                   'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

         'MeOh_high_fluo_007.nd2':
         {'nd2': {'shape': (13, 1, 1, 1, 1, 600, 800),  # TPZC1YX
                  'is_rgb': False,
                  'dtype': 'uint16',
                  'voxelsize': (0.37, 0.37, None),
                  'channels': [('pdt-405', (255, 0, 0))],
                  'pixels': [((0, 0, 0, 0, 0, 74, 657), 4095),
                             ((0, 0, 0, 0, 0, 250, 101), 1822),
                             ((7, 0, 0, 0, 0, 419, 542), 27),
                             ((12, 0, 0, 0, 0, 131, 142), 1703),
                             ]},
          'tiff': {'pages': 13,
                   'series': 1,
                   'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

         '130606_JCC719_003.nd2':
         {'nd2': {'shape': (20, 1, 8, 1, 1, 232, 304),  # TPZC1YX
                  'is_rgb': False,
                  'dtype': 'uint16',
                  'voxelsize': (0.214990421455938, 0.214990421455938, 0.5),
                  'channels': [('GFP', (28, 255, 0))],
                  'pixels': [((0, 0, 0, 0, 0, 143, 54), 224),
                             ((0, 0, 0, 0, 0, 172, 179), 249),
                             ((8, 0, 0, 0, 0, 138, 242), 221),
                             ((8, 0, 7, 0, 0, 187, 151), 272),
                             ((19, 0, 0, 0, 0, 132, 200), 190),
                             ((19, 0, 7, 0, 0, 103, 107), 243),
                             ]},
          'tiff': {'pages': 20 * 8,
                   'series': 1,
                   'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

         'b16_14_12.nd2':  # note: channel "40x1" is mostly but not all zeros
         {'nd2': {'shape': (50, 1, 1, 2, 1, 1024, 1280),  # TPZC1YX
                  'is_rgb': False,
                  'dtype': 'uint8',
                  'voxelsize': (0.154798761609907, 0.154798761609907, None),
                  'channels': None,
                  'pixels': [((0, 0, 0, 0, 0, 308, 962), 89),
                             ((0, 0, 0, 1, 0, 308, 962), 2),
                             ((21, 0, 0, 0, 0, 308, 962), 89),
                             ((21, 0, 0, 1, 0, 308, 962), 4),
                             ((21, 0, 0, 0, 0, 308, 963), 88),
                             ((21, 0, 0, 1, 0, 308, 963), 1),
                             ((37, 0, 0, 0, 0, 739, 31), 180),
                             ((37, 0, 0, 1, 0, 739, 31), 0),
                             ((49, 0, 0, 0, 0, 442, 576), 165),
                             ((49, 0, 0, 1, 0, 442, 576), 0),
                             ]},
          'tiff': {'pages': 50 * 2,
                   'series': 1,
                   'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

         'but3_cont200-1.nd2':
         {'nd2': {'shape': (1, 5, 1, 2, 1, 1040, 1392),  # TPZC1YX
                  'is_rgb': False,
                  'dtype': 'uint16',
                  'voxelsize': (50.0, 50.0, None),
                  'channels': None,
                  'pixels': [((0, 0, 0, 0, 0, 412, 640), 3552),
                             ((0, 0, 0, 1, 0, 412, 640), 4522),
                             ((0, 0, 0, 0, 0, 760, 606), 14267),
                             ((0, 0, 0, 1, 0, 760, 606), 2168),
                             ((0, 2, 0, 0, 0, 600, 257), 11025),
                             ((0, 2, 0, 1, 0, 600, 257), 2007),
                             ((0, 4, 0, 0, 0, 748, 1160), 5924),
                             ((0, 4, 0, 1, 0, 748, 1160), 1414),
                             ]},
          'tiff': {'pages': 5 * 2,
                   'series': 5,
                   'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

         'sample_image.nd2':
         {'nd2': {'shape': (1, 1, 21, 5, 1, 1019, 1019),  # TPZC1YX
                  'is_rgb': False,
                  'dtype': 'uint16',
                  'voxelsize': (1.0153102411107793, 1.0153102411107793, 5.0),
                  'channels': [('CSU far red RNA', (255, 255, 255)),
                               ('CSU red RNA', (255, 0, 0)),
                               ('CSU green RNA', (0, 255, 0)),
                               ('CSU blue RNA', (0, 0, 255)),
                               ('CSU BF', (255, 255, 255))],
                  'pixels': [((0, 0, 10, 0, 0, 304, 530), 400),
                             ((0, 0, 10, 1, 0, 304, 530), 4112),
                             ((0, 0, 10, 2, 0, 304, 530), 4432),
                             ((0, 0, 10, 3, 0, 304, 530), 1535),
                             ((0, 0, 10, 4, 0, 304, 530), 4946),
                             ((0, 0, 0, 0, 0, 304, 530), 359),
                             ((0, 0, 0, 1, 0, 304, 530), 1452),
                             ((0, 0, 0, 2, 0, 304, 530), 368),
                             ((0, 0, 0, 3, 0, 304, 530), 184),
                             ((0, 0, 0, 4, 0, 304, 530), 2034),
                             ]},
          'tiff': {'pages': 21 * 5,
                   'series': 1,
                   'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},

         'multipoint.nd2':
         {'nd2': {'shape': (11, 4, 5, 1, 1, 1040, 1392),  # TPZC1YX
                  'is_rgb': False,
                  'dtype': 'uint16',
                  'voxelsize': (0.094731235788473, 0.094731235788473, 0.5),
                  'channels': None,
                  'pixels': [((0, 0, 0, 0, 0, 793, 1107), 11126),
                             ((0, 0, 4, 0, 0, 782, 1143), 554),
                             ((5, 0, 0, 0, 0, 507, 752), 2842),
                             ((5, 0, 4, 0, 0, 837, 1094), 7849),
                             ((10, 0, 0, 0, 0, 916, 1097), 11848),
                             ((10, 0, 4, 0, 0, 918, 1101), 15571),
                             ((0, 3, 0, 0, 0, 576, 182), 12558),
                             ((0, 3, 4, 0, 0, 854, 1281), 12657),
                             ((10, 3, 0, 0, 0, 347, 233), 8076),
                             ((10, 3, 4, 0, 0, 718, 195), 607),
                             ]},
          'tiff': {'pages': 11 * 4 * 5,
                   'series': 4,
                   'photometric': TIFF.PHOTOMETRIC.MINISBLACK}},
         }
