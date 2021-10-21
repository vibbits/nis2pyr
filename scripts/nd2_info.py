import argparse
import nd2
import os
import sys
from typing import Any, Dict, Iterator


def get_info(nd2_filename: str) -> Dict[str, Any]:
    with nd2.ND2File(nd2_filename) as nd2file:
        dims = nd2file.sizes
        axes = ''.join(dims.keys())
        rgb = nd2file.is_rgb
        datatype = str(nd2file.dtype)
        info = {'axes': axes,
                'dims': dims,
                'rgb': rgb,
                'datatype': datatype,
                'filename': nd2_filename,
                'voxelsize': nd2file.voxel_size(),
                'meta': nd2file.metadata
                }
        # Note that 'voxelsize' is always a triplet of values, even if they
        # are not actually correct because the axes are 'not calibrated'.
        # However, the metadata axesCalibrated (and axesCalibration) provide
        # additional information on calibration.
        return info


def enumerate_files(path: str, recursive: bool) -> Iterator[str]:
    assert os.path.isdir(path)
    for entry in os.scandir(path):
        if entry.is_file():
            yield os.path.join(path, entry.name)
        else:
            if recursive:
                yield from enumerate_files(entry.path, recursive)


def is_nd2(path: str) -> bool:
    return os.path.splitext(path)[1] == '.nd2'


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Dump basic info about ND2 files")
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='recurse into subdirectories; '
             'only relevant if a directory was specified')
    parser.add_argument(
        'path',
        type=str,
        help='an ND2 filename, or the name of a directory to scan '
             'for ND2 files')
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()
    path = args.path
    if os.path.isfile(path):
        if is_nd2(path):
            info = get_info(path)
            print(info)
    elif os.path.isdir(path):
        for f in enumerate_files(path, args.recursive):
            if is_nd2(f):
                info = get_info(f)
                print(info)
    else:
        print(f'{path} does not exist')
        sys.exit(1)
