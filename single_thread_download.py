from json.tool import main
from async_img_scrapper import async_downloader
import os
import sys

"""
This test shows if the program is working as expected.

It will scrap files from a thread saved in test/art_deco_thread.html
and save them in test/art_deco_thread_images.

"""

TEMP_DIR_NAME = '$DELETE$ME$'

def test_async_downloader_directly(link_to_test):
    """
    This function tests if the number of files saved is correct.
    """
    if not os.path.exists(TEMP_DIR_NAME):
        os.mkdir(TEMP_DIR_NAME)

    real_number_of_images = async_downloader(link_to_test, "./" + TEMP_DIR_NAME, False)
    
    number_of_downloaded_images = len(os.listdir())
    os.chdir("..")
    os.system("rm -rf " + TEMP_DIR_NAME)

    try:
        assert real_number_of_images == number_of_downloaded_images
        print("async_downloader working!")
    except AssertionError:
        print("ERROR -------------------------------------------------------------")
        print("The number of images should be the same!\nrealN:{}|NumOfDownloadedImgs:{}")
        print("Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    html_path_to_test = "https://boards.4chan.org/wg/thread/7868002"
    test_async_downloader_directly(html_path_to_test)
