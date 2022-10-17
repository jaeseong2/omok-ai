import os

import pytest

from utils.resources import ResourceManager


@pytest.fixture(scope="module")
def resource_manager():
    return ResourceManager(
        os.path.join(os.path.dirname(__file__), "resources")
    )
