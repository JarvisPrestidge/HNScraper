#!/usr/bin/env python

__author__ = 'Yash Lakhani'
__email__ = 'yashlakhani13@gmail.com'

"""

Unit Testing for Hacker News Scraper 
Developed for TrueLayer

"""

import unittest
from hnScraper import find_valid_number, valid_string, valid_uri

###############################################################################
# Classes 
###############################################################################
class TestValidationMethods(unittest.TestCase):
	"""
	This class will perform unit testing on validation methods
	"""
	def test_number_validation(self):	
		self.assertEqual(find_valid_number(''), 0)
		self.assertEqual(find_valid_number('no_numbers'), 0)
		self.assertEqual(find_valid_number('8 is a digit'), 8)
		self.assertEqual(find_valid_number('13 is before 14'), 13)

	def test_string_validation(self):
		self.assertEqual(valid_string(""), False)	
		self.assertEqual(valid_string(300*'s'), False)
		#Edge Case 1:
		self.assertEqual(valid_string(256*'s'), True)
		#Edge Case 2:
		self.assertEqual(valid_string('s'), True)
	
	def test_uri_validation(self):
		self.assertEqual(valid_uri('http://www.google.com'), True)
		self.assertEqual(valid_uri('http://'), False)
		self.assertEqual(valid_uri('?=29105'), False)

###############################################################################
# Global 
###############################################################################
if __name__ == '__main__':
    unittest.main()
