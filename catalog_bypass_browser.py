#this program could be 10X faster, literally. 
#look at this shit
import requests 
import lxml
import os
from bs4 import BeautifulSoup as make_soup

def pull_infos(threads_list):
	gathered = dict() #this will be a dict of dicts
	for thread in threads_list:
		thread_info = {}
		title = thread.find('span', {'class' : 'subject'})
		link = thread.find('a', {'class' : 'replylink'})['href']
		#size =  #replies and images
		NOT DONE 
		print(thread_info)
	return gathered


def check_avaible_threads(fchanlink):

	raw = requests.get(fchanlink).content
	soup = make_soup(raw, 'lxml')
	threads = soup.findAll('div', class_='thread')
	infos = pull_infos(threads)

	return infos
	



#test
check_avaible_threads('https://boards.4chan.org/pol/')