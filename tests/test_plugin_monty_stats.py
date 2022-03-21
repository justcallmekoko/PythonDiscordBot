import os
import sys
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))
sys.path.append(os.path.abspath('tests'))

from plugin_monty_stats import MontyStats
from injectables.discord_dependencies import *

class TestTemplate(unittest.TestCase):

	def test_check_bits(self):
		monty = MontyStats()
		assert monty.checkBits(0) == False

	def test_check_cat_true(self):
		monty = MontyStats()
		assert monty.checkCat('admin') == True

	def test_check_cat_false(self):
		monty = MontyStats()
		assert monty.checkCat('arrow') == False

class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
	async def test_run_cheer(self):
		monty = MontyStats()
		assert await monty.runCheer('potato', 0) == True

	async def test_run_file_not_exist(self):
		a_channel = channel()
		a_message = message('!montystats', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')

		if os.path.isfile('montystats.json'):
			os.remove('montystats.json')

		obj_list = [a_plugin]

		monty = MontyStats()
		assert await monty.run(a_message, obj_list) == True

		if os.path.isfile('montystats.json'):
			os.remove('montystats.json')

	async def test_stop(self):
		monty = MontyStats()
		await monty.stop('potato')

if __name__ == '__main__':
	unittest.main()