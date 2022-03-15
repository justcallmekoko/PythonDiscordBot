import os
import sys
#import pytest
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))
sys.path.append(os.path.abspath('tests'))

from plugin_butts import Butts
from injectables.discord_dependencies import *

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

class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
	async def test_run_cheer(self):
		butt = Butts()
		assert await butt.runCheer('potato', 0) == True

	async def test_run(self):
		butt = Butts()
		a_channel = channel()
		a_message = message('!help', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')

		obj_list = [a_plugin]
		
		assert await butt.run(a_message, obj_list)

	async def test_stop(self):
		butt = Butts()
		await butt.stop('potato')

if __name__ == '__main__':
	unittest.main()