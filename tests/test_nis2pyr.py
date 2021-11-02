import os
import pytest
from nis2pyr.nis2pyr import main


@pytest.mark.parametrize("compression,pyramid_levels,tile_size",
                         [(None, None, None),
                          (None, 4, None),
                          ("zlib", None, 512),
                          ("zlib", 2, 128)])
def test_main(mocker,
              easy_nd2,
              input_dir,
              compression,
              pyramid_levels,
              tile_size):

    basename = os.path.basename(easy_nd2)
    input_file = os.path.join(input_dir, basename)

    args = ["nis2pyr"]
    if compression:
        args.extend(["--compression", compression])
    if pyramid_levels:
        args.extend(["--pyramid-levels", str(pyramid_levels)])
    if tile_size:
        args.extend(["--tile-size", str(tile_size)])
    args.append(input_file)

    mocker.patch("sys.argv", args)
    result = main()
    assert result == 0

    output_file = os.path.join(input_dir, basename[:-4] + '.ome.tif')
    assert os.path.exists(output_file)
