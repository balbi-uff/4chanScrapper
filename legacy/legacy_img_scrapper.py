import requests
import lxml
import os
from bs4 import BeautifulSoup as make_soup
from time import time as timer


#                                   ██╗     ███████╗ ██████╗  █████╗  ██████╗██╗   ██╗
#                                   ██║     ██╔════╝██╔════╝ ██╔══██╗██╔════╝╚██╗ ██╔╝
#                                   ██║     █████╗  ██║  ███╗███████║██║      ╚████╔╝ 
#                                   ██║     ██╔══╝  ██║   ██║██╔══██║██║       ╚██╔╝  
#                                   ███████╗███████╗╚██████╔╝██║  ██║╚██████╗   ██║   
#                                   ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═╝   
                                                  





"""Scrapes every image from a thread, this is a legacy file with stuff I don't want to delete. I'll keep it for now, but I'll delete it later"""

# globals 
thread_name = None
acceptedFormats = ['webm', '.mp4', '.mp3', '.mov']
STD_PATH = "."


def getThreadName(soup):
    def prettify_name(n):
        final = "THREAD-"
        for i in n:
            if i == " ":
                break
            else:
                final += i
        return final

    name = soup.find('blockquote', class_='postMessage').text
    #print('debug >> THREADname=' + name)
    return prettify_name(name)


def get_filename(link):
    filename = ""
    tempLetter = ""
    while not tempLetter in ["\\", "/"]:
        tempLetter = link[-1]
        filename = tempLetter + filename
        link = link[:len(link) - 1]
    #print(f'debug >>> filename defined as {filename}')
    return filename[1:]


def download(file_link, path=STD_PATH): # download function
    
    f = requests.get(file_link).content
    #print('debug > Downloading...')
    with open(get_filename(file_link), 'wb') as tempDownload:
        #print('debug > checking if is image')
        if not get_filename(file_link)[-4:] in acceptedFormats:  # untested
            tempDownload.write(f)
    #print(f'debug >>> {get_filename(file_link)} downloaded!')
    return None


def request_link():
    link = input("Insert thread full link:")
    if "https://boards.4chan.org" not in link:
        raise (NotImplementedError)  

    #print('debug >>> main_link loaded!')
    return link


def get_links(main_link):
    """Gets links from images in page"""
    global thread_name

    def get_div_link(d):
        div_soup = make_soup(d, 'lxml')
        return div_soup.find('a')['href']

    raw = requests.get(main_link).content

    #print("debug > content downloaded!")

    soup = make_soup(raw, 'lxml')

    #print("debug > soup made!")

    thread_name = getThreadName(soup)

    links = []
    raw_divs = list(map(str, soup.findAll('div', class_='fileText')))

    #print("debug > raw divs fetched!")

    for div in raw_divs:
        links.append(get_div_link(div))

    #print("debug >>> links fetched!")

    return links


def download_images(img_links):
    global thread_name
    #print("debug >> thread_name=" + thread_name)
    path = STD_PATH
    if path == '' or len(path) == 0: #resolve this!! its wrong
        os.chdir(path)
        
        path = os.getcwd()
    
    os.chdir(path)
    os.mkdir(f"SYNC-{thread_name}")
    os.chdir(f"SYNC-{thread_name}")
    
    for img_link in img_links:
        #print(f"Downloading from {img_link}")
        download('http:' + img_link, path)
    return None


def app():
    download_images(get_links(request_link()))
    return None


def multiple_downloads():
    to_download = []

    
    try:
        actual_link = input("Please insert thread link to download (-1 to revoke):")

        if "https://boards.4chan.org" not in actual_link: raise (NameError)

        to_download.append(actual_link)
    except Exception as error_name:
        print(f"This happened => {error_name}")
        print("Try again!")

    for link in to_download:
        download_images(get_links(link))



def test_function(link):
    download_images(get_links(link))

def sync_main(link):
    start = timer()
    test_function(link)
    end = timer()
    return end-start

# developed by Andre Balbi - DerKatze789 - balbi-uff
# Fluminense Federal University - Rio de Janeiro - Brazil
