import pytest
import sys, os
from shutil import rmtree

project_root = sys.path[0]
temp_dir_name = "$temp"

# Path adjustment to add scrapper methods
sys.path.append(os.path.join(project_root, ".."))


#


@pytest.fixture()
def create_and_cleanup_temp_dir():
    # setup
    os.chdir(project_root + "/test_cases")
    os.mkdir(temp_dir_name)
    os.chdir(temp_dir_name)

    # test
    yield

    # teardown
    os.chdir("..")
    rmtree(f"{temp_dir_name}")
