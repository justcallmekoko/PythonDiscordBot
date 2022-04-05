import os
import sys
import asyncio
#import pytest
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))

from plugin_auto_role import AutoRole

class TestAutoRole(unittest.TestCase):

	def test_check_bits(self):
		autorole = AutoRole()
		autorole.startService()
		assert autorole.checkBits(0) == False

	def test_check_cat_true(self):
		autorole = AutoRole()
		autorole.startService()
		assert autorole.checkCat('admin') == True

	def test_check_cat_false(self):
		autorole = AutoRole()
		autorole.startService()
		assert autorole.checkCat('arrow') == False

if __name__ == '__main__':
	unittest.main()