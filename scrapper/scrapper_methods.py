import requests
import os
import asyncio
from bs4 import BeautifulSoup as make_soup
from time import time as timer

"""Scrapes every image from a thread, according to your specifications."""

# globals 
## constants
DIV_CLASS_STD_NAME = 'fileText'
THREAD_CLASS_STD_NAME = 'postMessage'
SELECTED_PARSER = 'lxml'
HTTP_PROTOCOL_SYMBOL = 'http'
NUM_IMG_STD_SPAN_CLASS = 'ts-images'
STD_PATH_DOWNLOAD = "."

## other globals
acceptedFormats = ['webm', '.mp4', '.mp3', '.mov'] # get from txt file
thread_name = None
ended_tasks = 0
number_of_tasks = 0


def download(file_link):
    """
    Download single image from link.
    """
    global ended_tasks, number_of_tasks
    
    # Inner methods
    def file_is_valid(filename):
        return filename[-4:] in acceptedFormats
    
    def get_filename(link):
        """
        Gets filename from link.
        """
        filename = ""
        tempLetter = ""
        while not tempLetter in ["\\", "/"]:
            tempLetter = link[-1]
            filename = tempLetter + filename
            link = link[:len(link) - 1]
        return filename[1:]
    
    # File Variables
    file_data = requests.get(file_link).content
    filename = get_filename(file_link)
    
    # Download
    with open(filename, 'wb') as tempDownload:
        if not file_is_valid(filename): # rejects non-declared types of files
            tempDownload.write(file_data)
    ended_tasks += 1

    print(f"{ended_tasks} of {number_of_tasks} downloaded!")
    return 0

async def download_image_task(img_link): # WATCH MY ASS
    """
    Function responsible for creating the task of downloading a single image.
    """
    link = HTTP_PROTOCOL_SYMBOL + ":" + img_link
    download(link)


def get_thread_data_from_web(thread_link):
    return requests.get(thread_link).content


def get_file_links_from_thread_divs(list_of_divs, **filters):
    def get_div_link(image_raw_div):
        div_soup = make_soup(image_raw_div, SELECTED_PARSER)
        
        return div_soup.find('a')['href']
    
    # filter this after primary tests
    file_links = [get_div_link(div_html) for div_html in list_of_divs]
    #
    return file_links
    


def get_all_divs_with_classname(soup, classname):
    return list(map(str, soup.findAll('div', class_=classname)))


def get_thread_name(soup):
    pass


async def download_tasks(download_path, links_from_threads_files):
    # Organizing download tasks
    thread_download_tasks = []
    
    #loop = asyncio.get_event_loop()
    os.chdir(download_path)
    
    for file_link in links_from_threads_files:
        task_name = file_link[-17:]
        thread_download_tasks.append(asyncio.create_task(download_image_task(file_link), name=task_name))
    
    await asyncio.gather(*thread_download_tasks)
    #loop.run_until_complete(asyncio.gather(*thread_download_tasks))
    #loop.close()
    



def download_files_from_thread(thread_link, download_path, **filters):
    """Download files from inputed thread.

    Args:
        thread_link (str): Thread link.
        download_path (str): Absolute download path

    Returns:
        int: Number of tasks created (number of downloads)
    """
    
    # Gathering files links
    thread_html = get_thread_data_from_web(thread_link)
    thread_soup = make_soup(thread_html, SELECTED_PARSER)
    list_of_thread_files_divs_html = get_all_divs_with_classname(thread_soup, DIV_CLASS_STD_NAME)
    links_from_threads_files = get_file_links_from_thread_divs(list_of_thread_files_divs_html, **filters)
    
    asyncio.run(download_tasks(download_path, links_from_threads_files))
        
    return len(links_from_threads_files)
    