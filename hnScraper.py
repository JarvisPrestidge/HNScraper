#!/usr/bin/env python

__author__ = 'Yash Lakhani'
__email__ = 'yashlakhani13@gmail.com'

"""

Hacker News Scraper 
Developed for TrueLayer

"""

import argparse, requests, validators, json 
from multiprocessing import Pool 
from math import ceil 
from lxml import html

MAX_POSTS = 200 
MAX_PROCS = 20 
MAX_INDENT = 10 

###############################################################################
# Classes 
###############################################################################
class HNScraper:
	""" 
	This class scrapes the HackerNews page and builds up stories
	"""	
	BASEURL =  "https://news.ycombinator.com/news"
	PER_PAGE = 30.0
	STORY_COUNT = 0 
	STORY_LIST = []

	def __init__(self, num_posts):
		self._num_posts = num_posts
		self._num_pages = int(ceil(num_posts
					/ self.PER_PAGE))

	def fetch_content(self, num_procs):
		"""
		Method will iterate over url/pages and add 
		dictionary objects (stories) to an internal list 
		"""
		urls = []
		iter_num = 1  
		while(iter_num <= self._num_pages):
			url = "{}?p={}".format(self.BASEURL, iter_num)
			if num_procs:
				urls.append(url)
			else:
				table = get_html_table(get_request(url)) 
				self.parse_stories(table)	
			iter_num += 1

		if num_procs:
			p = Pool(num_procs)
			results = p.map(get_request, urls) 
			map(self.parse_stories,
				 map(get_html_table, results))
	
	def parse_stories(self, table):	
		"""
		Given a HTML Table, the relevant data will be parsed
		"""
		for top, btm in zip(table.cssselect('tr[class=athing]'), 
				    table.cssselect('td[class=subtext]')):
			
			self.STORY_COUNT += 1
			if self.STORY_COUNT > self._num_posts: return 
			
			links = top.cssselect('a[class=storylink]')	
			href = links[0].attrib['href']
			title = links[0].text_content().strip()
			
			sub_links = btm.cssselect('a')
			user, comments = (sub_links[0].text_content(),
					  sub_links[-1].text_content())
			points = btm.cssselect('span')[0].text_content()
							
			story = {
				'title' : title, 
				'uri' : href,
				'author' : user, 
				'rank' : self.STORY_COUNT	
				}

			story = validate_fields(story, points, comments)
			
			self.STORY_LIST.append(story) 
	
	def json_print(self, indentation):
		"""
		Prints list of dictionary objects (stories) in JSON format 
		"""
		json_data = json.dumps(self.STORY_LIST, indent=indentation) 
		print json_data

###############################################################################
# Functions
###############################################################################
def get_request(url):	
	"""
	Returns Response When Given a URL Request  
	"""
	response = requests.get(url, stream=True)
	if response.status_code != requests.codes.ok:
		response.raise_for_status()
	return response 

def get_html_table(response):
	""" 
	Method to Retrive HTML Table from Response 
	"""
	tree = html.fromstring(response.text)
	tables = tree.cssselect("table[class=itemlist]")
	
	if len(tables) != 1:
		err_string = 'Retrieved {} tables, expected 1'
		print err_string.format(len(tables))
		return
	
	return tables[0]

def find_valid_number(input):
	"""
	Method will find numbers from scraped data
	append to list and select the first valid 
	"""
	numbers = [int(s) for s in input.split()
				if s.isdigit()]
	
	return numbers[0] if len(numbers) > 0 else 0 

valid_string = lambda x: True if len(x) in range(1,257) else False 

valid_uri = lambda x: True if validators.url(x) else False

def validate_fields(story, points, comments) :	
	"""
	Validates data to meet requirements
	"""
	story['points'] = find_valid_number(points)
	story['comments'] = find_valid_number(comments)
	
	if not valid_string(story['title']):
		story['title'] = 'NA'

	if not valid_string(story['author']):
		story['author'] = 'NA'
	
	if not valid_uri(story['uri']): 
		story['uri'] = 'NA'

	return story 

def parse_arguments():
	"""
	This function parses command line arguments 
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('--posts', '-p', metavar='n', type=int, 
			    default=100, help='number of posts')
	parser.add_argument('--multi', '-m', metavar='n', type=int, 
			    default=0, help='number of processes')	
	parser.add_argument('--indent', '-i', metavar='n', type=int, 
			    default=4, help='identation of JSON')
	args = parser.parse_args()

	if args.posts > MAX_POSTS:	
		err_string = "Number of Posts Must Be < {}"
		raise argparse.ArgumentTypeError(err_string.format(MAX_POSTS))
	if args.multi > MAX_PROCS: 	
		err_string = "Number of Processes Must Be < {}"
		raise argparse.ArgumentTypeError(err_string.format(MAX_PROCS))
	if args.indent > MAX_INDENT: 
		err_string = "Indentation Level Must Be < {}"
		raise argparse.ArgumentTypeError(err_string.format(MAX_INDENT))

	return args.posts, args.multi, args.indent

###############################################################################
# Main
###############################################################################
def main():
	try:
		NUM_POSTS, NUM_PROCS, INDENT = parse_arguments()
		
		hnScraper = HNScraper(NUM_POSTS)
		hnScraper.fetch_content(NUM_PROCS)
		hnScraper.json_print(indentation=INDENT)
	
	except ValueError as ex:
		err_string = 'Maximum Argument Exceeded \n{}'
		print err_string.format(ex) 				

###############################################################################
# Global 
###############################################################################
if __name__ == "__main__":
	main()
