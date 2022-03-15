import os
import sys
#import pytest
import asyncio
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))

from plugin_help import Help

class plugin():
	name = None
	desc = None
	synt = None

	def __init__(self, name, desc, synt):
		self.name = name
		self.desc = desc
		self.synt = synt

class message():
	content = None
	channel = None
	embed = None

	def __init__(self, content, channel):
			self.content = content
			self.channel = channel
			channel = None

class channel():
	def __init__(self):
		return

	async def send(self, content=None, embed=None):
		return True

class TestHelp(unittest.TestCase):

	def test_check_bits(self):
		help = Help()
		assert help.checkBits(0) == False

	def test_check_cat_true(self):
		help = Help()
		assert help.checkCat('admin') == True

	def test_check_cat_false(self):
		help = Help()
		assert help.checkCat('arrow') == False


class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
	async def test_run_cheer(self):
		help = Help()
		assert await help.runCheer('potato', 0) == True

	async def test_run_help(self):
		help = Help()
		a_channel = channel()
		a_message = message('!help', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')

		print('message content: ' + str(a_message.content))

		obj_list = [a_plugin]

		await help.run(a_message, obj_list)

'''
@pytest.mark.asyncio
async def test_stop():
	help = Help()
	await help.stop('potato')

@pytest.mark.asyncio
async def test_run_help():
	help = Help()
	a_channel = channel()
	a_message = message('!help', a_channel)
	a_plugin = plugin('!help', 'help menu', '!help')

	print('message content: ' + str(a_message.content))

	obj_list = [a_plugin]

	await help.run(a_message, obj_list)

@pytest.mark.asyncio
async def test_run_help_command():
	help = Help()
	a_channel = channel()
	a_message = message('!help !command', a_channel)
	a_plugin = plugin('!command', 'Random Command', '!command')

	print('message content: ' + str(a_message.content))

	obj_list = [a_plugin]

	await help.run(a_message, obj_list)
'''

if __name__ == '__main__':
	unittest.main()