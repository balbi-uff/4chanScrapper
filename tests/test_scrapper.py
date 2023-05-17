import os

from conftest import temp_dir_path, temp_dir_name, projects_test_directory
import sys

# Path adjustment to add scrapper methods
parent_dir = os.path.dirname(os.path.abspath(os.getcwd()))
sys.path.append(parent_dir)
from scrapper.scrapper_methods import *
from FchanScrapper import manual_mode_download


#


class Test_Scrapper:
    BATTLESHIP_THREAD_PATH = projects_test_directory + "/test_cases/battleship/battleship.html"
    BATTLESHIP_THREAD_NAME = "Battleship Bread (Real Ones)"
    WINDOWS_ERROR_CODE = 1

    def test_download_thread_directly(self, setup_and_teardown_at_temp_dir):
        """
        Tests main functionality by creating temporary directory, downloading files found in locally installed thread.
        Deletes temporary directory after conclusion.

        Args:
            setup_and_teardown_at_temp_dir: Pytest fixture with setup and teardown functions.

        """
        selected_thread_link = "https://boards.4chan.org/wg/thread/7986462"
        selected_download_path_link = "."

        number_of_links = download_files_from_thread(selected_thread_link, selected_download_path_link)
        assert os.getcwd().endswith(temp_dir_name)
        assert len(os.listdir()) == number_of_links

    def test_download_thread_from_manual_mode(self, setup_and_teardown_at_temp_dir):
        """
        Tests program's response when correct arguments are passed. Expects OS success code 0.
        Args:
            setup_and_teardown_at_temp_dir: Pytest fixture.

        Returns:

        """
        selected_thread_link = "https://boards.4chan.org/wg/thread/7986462"
        selected_download_path_link = "."  # cwd is $temp here at runtime

        arguments = [
            "FchanScrapper.py",
            "-m",
            selected_thread_link,
            selected_download_path_link,
            "--resolution",
            "1920",
            "1080"
        ]
        number_of_links = manual_mode_download(arguments)
        assert os.getcwd().endswith(temp_dir_name)
        assert len(os.listdir()) == number_of_links

    def test_download_thread_from_manual_mode_only_min_res(self, setup_and_teardown_at_temp_dir):
        """
        Tests program's response when correct arguments are passed. Expects OS success code 0.
        Args:
            setup_and_teardown_at_temp_dir: Pytest fixture.

        Returns:

        """
        selected_thread_link = "https://boards.4chan.org/wg/thread/7986462"
        selected_download_path_link = "."  # cwd is $temp here at runtime

        arguments = [
            "FchanScrapper.py",
            "-m",
            selected_thread_link,
            selected_download_path_link,
            "--min-res",
            "3200",
            "1800"
        ]
        number_of_links = manual_mode_download(arguments)
        assert os.getcwd().endswith(temp_dir_name)
        assert len(os.listdir()) == number_of_links

    def test_get_battleship_thread_name(self, setup_for_thread_name_at_battleship_thread_dir):
        """
        Test local files at ./test_cases to check if name validations are working.
        In threads, 2 different patterns are found, nameless threads with big commentaries and threads with names.
        """

        html = get_thread_data(self.BATTLESHIP_THREAD_PATH)
        soup = make_soup(html, SELECTED_PARSER)
        name = get_thread_name(soup)

        assert self.BATTLESHIP_THREAD_NAME.startswith(name)

    def test_download_thread_from_command_line_with_no_arguments(self, setup_and_teardown_at_battleship_thread_dir):
        """
        Tests program's response when no arguments are passed. Expects OS error code 1.
        Meaning "ERROR_SUCCESS" (https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-).
        """
        execution_code = os.system("python FchanScrapper.py")
        assert execution_code == self.WINDOWS_ERROR_CODE

    def test_download_thread_from_command_line_auto_mode(self, setup_and_teardown_at_battleship_thread_dir):
        """
        Tests program's response when correct arguments are passed. Expects OS success code 0.
        Args:
            setup_and_teardown_at_battleship_thread_dir: Pytest fixture.
        """
        # test_vars
        battleship_thread_file_full_path = projects_test_directory + "/test_cases/battleship/battleship.html"
        download_path = temp_dir_path
        number_of_images_in_thread = 16

        # test
        execution_code = os.system(f"python FchanScrapper.py {battleship_thread_file_full_path} {download_path}")
        os.chdir(temp_dir_path)

        # assertions
        assert execution_code == 0
        assert len(os.listdir()) == number_of_images_in_thread

    def test_download_thread_from_command_line_manual_mode_simple(self, setup_and_teardown_at_battleship_thread_dir):
        # test_vars
        battleship_thread_file_full_path = projects_test_directory + "/test_cases/battleship/battleship.html"
        download_path = temp_dir_path
        number_of_images_above_minimum_resolution_in_thread = 14

        # test
        command = f"python FchanScrapper.py -m {battleship_thread_file_full_path} {download_path} " \
                  "--resolution 1920 1080"
        execution_code = os.system(command)
        os.chdir(temp_dir_path)

        # assertions
        assert execution_code == 0
        assert len(os.listdir()) == number_of_images_above_minimum_resolution_in_thread

    def test_error_missing_arg_download_thread_cmd_line_manual_mode(self, setup_and_teardown_at_battleship_thread_dir):
        # test_vars
        battleship_thread_file_full_path = projects_test_directory + "/test_cases/battleship/battleship.html"
        download_path = temp_dir_path

        # test
        command = f"python FchanScrapper.py -m {battleship_thread_file_full_path} {download_path} " \
                  "--resolution 1080"
        execution_code = os.system(command)
        os.chdir(temp_dir_path)

        # assertions
        assert execution_code == self.WINDOWS_ERROR_CODE

    def test_download_thread_from_cmd_line_manual_mode_full_config(self, setup_and_teardown_at_battleship_thread_dir):
        """
        Tests program's response when all arguments are passed (correctly). Expects OS success code 0.
        Args:
            setup_and_teardown_at_battleship_thread_dir: Pytest fixture.
        """
        # test_vars
        battleship_thread_file_full_path = projects_test_directory + "/test_cases/battleship/battleship.html"
        download_path = temp_dir_path
        number_of_images_within_chosen_resolution_in_thread = 3  # Modify accordingly
        min_x_resolution = 1000
        min_y_resolution = 700
        max_x_resolution = 1921
        max_y_resolution = 1081

        # test
        command = f"python FchanScrapper.py -m {battleship_thread_file_full_path} {download_path} " \
                  f"--min-res {min_x_resolution} {min_y_resolution} " \
                  f"--max-res {max_x_resolution} {max_y_resolution}"
        execution_code = os.system(command)
        os.chdir(temp_dir_path)

        # assertions
        assert execution_code == 0
        assert len(os.listdir()) == number_of_images_within_chosen_resolution_in_thread

    def test_error_download_from_cmd_line_manual_full_config(self, setup_and_teardown_at_battleship_thread_dir):
        """
        Tests program's response when no arguments are passed. Expects OS success code 1.
        Args:
            setup_and_teardown_at_battleship_thread_dir: Pytest fixture.
        """
        # test_vars
        battleship_thread_file_full_path = projects_test_directory + "/test_cases/battleship/battleship.html"
        download_path = temp_dir_path
        max_x_resolution = 1921
        max_y_resolution = 1081

        # test
        command = f"python FchanScrapper.py -m {battleship_thread_file_full_path} {download_path} " \
                  f"--min-res" \
                  f"--max-res {max_x_resolution} {max_y_resolution}"
        execution_code = os.system(command)
        os.chdir(temp_dir_path)

        # assertions
        assert execution_code == self.WINDOWS_ERROR_CODE

    def test_download_thread_from_cmd_line_manual_mode_only_max(self, setup_and_teardown_at_battleship_thread_dir):
        """
        Tests program's response when half the arguments are passed (correctly). Expects OS success code 0.
        Args:
            setup_and_teardown_at_battleship_thread_dir: Pytest fixture.
        """
        # test_vars
        battleship_thread_file_full_path = projects_test_directory + "/test_cases/battleship/battleship.html"
        download_path = temp_dir_path
        number_of_images_within_chosen_resolution_in_thread = 2  # Modify accordingly
        max_x_resolution = 1200
        max_y_resolution = 800

        # test
        command = f"python FchanScrapper.py -m {battleship_thread_file_full_path} {download_path} " \
                  f"--max-res {max_x_resolution} {max_y_resolution}"
        execution_code = os.system(command)
        os.chdir(temp_dir_path)

        # assertions
        assert execution_code == 0
        assert len(os.listdir()) == number_of_images_within_chosen_resolution_in_thread

    def test_download_thread_from_cmd_line_manual_mode_only_min(self, setup_and_teardown_at_battleship_thread_dir):
        """
        Tests program's response when all arguments are passed (correctly). Expects OS success code 0.
        Args:
            setup_and_teardown_at_battleship_thread_dir: Pytest fixture.
        """
        # test_vars
        battleship_thread_file_full_path = projects_test_directory + "/test_cases/battleship/battleship.html"
        download_path = temp_dir_path
        number_of_images_within_chosen_resolution_in_thread = 4  # Modify accordingly
        min_x_resolution = 3200
        min_y_resolution = 1800

        # test
        command = f"python FchanScrapper.py -m {battleship_thread_file_full_path} {download_path} " \
                  f"--min-res {min_x_resolution} {min_y_resolution}"
        execution_code = os.system(command)
        os.chdir(temp_dir_path)

        # assertions
        assert execution_code == 0
        assert len(os.listdir()) == number_of_images_within_chosen_resolution_in_thread

    def test_automatic_directory_creation(self): # TODO: Implement
        pass