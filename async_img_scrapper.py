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
STD_REQUEST_PROTOCOL = 'http'

## other globals
acceptedFormats = ['webm', '.mp4', '.mp3', '.mov']
thread_name = None
ended_tasks = 0
number_of_tasks = 0


def getThreadName(soup):
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


def get_links(main_link):
    """
    Gets links from images in page
    """
    global thread_name
    
    # Constants

    def get_div_link(d):
        div_soup = make_soup(d, SELECTED_PARSER)
        return div_soup.find('a')['href']

    links = []
    raw_content = requests.get(main_link).content
    soup = make_soup(raw_content, SELECTED_PARSER)
    thread_name = getThreadName(soup)
    
    raw_divs = list(map(str, soup.findAll('div', class_=DIV_CLASS_STD_NAME)))
    
    for div in raw_divs:
        links.append(get_div_link(div))
    return links


async def download_image_task(img_link):
    """
    Function responsible for creating the task of downloading a single image.
    """
    await download(STD_REQUEST_PROTOCOL + ":" + img_link)
    

def download_images(img_links, path, create_folder):
    """
    Main function responsible for downloading images from a thread.
    """
    global thread_name
    tasks = []
    
    loop = asyncio.get_event_loop()
    
    os.chdir(path)
    
    if create_folder:
        os.mkdir(f"{thread_name}")
        os.chdir(f"{thread_name}")

    for img_link in img_links:
        tasks.append(loop.create_task(download_image_task(img_link)))
        
    
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    return None

def async_downloader(link, path, create_folder):
    """
    Function responsible for creating the task of downloading a thread.
    """
    global number_of_tasks

    images_links = get_links(link)
    number_of_tasks = len(images_links)
    download_images(images_links, path, create_folder)

def async_main(link, path, create_folder=False):
    """
     Times the time it takes to download.
    """
    start = timer()
    async_downloader(link, path, create_folder)
    end = timer()
    return end-start

# testing-related
if __name__ == "__main__":
    thread_code = '7820596'
    async_main("https://boards.4chan.org/wg/thread/" + thread_code, "C:\\Users\\balbi\\Desktop\\", True)


# developed by Andre Balbi - DerKatze789 - balbi-uff
# Fluminense Federal University - Rio de Janeiro - Brazil