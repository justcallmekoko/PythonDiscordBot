import os
import sys
#import pytest
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))

from plugin_template import Template

class TestTemplate(unittest.TestCase):

	def test_check_bits(self):
		template = Template()
		assert template.checkBits(0) == False

	def test_check_cat_true(self):
		template = Template()
		assert template.checkCat('admin') == True

	def test_check_cat_false(self):
		template = Template()
		assert template.checkCat('arrow') == False

if __name__ == '__main__':
	unittest.main()