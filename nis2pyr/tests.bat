# Seems correct
python nis2pyr.py "g:\NISMakePyramidal\Testfiles\BF\RGB-8bit\B-1981946 1-1.2.nd2" e:\temp\bf1.ome.tif
python nis2pyr.py "g:\NISMakePyramidal\Testfiles\Fluo\3x-16bit\Slide3-12-2_Region0001_Channel395,488,555_1_Seq0054.nd2" e:\temp\brol.ome.tif
python nis2pyr.py "g:\NISMakePyramidal\Testfiles\Fluo\5x-16bit\Slide1-5-1_Region0001_Channel730,640,555,488,395_Seq0003.nd2" e:\temp\brol7.ome.tif
python nis2pyr.py "g:\NISMakePyramidal\Testfiles\Fluo\Mono-16bit\Slide1-1-2_Region0001_Channel555_Seq0003.nd2" e:\temp\mono.ome.tif
python nis2pyr.py "g:\NISMakePyramidal\Testfiles\SlideExpressAxelle\Slide2-17-1_ChannelBrightfield_Seq0080.nd2" e:\temp\seq80.ome.tif
python nis2pyr.py "g:\NISMakePyramidal\Testfiles\Unknown\Mono-16bit\ChannelBF_Seq0000.nd2" e:\temp\mono-seq0.ome.tif
python nis2pyr.py "g:\NISMakePyramidal\Testfiles\Unknown\Mono-16bit\ChannelBF_Seq0001.nd2" e:\temp\mono-seq1.ome.tif

# Output seems wrong, it is as if one channel is duplicated (?)
python nis2pyr.py "g:\NISMakePyramidal\Testfiles\Fluo\3x-16bit\SlideExpress20x.nd2" e:\temp\slidex.ome.tif

# Output is wrong, color seems to be missing, also a diagonal pattern
python nis2pyr.py "g:\NISMakePyramidal\Testfiles\BF\RGB-8bit\Slide2-3-1_ChannelBrightfield_Seq0001.nd2" e:\temp\bf2.ome.tif

ND2 metadata: {'width': 12730, 'width_bytes': 38192, 'height': 5039, 'components': 3, 'bitsize_memory': 8, 
'bitsize_significant': 8, 'sequence_count': 1, 'tile_width': 12730, 'tile_height': 5039, 
'compression': None, 'compression_quality': 0, 'plane_count': 1, 'angle': -3.1393237255622073,
'calibration_um': 3.999999999999999, 'time_start_jdn': 2459278.9415225117,
'time_start': datetime.datetime(2021, 3, 5, 11, 35, 47, 545007), 
'time_start_utc': datetime.datetime(2021, 3, 5, 10, 35, 47, 545007), 
'objective': 'Plan Apo λ 2x', 'magnification': -1.0, 'NA': 0.1, 'refractive_index1': 1.0, 
'refractive_index2': 1.0, 'pinhole': 0.0, 'zoom': 0.6000000000000001, 'projective_mag': 1.0, 
'image_type': 'normal', 'z_home': None, 'frame_rate': None, 
'plane_0': {'components': 3, 
'rgb_value': (1.0, 1.0, 1.0), 'name': 'Brightfield', 'oc': '2x_BF-RGB_WeiTing', 'emission_nm': -1.0}}
Note that width * 3 channels = 12730 * 3 = 38190 but metadata says width_bytes = 38192,
so perhaps there is a bug where the reader should skip the last 2 bytes of each scanline?
Also: the yellow boxes are missing, so the pyramidal tiff has no colors
See perhaps https://www.javatips.net/api/VisAD-master/deps/src/loci/formats/in/ND2Reader.java
for info on how to correctly read the data (but verify that it indeed reads it correctly). 
Search for padRow in the java source code. Alternatively, the problem may be with tile_height=5039

# Crash. Is it related to the size of the image (79200 x 26829 pixels). Out of memory? Or an integer overflow?
# Could try this on a machine with more than 16 GB RAM.
python nis2pyr.py "g:\NISMakePyramidal\Testfiles\SlideExpressAxelle\Slide2-17-1_ChannelBrightfield_Seq0079.nd2" e:\temp\seq79.ome.tif

Reading g:\NISMakePyramidal\Testfiles\SlideExpressAxelle\Slide2-17-1_ChannelBrightfield_Seq0079.nd2 with ND2Reader_SDK
E:\Anaconda3\envs\nis\lib\site-packages\pims\base_frames.py:472: UserWarning: Please call FramesSequenceND.__init__() at the start of thethe reader initialization.
  warn("Please call FramesSequenceND.__init__() at the start of the"
ND2 file: #frames=1, #components=3, #planes=1, bits per component=8, is RGB=True, pixel size=0.48 um, frames.sizes={'x': 79200, 'y': 26829, 'c': 3}
Reading image
Traceback (most recent call last):
  File "nis2pyr.py", line 100, in <module>
    image, metadata = read_nd2(args.nd2_filename)
  File "E:\git\bits\bioimaging\NISMakePyramidal\src\main\python\reader.py", line 34, in read_nd2
    image = frames[0]
  File "E:\Anaconda3\envs\nis\lib\site-packages\slicerator\__init__.py", line 188, in __getitem__
    return self._get(indices)
  File "E:\Anaconda3\envs\nis\lib\site-packages\pims\base_frames.py", line 98, in __getitem__
    return self.get_frame(key)
  File "E:\Anaconda3\envs\nis\lib\site-packages\pims\base_frames.py", line 592, in get_frame
    result = self._get_frame_wrapped(**coords)
  File "E:\Anaconda3\envs\nis\lib\site-packages\pims\base_frames.py", line 252, in get_frame_T
    return get_frame(**ind).transpose(transposition)
  File "E:\Anaconda3\envs\nis\lib\site-packages\pims\base_frames.py", line 265, in get_frame_bundled
    frame = get_frame(**ind)
  File "E:\Anaconda3\envs\nis\lib\site-packages\pims\base_frames.py", line 303, in get_frame_dropped
    result = get_frame(**ind)
  File "E:\Anaconda3\envs\nis\lib\site-packages\pims_nd2\nd2reader.py", line 194, in get_frame_2D
    h.Lim_FileGetImageData(self._handle, i, self._buf_p, self._buf_md)
OSError: exception: access violation writing 0x00000271BF0DB000
