from conftest import create_and_cleanup_temp_dir, temp_dir_name
import sys, os

# Path adjustment to add scrapper methods
project_root = sys.path[0]
sys.path.append(os.path.join(project_root, ".."))
from scrapper.scrapper_methods import *


#


class Test_Scrapper:
    def test_download_thread(self, create_and_cleanup_temp_dir):
        selected_thread_link = "https://boards.4chan.org/wg/thread/7950511"
        selected_download_path_link = "."

        number_of_links = download_files_from_thread(selected_thread_link, selected_download_path_link)
        assert os.getcwd().endswith(temp_dir_name)
        assert len(os.listdir()) == number_of_links
