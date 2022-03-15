import os
import sys
#import pytest
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))

from plugin_giveaway import Giveaway

class TestGiveaway(unittest.TestCase):

	def test_check_bits(self):
		giveaway = Giveaway()
		assert giveaway.checkBits(0) == False

	def test_check_cat_true(self):
		giveaway = Giveaway()
		assert giveaway.checkCat('admin') == True

	def test_check_cat_false(self):
		giveaway = Giveaway()
		assert giveaway.checkCat('arrow') == False

if __name__ == '__main__':
	unittest.main()