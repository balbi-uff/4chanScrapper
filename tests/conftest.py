import shutil

import pytest
import sys, os
from shutil import rmtree

projects_test_directory = sys.path[0]
projects_root = projects_test_directory + "/.."
temp_dir_name = "$temp"
temp_dir_path = projects_test_directory + "/test_cases/" + temp_dir_name


def remove_recursive(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)


@pytest.fixture()
def setup_and_teardown_at_temp_dir():
    # setup
    os.mkdir(temp_dir_path)
    os.chdir(temp_dir_path)

    # test
    yield

    # teardown
    os.chdir("..")
    remove_recursive(f"{temp_dir_path}")


@pytest.fixture()
def setup_for_thread_name_at_battleship_thread_dir():
    # setup
    os.chdir(projects_test_directory + "/test_cases/battleship")

    # test
    yield

@pytest.fixture()
def setup_and_teardown_at_battleship_thread_dir():
    # setup
    os.chdir(projects_root)
    # create temp directory
    os.mkdir(temp_dir_path)

    # test
    yield

    # teardown
    os.chdir("..")
    remove_recursive(temp_dir_path)
