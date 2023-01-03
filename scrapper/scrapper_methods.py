import requests
import os
import asyncio
from bs4 import BeautifulSoup as make_soup
from time import time as timer

"""Scrapes every image from a thread, according to your specifications."""

# global vars
DIV_CLASS_STD_NAME = 'fileText'
THREAD_CLASS_STD_NAME = 'subject'
SELECTED_PARSER = 'lxml'
HTTP_PROTOCOL_SYMBOL = 'http'
NUM_IMG_STD_SPAN_CLASS = 'ts-images'
STD_PATH_DOWNLOAD = "."

# global configs
acceptedFormats = ['webm', '.mp4', '.mp3', '.mov']  # get from txt file
thread_name = None
number_of_ended_tasks = 0
number_of_links_to_download = 0


def download(file_link):
    """
    Download single image from link.
    """
    global number_of_ended_tasks, number_of_links_to_download

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
        if not file_is_valid(filename):  # rejects non-declared types of files
            tempDownload.write(file_data)
    number_of_ended_tasks += 1

    print(f"{number_of_ended_tasks} of {number_of_links_to_download} downloaded!")


async def download_image_task(img_link):
    """
    Creates the task of downloading a single image.
    Args:
        img_link: Link of the image, the standart is a internal link without the protocol included.

    Returns:

    """
    link = HTTP_PROTOCOL_SYMBOL + ":" + img_link
    print(f"Downloading {link}")
    download(link)


def get_thread_data_from_web(thread_link):
    return requests.get(thread_link).content


def get_resolution_from_div_text(text):
    """
    Gets resolution from div text.
    Used "File: filename.jpg(491 KB, 1164x705)" as example.
    Args:
        text: Text from div.

    Returns: Resolution as tuple.
    """
    resolution = text[:-1].strip().split(",")[-1]
    x_res, y_res = resolution.split("x")
    return int(x_res), int(y_res)


def get_file_links_from_thread_divs(list_of_divs, **filters):
    def check_minimum_resolution(img_x, img_y, min_x, min_y):
        if min_x:
            x_validation = img_x >= min_x
        else:
            x_validation = True
        if min_y:
            y_validation = img_y >= min_y
        else:
            y_validation = True

        return x_validation and y_validation

    def check_maximum_resolution(img_x, img_y, max_x, max_y):
        if max_x:
            x_validation = img_x <= max_x
        else:
            x_validation = True
        if max_y:
            y_validation = img_y <= max_y
        else:
            y_validation = True

        return x_validation and y_validation

    def check_resolution(img_x, img_y, min_x, min_y, max_x, max_y):
        # VALIDATE AS NONE IS ENTERING MIN AND MAX VARS
        return check_minimum_resolution(img_x, img_y, min_x, min_y) and check_maximum_resolution(img_x, img_y, max_x,
                                                                                                 max_y)

    def get_div_link(image_raw_div, **filters):
        div_soup = make_soup(image_raw_div, SELECTED_PARSER)
        div_link = div_soup.find('a')['href']
        if filters.values():
            x_resolution, y_resolution = get_resolution_from_div_text(div_soup.text)
            if not check_resolution(x_resolution, y_resolution, *filters.values()):
                div_link = None
        return div_link

    # filter this after primary tests
    file_links = [get_div_link(div_html, **filters) for div_html in list_of_divs]
    #

    return [link for link in file_links if type(link) is str]


def get_all_divs_with_class_name(soup, class_name):
    return list(map(str, soup.findAll('div', class_=class_name)))


def get_thread_name(soup):
    """
    Simple function that gets thread name directly from soup.
    """

    return soup.find('span', class_=THREAD_CLASS_STD_NAME).text


async def download_tasks(download_path, links_from_threads_files):
    # Organizing download tasks
    thread_download_tasks = []

    os.chdir(download_path)

    for file_link in links_from_threads_files:
        task_name = file_link[-17:]
        thread_download_tasks.append(asyncio.create_task(download_image_task(file_link), name=task_name))

    await asyncio.gather(*thread_download_tasks)


def get_html_file_as_string(file_path):
    """
    Returns html content as string.
    Args:
        file_path: File path.

    Returns: HTML file converted as string.
    """
    with open(file_path, "r") as html_file:
        return html_file.read()


def get_thread_data(thread_link):
    if "boards.4chan.org" in thread_link:
        return get_thread_data_from_web(thread_link)
    else:
        return get_html_file_as_string(thread_link)


def has_empty_arguments(t, d):
    return '' in [t, d]


def create_local_download_path(new_dir_name):
    """
    Creates a local download path.
    Args:
        new_dir_name: Thread name for new dir.

    Returns: Path as string.
    """
    return f"{STD_PATH_DOWNLOAD}/{new_dir_name}"


def download_files_from_thread(thread_link, download_path, **filters):
    """Download files from inputted thread.

    Args:
        thread_link (str): Thread link.
        download_path (str): Absolute download path

    Returns:
        int: Number of tasks created (number of downloads)
    """
    global number_of_links_to_download

    # Analyse arguments
    if has_empty_arguments(thread_link, download_path):
        raise Exception("Invalid number of arguments. Please, pass at least 2 arguments")

    # Gathering files links
    thread_html = get_thread_data(thread_link)
    thread_soup = make_soup(thread_html, SELECTED_PARSER)
    thread_name_ = get_thread_name(thread_soup)
    if not download_path:
        create_local_download_path(thread_name_)
    list_of_thread_files_divs_html = get_all_divs_with_class_name(thread_soup, DIV_CLASS_STD_NAME)
    links_from_threads_files = get_file_links_from_thread_divs(list_of_thread_files_divs_html, **filters)
    number_of_links_to_download = len(links_from_threads_files)

    asyncio.run(download_tasks(download_path, links_from_threads_files))

    return number_of_links_to_download
