#!/usr/bin/env python

__author__ = 'Yash Lakhani'
__email__ = 'yashlakhani13@gmail.com'

"""

Hacker News Scraper 
Developed for TrueLayer

"""

import argparse, requests, validators, json 
from math import ceil 
from lxml import html

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
			if num_posts > 100: 
				err_string = 'Please enter a number < 100'
				raise ValueError(err_string)
			else:
				self._num_posts = num_posts
				self._num_pages = int(ceil(num_posts
							/ self.PER_PAGE)) 
	
	def fetch_content(self):
		"""
		Method will iterate over url/pages and add 
		dictionary objects (stories) to an internal list 
		"""
		iter_num = 1  
		while(iter_num <= self._num_pages):
			url = "{}?p={}".format(self.BASEURL, iter_num)
			self.parse_stories(self, self.get_table(url))	
			iter_num += 1

	def json_print(self, indentation):
		"""
		Prints list of dictionary objects (stories) in JSON format 
		"""
		json_data = json.dumps(self.STORY_LIST, indent=indentation) 
		print json_data

	@staticmethod
	def get_table(url):
		""" 
		Static Method to Retrive HTML Table from URL
		"""
		response = requests.get(url, stream=True)
		if response.status_code != requests.codes.ok:
			response.raise_for_status()
		tree = html.fromstring(response.text)
		tables = tree.cssselect("table[class=itemlist]")
		
		if len(tables) != 1:
			err_string = 'Retrieved {} tables, expected 1'
			print err_string.format(len(tables))
			return
		
		return tables[0]

	@staticmethod
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

			story = self.validate_fields(self, story, 
						     points, comments)
			
			self.STORY_LIST.append(story) 

	check_for_digits = lambda self, x: [int(s) for s in x.split()
						   if s.isdigit()] 
	@staticmethod
	def validate_fields(self, story, points, comments) :	
		"""
		Validates data to meet requirements
		"""
		points = self.check_for_digits(points)
		comments = self.check_for_digits(comments) 

		points = points[0] if len(points) > 0 else 0 
		comments = comments[0] if len(comments) > 0 else 0 
		
		story['points'] , story['comments'] = points, comments 
		
		if len(story['title']) not in range(1,257):
			story['title'] = 'NA'
		
		if len(story['author']) not in range(1,257):
			story['author'] = 'NA'
		
		if not validators.url(story['uri']):
			story['uri'] = 'NA'

		return story 

###############################################################################
# Functions
###############################################################################
def parse_arguments():
	"""
	This function parses command line arguments 
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('--posts', '-p', metavar='n', type=int, 
			    default=100, help='number of posts')
	parser.add_argument('--ident', '-i', metavar='n', type=int, 
			    default=4, help='identation of JSON')
	args = parser.parse_args()
	return args.posts, args.ident

###############################################################################
# Main
###############################################################################
def main():
	NUM_POSTS, INDENT = parse_arguments()
	try:
		hnScraper = HNScraper(NUM_POSTS)
		hnScraper.fetch_content()
		hnScraper.json_print(indentation=INDENT)
	
	except ValueError as v:
		err_string = '{} \nMaximum Posts : 100 \nRequested : {}'
		err_string.format(v, NUM_POSTS) 				

if __name__ == "__main__":
	main()
