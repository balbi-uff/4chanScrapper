import os

from conftest import temp_dir_path, temp_dir_name, projects_test_directory
import sys

# Path adjustment to add scrapper methods
sys.path.append(projects_test_directory)
from scrapper.scrapper_methods import *
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
        selected_thread_link = "https://boards.4chan.org/wg/thread/7950511"
        selected_download_path_link = "."

        number_of_links = download_files_from_thread(selected_thread_link, selected_download_path_link)
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
        execution_code = os.system("python 4chanScrapper.py")
        assert execution_code == self.WINDOWS_ERROR_CODE

    def test_download_thread_from_command_line_auto_mode(self, setup_and_teardown_at_battleship_thread_dir):
        """
        Tests program's response when correct arguments are passed. Expects OS success code 0.
        Args:
            setup_and_teardown_at_battleship_thread_dir: Pytest fixture.
        """
        battleship_thread_file_full_path = projects_test_directory + "/test_cases/battleship/battleship.html"
        download_path = temp_dir_path
        number_of_images_in_thread = 16

        execution_code = os.system(f"python 4chanScrapper.py {battleship_thread_file_full_path} {download_path}")
        assert execution_code == 0
        os.chdir(temp_dir_path)
        assert len(os.listdir()) == number_of_images_in_thread

    def test_download_thread_from_command_line_manual_mode(self, setup_and_teardown_at_battleship_thread_dir):
        battleship_thread_file_full_path = projects_test_directory + "/test_cases/battleship/battleship.html"
        download_path = temp_dir_path
        number_of_images_in_thread = 16


        pass