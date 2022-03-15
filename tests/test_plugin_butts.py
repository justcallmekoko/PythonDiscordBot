import os
import sys
import pytest
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))

from plugin_butts import Butts

class TestButts(unittest.TestCase):

	def test_check_bits(self):
		butt = Butts()
		assert butt.checkBits(0) == False

	def test_check_cat_true(self):
		butt = Butts()
		assert butt.checkCat('admin') == True

	def test_check_cat_false(self):
		butt = Butts()
		assert butt.checkCat('arrow') == False

if __name__ == '__main__':
	unittest.main()