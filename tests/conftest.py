import pytest
import sys, os
from shutil import rmtree

projects_test_directory = sys.path[0]
projects_root = projects_test_directory + "/.."
temp_dir_name = "$temp"


@pytest.fixture()
def setup_and_teardown_at_temp_dir():
    # setup
    os.chdir(projects_test_directory + "/test_cases")
    os.mkdir(temp_dir_name)
    os.chdir(temp_dir_name)

    # test
    yield

    # teardown
    os.chdir("..")
    rmtree(f"{temp_dir_name}")


@pytest.fixture()
def setup_at_battleship_thread_dir():
    # setup
    os.chdir(projects_test_directory + "/test_cases/battleship")

    # test
    yield
