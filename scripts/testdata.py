# Publicly available ND2 files for testing.

URL_PREFIX = 'https://downloads.openmicroscopy.org/images/ND2/'

IMAGES = ['maxime/BF007.nd2',
          'karl/sample_image.nd2',
          'aryeh/qa-9507/control003.nd2',
          'aryeh/MeOh_high_fluo_011.nd2',
          'aryeh/MeOh_high_fluo_007.nd2',
          'aryeh/MeOh_high_fluo_003.nd2',
          'aryeh/b16_pdtB+y50__crop.nd2',
          'aryeh/rfp_h2a_cells_02.nd2',
          'aryeh/old_cells_02.nd2',
          'aryeh/4_2_1_cont_NoMR001.nd2',
          'aryeh/4_con_2_1_cot002.nd2',
          'aryeh/multipoint.nd2',
          'aryeh/but3_cont2002.nd2',
          'aryeh/but3_cont200-1.nd2',
          'aryeh/por003.nd2',
          'aryeh/weekend002.nd2',
          'aryeh/b16_14_12.nd2',
          'aryeh/Time%20sequence%2024.nd2',
          'jonas/qa-7534/130606_JCC719_003.nd2',
          # jonas/movieSize/...
          # jonas/jonas_nd2Test/...
          # jonas/divisionByZero/...
          # jonas/512c/...
          'jonas/JJ1473_control_24h/JJ1473_control_24h_03.nd2',
          'jonas/JJ1473_control_24h/JJ1473_conrol_24h_02.nd2',
          'jonas/2.nd2',
          'jonas/3.nd2',
          'jonas/100217_OD122_001.nd2',
          'jonas/2112-2265.nd2',
          'jonas/control002.nd2',
          'jonas/header_test2.nd2',
          'jonas/header_test1.nd2',
          'jonas/multicolorTest.nd2',
          ]

URLS = [URL_PREFIX + image for image in IMAGES]
