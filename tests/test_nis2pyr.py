import os
from nis2pyr.nis2pyr import main


def test_main(mocker, easy_nd2, input_dir):
    basename = os.path.basename(easy_nd2)
    input_file = os.path.join(input_dir, basename)

    mocker.patch(
        "sys.argv",
        [
            "nis2pyr",
            "--compression",
            "zlib",
            "--pyramid-levels",
            "4",
            "--tile-size",
            "512",
            input_file
        ]
    )

    result = main()
    assert result == 0

    output_file = os.path.join(input_dir, basename[:-4] + '.ome.tif')
    assert os.path.exists(output_file)
