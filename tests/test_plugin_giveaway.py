import os
import sys
#import pytest
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))
sys.path.append(os.path.abspath('tests'))

from plugin_giveaway import Giveaway
from injectables.discord_dependencies import *

class TestGiveaway(unittest.TestCase):

	def test_check_bits(self):
		giveaway = Giveaway()
		assert giveaway.checkBits(0) == False

	def test_check_cat_true(self):
		giveaway = Giveaway()
		assert giveaway.checkCat('admin') == True

	def test_check_cat_false(self):
		giveaway = Giveaway()
		assert giveaway.checkCat('arrow') == False

class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
	async def test_run_cheer(self):
		giveaway = Giveaway()
		assert await giveaway.runCheer('potato', 0) == True

	async def test_run_no_giveaways(self):
		giveaway = Giveaway()
		a_channel = channel()

		a_message = message('!giveaway', a_channel)

		a_plugin = plugin('!giveaway', 'Giveaway', '!giveaway <name>')

		#a_message.content = '!adduser ' + str(a_message.author.name)
		#role = Role('Restricted')
		#a_message.author.roles.append(role)

		print('message content: ' + str(a_message.content))

		obj_list = [a_plugin]

		assert await giveaway.run(a_message, obj_list) == True

	async def test_fail_post_channel(self):
		giveaway = Giveaway()
		a_channel = channel()

		giveaway_name = 'This is a test giveaway'

		a_message = message('!giveaway start ' + str(giveaway_name), a_channel)

		a_plugin = plugin('!giveaway', 'Giveaway', '!giveaway <name>')

		role = Role('Moderator')
		a_message.author.roles.append(role)

		print('message content: ' + str(a_message.content))

		obj_list = [a_plugin]

		a_channel.name = 'potato'

		a_message.guild.channels.append(a_channel)

		result = await giveaway.run(a_message, obj_list)

		self.assertEqual(result, False)

	async def test_start_giveaway(self):
		giveaway = Giveaway()
		a_channel = channel()

		giveaway_name = 'This is a test giveaway'

		a_message = message('!giveaway start ' + str(giveaway_name), a_channel)

		a_plugin = plugin('!giveaway', 'Giveaway', '!giveaway <name>')

		role = Role('Moderator')
		a_message.author.roles.append(role)

		print('message content: ' + str(a_message.content))

		obj_list = [a_plugin]

		a_channel.name = 'giveaways'

		a_message.guild.channels.append(a_channel)

		result = await giveaway.run(a_message, obj_list)

		self.assertEqual(result, giveaway_name)

	async def test_stop(self):
		giveaway = Giveaway()
		await giveaway.stop('potato')

if __name__ == '__main__':
	unittest.main()