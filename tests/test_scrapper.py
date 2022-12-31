from conftest import temp_dir_name, projects_test_directory
import sys

# Path adjustment to add scrapper methods
sys.path.append(projects_test_directory)
from scrapper.scrapper_methods import *
#


class Test_Scrapper:
    BATTLESHIP_THREAD_PATH = projects_test_directory + "/test_cases/battleship/battleship.html"
    BATTLESHIP_THREAD_NAME = "Battleship Bread (Real Ones)"

    def test_download_thread(self, setup_and_teardown_at_temp_dir):
        """
        Tests main functionality by creating temporary directory, downloading files found in locally installed thread.
        Deletes temporary directory after conclusion.

        Args:
            create_and_cleanup_temp_dir: Pytest fixture with setup and teardown functions.

        """
        selected_thread_link = "https://boards.4chan.org/wg/thread/7950511"
        selected_download_path_link = "."

        number_of_links = download_files_from_thread(selected_thread_link, selected_download_path_link)
        assert os.getcwd().endswith(temp_dir_name)
        assert len(os.listdir()) == number_of_links

    def test_get_battleship_thread_name(self, setup_at_battleship_thread_dir):
        """
        Test local files at ./test_cases to check if name validations are working.
        In threads, 2 different patterns are found, nameless threads with big commentaries and threads with names.
        """

        html = get_thread_data(self.BATTLESHIP_THREAD_PATH)
        soup = make_soup(html, SELECTED_PARSER)
        name = get_thread_name(soup)

        assert self.BATTLESHIP_THREAD_NAME.startswith(name)
