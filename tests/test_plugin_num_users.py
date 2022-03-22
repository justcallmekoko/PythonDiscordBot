import os
import sys
#import pytest
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))
sys.path.append(os.path.abspath('tests'))

from plugin_numusers import Numusers
from injectables.discord_dependencies import *

class TestNumusers(unittest.TestCase):
	numusers = Numusers()

	def test_check_bits(self):
		assert self.numusers.checkBits(0) == False

	def test_check_cat_true(self):
		assert self.numusers.checkCat('admin') == True

	def test_check_cat_false(self):
		assert self.numusers.checkCat('arrow') == False

class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
	numusers = Numusers()

	async def test_run_cheer(self):
		assert await self.numusers.runCheer('potato', 0) == True

	async def test_run(self):
		a_channel = channel()
		a_message = message('!numusers', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')

		obj_list = [a_plugin]

		assert await self.numusers.run(a_message, obj_list) == True

	async def test_stop(self):
		await self.numusers.stop('potato')

if __name__ == '__main__':
	unittest.main()