import os
import sys
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))
sys.path.append(os.path.abspath('tests'))

from plugin_pet_ozzy import PetOzzy
from injectables.discord_dependencies import *

class TestPetOzzy(unittest.TestCase):
	obj = PetOzzy()

	def test_check_bits(self):
		assert self.obj.checkBits(0) == False

	def test_check_cat_true(self):
		assert self.obj.checkCat('admin') == True

	def test_check_cat_false(self):
		assert self.obj.checkCat('arrow') == False

class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
	obj = PetOzzy()
	
	a_channel = channel()
	a_message = message('!petozzy', a_channel)
	a_plugin = plugin('!help', 'help menu', '!help')

	obj_list = [a_plugin]

	async def test_run_cheer(self):
		assert await self.obj.runCheer('potato', 0) == True

	async def test_run_twice(self):
		print('discord_user: ' + str(self.a_message.author))
		assert await self.obj.run(self.a_message, self.obj_list) == True
		assert await self.obj.run(self.a_message, self.obj_list) == True

	async def test_stop(self):
		await self.obj.stop('potato')

if __name__ == '__main__':
	unittest.main()