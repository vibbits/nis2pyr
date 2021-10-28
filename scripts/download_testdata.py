import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen
import testdata


def download(url: str) -> bytes:
    with urlopen(url) as f:
        data = f.read()
    return data


def save(data: bytes, filename: str) -> None:
    with open(filename, 'wb') as f:
        f.write(data)


def download_and_save(url: str, output_folder: str) -> None:
    print(f'Fetching {url}')
    data = download(url)
    print(f'Saving {url}')
    filename = os.path.join(output_folder, Path(url).name)
    save(data, filename)


def main(output_folder: str) -> None:
    Path(output_folder).mkdir(exist_ok=True)
    with ThreadPoolExecutor() as executor:
        print(f'Downloading test images to {output_folder}')
        executor.map(lambda url: download_and_save(url, output_folder),
                     testdata.URLS)


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Download ND2 test images")
    parser.add_argument(
        'output_folder',
        type=str,
        help='directory to save the test images in; the directory will be '
             'created if it does not exist yet')
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()
    main(args.output_folder)
