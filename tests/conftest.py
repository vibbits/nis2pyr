import pytest
from truth import TRUTH

# Collect the filenames of all ND2 test images
ALL = list(TRUTH.keys())


@pytest.fixture(params=ALL, scope="session")
def any_nd2(request):
    return request.param


@pytest.fixture(scope="session")
def nd2_truth(any_nd2):
    filename = any_nd2
    return TRUTH[filename]['nd2']


@pytest.fixture(scope="session")
def tiff_truth(any_nd2):
    filename = any_nd2
    return TRUTH[filename]['tiff']


@pytest.fixture(scope="session")
def input_dir(request):
    return request.config.getoption('--input-dir')


@pytest.fixture(scope="session")
def output_dir(request):
    return request.config.getoption('--output-dir')


def pytest_addoption(parser):
    parser.addoption(
        '--input-dir',
        action='store',
        default=None,
        help='the directory with the ND2 test images'
    )
    parser.addoption(
        '--output-dir',
        action='store',
        default=None,
        help='the directory where the OME TIFFs will be written'
    )
