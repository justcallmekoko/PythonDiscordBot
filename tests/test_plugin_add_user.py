import os
import sys
#import pytest
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))
sys.path.append(os.path.abspath('tests'))

from plugin_add_user import AddUser
from injectables.discord_dependencies import *

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


class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
	async def test_run_cheer(self):
		user = AddUser()
		assert await user.runCheer('potato', 0) == True

	async def test_run_restricted(self):
		user = AddUser()
		a_channel = channel()

		a_message = message('!adduser', a_channel)

		a_plugin = plugin('!adduser', 'Add user', '!adduser <name>')

		a_message.content = '!adduser ' + str(a_message.author.name)
		role = Role('Restricted')
		a_message.author.roles.append(role)

		print('message content: ' + str(a_message.content))

		obj_list = [a_plugin]

		assert await user.run(a_message, obj_list) == True

	async def test_run_missing_role(self):
		user = AddUser()
		a_channel = channel()

		a_message = message('!adduser', a_channel)

		a_plugin = plugin('!adduser', 'Add user', '!adduser <name>')

		a_message.content = '!adduser ' + str(a_message.author.name)
		role = Role('member')
		a_message.author.roles.append(role)

		obj_list = [a_plugin]

		assert await user.run(a_message, obj_list) == True

if __name__ == '__main__':
	unittest.main()