NOT WORKING - FUCKING BS4 TROLLED ME
import requests 
import lxml
import os
from bs4 import BeautifulSoup as make_soup

def DNU_write_new_file(filename, content):
	with open(filename, 'w', encoding='utf-8') as file:
		file.write(content)
	return None

def debug(level, message):
	s = '>' * level
	print(f'debug {s} {message}')

	return None

def choose_board():
	decided = False
	boards = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'gif', 'h', 'hr', 'k', 'm', 'o', 'p', 'r', 's', 't', 'u', 'v', 'vg', 'vmg', 'vr', 'vrpg', 'vst', 'w', 'wg', 'i', 'ic', 'r9k', 's4s', 'vip', 'qa', 'cm', 'hm', 'lgbt', 'y', '3', 'aco', 'adv', 'an', 'asp', 'bant', 'biz', 'cgl', 'ck', 'co', 'diy', 'fa', 'fit', 'gd', 'hc', 'his', 'int', 'jp', 'lit', 'mlp', 'mu', 'n', 'news', 'out', 'po', 'pol', 'qst', 'sci', 'soc', 'sp', 'tg', 'toy', 'trv', 'tv', 'vp', 'wsg', 'wsr', 'x']
	while not decided: #I did this way to be intuitive. I DONT FUCKING CARE IF IT'S NOT PYTHONIC.
		boardName = input("Insert board's name: ")
		if boardName in boards:
			debug(1, 'changed decided condition!')
			chosen = boardName
			decided = True
		else:
			print("This board does not exist, try again.")
	return chosen

def fetch_info(t):
	debug(1, 'making div soup!')
	infos = {}
	thread_soup = make_soup(t, 'lxml')
	infos['title'] = thread_soup.find('b').text
	infos['subtitle'] = thread_soup.find('div', class_='teaser')
	infos['r/i'] = thread_soup.find('div', class_= 'meta').text       #NEEDS TESTING
	infos['link'] = thread_soup.find('a')['href']
	debug(3, 'printing values')
	for key in infos.keys:
		print(f'{key}:\n{infos[key]}')
	return None


def show_catalog_options(board='wg'):
	std_url = "https://boards.4chan.org/" + board + "/catalog"
	# print(std_url)
	debug(1, 'fetching catalog content')
	raw = requests.get(std_url).content
	
	

	debug(1, 'making soup w/ lxml')
	soup = make_soup(raw, 'lxml')

	# debug(2, 'making testfile.html')
	# DNU_write_new_file('testfile.html', str(grandfather.prettify))

	grandfather = soup.findAll('div', {"id": "content"}, recursive=True)
	print(grandfather)
	for child in grandfather:
		grandchildren = child.findChildren("div", recursive=True)
		print(grandchildren)
		# child_nodes = child.descendants
		# for c in child_nodes:
		# 	if c.name == 'div' and c.get('id') == 'threads':
		# 		pass



	# father = grandfather.find('div', {"id": "threads"})
	# children = list(map(str, father.findAll('div', class_="thread")))

	# print(f'Found {len(children)}!')
	# # [print(x) for x in children]

	# debug(3, 'processing options!')
	# for thr in children:
	# 	# debug(1, 'fetching thread info - initialized')
	# 	fetch_info(thr)
	# 	# debug(3, 'fetching thread info - DONE!')
	
	return None

def app():
	show_catalog_options()
	return None

app()


print('ENDED - ENDED')