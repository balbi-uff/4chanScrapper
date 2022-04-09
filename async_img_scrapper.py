from venv import create
import requests
import lxml # do not delete this line, it is used for parsing
import os
import asyncio
from json.tool import main
from bs4 import BeautifulSoup as make_soup
from time import time as timer

"""Scrapes every image from a thread"""

# globals 

## constants
DIV_CLASS_STD_NAME = 'fileText'
THREAD_CLASS_STD_NAME = 'postMessage'
SELECTED_PARSER = 'lxml'
HTTP_PROTOCOL_SYMBOL = 'http'
NUM_IMG_STD_SPAN_CLASS = 'ts-images'
STD_PATH_DOWNLOAD = "C:\\Wallpapers\\"

## other globals
acceptedFormats = ['webm', '.mp4', '.mp3', '.mov']
thread_name = None
ended_tasks = 0
number_of_tasks = 0


def get_thread_name_automatically(soup):
    """
    Simple function that gets thread name directly from soup.
    """
    def prettify_thread_name(name):
        return name.title().replace(" ", "")[15:]

    thread_name = soup.find('blockquote', class_=THREAD_CLASS_STD_NAME).text
    return prettify_thread_name(thread_name)


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


def download(file_link):
    """
    Download single image from link.
    """
    f = requests.get(file_link).content
    global ended_tasks, number_of_tasks

    with open(get_filename(file_link), 'wb') as tempDownload:
        if not get_filename(file_link)[-4:] in acceptedFormats: # rejects non-declared types of files
            tempDownload.write(f)
    ended_tasks += 1

    # there must be a better way to do this, idk, got lazy and used global variables
    os.system("cls")
    print(f"{ended_tasks} of {number_of_tasks} downloaded.")


def get_links(main_link, manual_name, min_res_x, min_res_y, max_res_x, max_res_y):
    """
    Gets links from images in page
    """
    global thread_name
    
    # Constants

    def get_div_link(image_raw_div):
        div_soup = make_soup(image_raw_div, SELECTED_PARSER)
        
        return div_soup.find('a')['href']

    def get_image_resolution_raw_hard_coded(image_raw_div):
        div_soup = make_soup(image_raw_div, SELECTED_PARSER)
        
        return tuple(map(int, div_soup.text.split(",")[1].strip(")").split("x")))

    links = []
    raw_content = requests.get(main_link).content
    soup = make_soup(raw_content, SELECTED_PARSER)
    if not manual_name:
        thread_name = get_thread_name_automatically(soup)
    else:
        thread_name = manual_name
    
    
    raw_divs = list(map(str, soup.findAll('div', class_=DIV_CLASS_STD_NAME)))
    
    

    for raw_div_html in raw_divs:
        image_resolution = get_image_resolution_raw_hard_coded((raw_div_html))
        
        if min_res_x <= image_resolution[0] and min_res_y <= image_resolution[1]:
            if max_res_x >= image_resolution[0] and max_res_y >= image_resolution[1]:
                links.append(get_div_link(raw_div_html))

    return links


async def download_image_task(img_link):
    """
    Function responsible for creating the task of downloading a single image.
    """
    print()
    link = HTTP_PROTOCOL_SYMBOL + ":" + img_link
    await download(link)
    

def download_images(img_links, path, forced_name):
    """
    Main function responsible for downloading images from a thread.
    """

    global thread_name
    tasks = []
    loop = asyncio.get_event_loop()
    os.chdir(path)
    if forced_name and not (os.path.exists(thread_name)):
        thread_name = forced_name

        os.mkdir(f"{thread_name}")
        os.chdir(f"{thread_name}")

    for img_link in img_links:
        tasks.append(loop.create_task(download_image_task(img_link), name=img_link[-17:]))
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()


def async_downloader(link, path, forced_name, min_res_x, min_res_y, max_res_x, max_res_y):
    """
    Function responsible for creating the task of downloading a thread.
    """
    global number_of_tasks

    images_links = get_links(link, forced_name, min_res_x, min_res_y, max_res_x, max_res_y)
    number_of_tasks = len(images_links)
    try:
        download_images(images_links, path, forced_name)
    except TypeError as e:
        print(f"I AM A BUG AND I STILL EXIST, THERE IS NO ONE WHO CAN EXTINGUISH ME, PLEASE KILL ME!\nDescription:{e}")
    return number_of_tasks

def async_main(link, path, forced_name, min_res_x, min_res_y, max_res_x, max_res_y):
    """
     Times the time it takes to download.
    """
    start = timer()
    if not path:
        path = STD_PATH_DOWNLOAD
    async_downloader(link, path, forced_name, min_res_x, min_res_y, max_res_x, max_res_y)
    end = timer()
    return end-start


# developed by Andre Balbi - DerKatze789 - balbi-uff
# Fluminense Federal University - Rio de Janeiro - Brazil