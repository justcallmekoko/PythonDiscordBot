import os
import sys
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))
sys.path.append(os.path.abspath('tests'))

from plugin_ozzy_stats import OzzyStats
from injectables.discord_dependencies import *

class TestOzzyStats(unittest.TestCase):
	obj = OzzyStats()
	def test_check_bits(self):
		assert self.obj.checkBits(0) == False

	def test_check_cat_true(self):
		assert self.obj.checkCat('admin') == True

	def test_check_cat_false(self):
		assert self.obj.checkCat('arrow') == False

class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
	obj = OzzyStats()

	async def test_run_cheer(self):
		assert await self.obj.runCheer('potato', 0) == True

	async def test_run_file_not_exist(self):
		a_channel = channel()
		a_message = message('!ozzystats', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')

		if os.path.isfile('ozzystats.json'):
			os.remove('ozzystats.json')

		obj_list = [a_plugin]

		assert await self.obj.run(a_message, obj_list) == True

		if os.path.isfile('ozzystats.json'):
			os.remove('ozzystats.json')

	async def test_stop(self):
		await self.obj.stop('potato')

if __name__ == '__main__':
	unittest.main()