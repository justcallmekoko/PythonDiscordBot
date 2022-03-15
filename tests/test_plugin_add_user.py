import os
import sys
#import pytest
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))

from plugin_add_user import AddUser

class TestAddUser(unittest.TestCase):
    	
	def test_check_bits(self):
		user = AddUser()
		assert user.checkBits(0) == False

	def test_check_cat_true(self):
		user = AddUser()
		assert user.checkCat('admin') == True

	def test_check_cat_false(self):
		user = AddUser()
		assert user.checkCat('arrow') == False

if __name__ == '__main__':
	unittest.main()