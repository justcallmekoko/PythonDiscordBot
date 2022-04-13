import os
import sys
import discord
import unittest
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath('plugins'))
sys.path.append(os.path.abspath('tests'))

from plugin_poll import Poll
from injectables.discord_dependencies import *

class TestPoll(unittest.TestCase):
	obj = Poll()

	def test_check_bits(self):
		assert self.obj.checkBits(0) == False

	def test_check_cat_true(self):
		assert self.obj.checkCat('admin') == True

	def test_check_cat_false(self):
		assert self.obj.checkCat('arrow') == False

class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
	obj = Poll()
	
	#a_channel = channel()
	#a_message = message('!help', a_channel)
	#a_plugin = plugin('!help', 'help menu', '!help')

	#obj_list = [a_plugin]

	async def test_run_cheer(self):
		assert await self.obj.runCheer('potato', 0) == True

	async def test_poll_role_not_found(self):
		a_channel = channel()
		a_message = message('!poll start', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')
		role = Role('Owner')
		a_message.author.roles.append(role)

		obj_list = [a_plugin]
		#assert await self.obj.run(a_message, obj_list) == False

	async def test_poll_check_service_not_running(self):
		a_channel = channel()
		a_message = message('!poll', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')
		role = Role('Moderator')
		a_message.author.roles.append(role)

		obj_list = [a_plugin]
		assert await self.obj.run(a_message, obj_list) == True

	async def test_poll_check_service_running(self):
		a_channel = channel()
		a_message = message('!poll start', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')
		role = Role('Moderator')
		a_message.author.roles.append(role)

		obj_list = [a_plugin]
		await self.obj.run(a_message, obj_list)
		a_message.content = '!poll'
		assert await self.obj.run(a_message, obj_list) == True

	async def test_poll_restricted(self):
		a_channel = channel()
		a_message = message('!poll start', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')
		role = Role('Restricted')
		a_message.author.roles.append(role)

		obj_list = [a_plugin]
		#assert await self.obj.run(a_message, obj_list) == False

	async def test_start_service(self):
		new_obj = Poll()

		a_channel = channel()
		#a_channel.name = new_obj.post_channel
		a_message = message('!poll start', a_channel)
		a_message.guild.channels.append(a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')
		role = Role('Moderator')
		a_message.author.roles.append(role)

		print('Channel name: ' + str(a_message.channel.name))

		obj_list = [a_plugin]
		assert await new_obj.run(a_message, obj_list) == True

	async def test_stop_service_not_running(self):
		a_channel = channel()
		#a_channel.name = self.obj.post_channel
		a_message = message('!poll stop', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')
		role = Role('Moderator')
		a_message.author.roles.append(role)

		obj_list = [a_plugin]
		assert await self.obj.run(a_message, obj_list) == False

	async def test_poll_stop_service_running(self):
		new_obj = Poll()

		a_channel = channel()
		#a_channel.name = new_obj.post_channel
		a_message = message('!poll start', a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')
		role = Role('Moderator')
		a_message.author.roles.append(role)

		obj_list = [a_plugin]
		await new_obj.run(a_message, obj_list)
		a_message.content = '!poll stop'
		assert await new_obj.run(a_message, obj_list) == True

	async def test_start_new_poll(self):
		new_obj = Poll()

		a_channel = channel()
		#a_channel.name = new_obj.post_channel
		a_message = message('!poll This is a test poll', a_channel)
		a_message.guild.channels.append(a_channel)
		a_plugin = plugin('!help', 'help menu', '!help')
		role = Role('Moderator')
		a_message.author.roles.append(role)

		print('Channel name: ' + str(a_message.channel.name))

		obj_list = [a_plugin]
		assert await new_obj.run(a_message, obj_list) == True

	async def test_update_poll_embed_base_fields(self):
		new_obj = Poll()

		a_channel = channel()
		#a_channel.name = new_obj.post_channel
		a_message = message('', a_channel)
		a_message.guild.channels.append(a_channel)
		role = Role('Moderator')
		a_message.author.roles.append(role)

		embed = discord.Embed(title="Poll",
				color=discord.Color.blue())

		embed.add_field(name='Poll Description', value='This is a test poll', inline=False)
		embed.add_field(name='Creator', value=str(a_message.author.mention), inline=False)

		embed.add_field(name='Status', value='```OPEN```', inline = False)

		a_message.embed = embed

		assert await new_obj.update_poll_embed(a_message, embed, 10) == True

	async def test_update_poll_embed_new_fields(self):
		new_obj = Poll()

		a_channel = channel()
		#a_channel.name = new_obj.post_channel
		a_message = message('', a_channel)
		a_message.guild.channels.append(a_channel)
		role = Role('Moderator')
		a_message.author.roles.append(role)

		embed = discord.Embed(title="Poll",
				color=discord.Color.blue())

		embed.add_field(name='Poll Description', value='This is a test poll', inline=False)
		embed.add_field(name='Creator', value=str(a_message.author.mention), inline=False)

		embed.add_field(name='Status', value='```OPEN```', inline = False)

		embed.add_field(name='Time Left', value='```' + str(10) + '```', inline=False)

		embed.add_field(name='Minimum required "yes" votes', value='```' + str(10) + '```', inline=False)

		a_message.embed = embed

		assert await new_obj.update_poll_embed(a_message, embed, 10) == True

	async def test_check_poll_embed_new(self):
		new_obj = Poll()

		a_channel = channel()
		#a_channel.name = new_obj.post_channel
		a_message = message('', a_channel)
		a_message.guild.channels.append(a_channel)
		role = Role('Moderator')
		a_message.author.roles.append(role)

		embed = discord.Embed(title="Poll",
				color=discord.Color.blue())

		embed.add_field(name='Poll Description', value='This is a test poll', inline=False)
		embed.add_field(name='Creator', value=str(a_message.author.mention), inline=False)

		embed.add_field(name='Status', value='```OPEN```', inline = False)

		embed.add_field(name='Time Left', value='```' + str(10) + '```', inline=False)

		embed.add_field(name='Minimum required "yes" votes', value='```' + str(10) + '```', inline=False)

		a_message.embed = embed

		assert await new_obj.check_poll_embed(a_message, embed) == True

	async def test_close_poll_embed_tie(self):
		new_obj = Poll()

		a_channel = channel()
		#a_channel.name = new_obj.post_channel
		a_message = message('', a_channel)
		a_message.guild.channels.append(a_channel)
		role = Role('Moderator')
		a_message.author.roles.append(role)

		embed = discord.Embed(title="Poll",
				color=discord.Color.blue())

		embed.add_field(name='Poll Description', value='This is a test poll', inline=False)
		embed.add_field(name='Creator', value=str(a_message.author.mention), inline=False)

		embed.add_field(name='Status', value='```OPEN```', inline = False)

		embed.add_field(name='Time Left', value='```' + str(10) + '```', inline=False)

		embed.add_field(name='Minimum required "yes" votes', value='```' + str(10) + '```', inline=False)

		#reaction = Reaction(new_obj.yes_vote)

		#a_message.reactions.append(reaction)

		#reaction = Reaction(new_obj.no_vote)

		#a_message.reactions.append(reaction)

		a_message.embed = embed

		assert await new_obj.close_poll_embed(a_message, embed) == True

	async def test_close_poll_embed_lose(self):
		new_obj = Poll()

		a_channel = channel()
		#a_channel.name = new_obj.post_channel
		a_message = message('', a_channel)
		a_message.guild.channels.append(a_channel)
		role = Role('Moderator')
		a_message.author.roles.append(role)

		embed = discord.Embed(title="Poll",
				color=discord.Color.blue())

		embed.add_field(name='Poll Description', value='This is a test poll', inline=False)
		embed.add_field(name='Creator', value=str(a_message.author.mention), inline=False)

		embed.add_field(name='Status', value='```OPEN```', inline = False)

		embed.add_field(name='Time Left', value='```' + str(10) + '```', inline=False)

		embed.add_field(name='Minimum required "yes" votes', value='```' + str(10) + '```', inline=False)

		#reaction = Reaction(new_obj.no_vote)

		#a_message.reactions.append(reaction)

		a_message.embed = embed

		assert await new_obj.close_poll_embed(a_message, embed) == True

	async def test_close_poll_embed_win(self):
		new_obj = Poll()

		a_channel = channel()
		#a_channel.name = new_obj.post_channel
		a_message = message('', a_channel)
		a_message.guild.channels.append(a_channel)
		role = Role('Moderator')
		a_message.author.roles.append(role)

		embed = discord.Embed(title="Poll",
				color=discord.Color.blue())

		embed.add_field(name='Poll Description', value='This is a test poll', inline=False)
		embed.add_field(name='Creator', value=str(a_message.author.mention), inline=False)

		embed.add_field(name='Status', value='```OPEN```', inline = False)

		embed.add_field(name='Time Left', value='```' + str(10) + '```', inline=False)

		embed.add_field(name='Minimum required "yes" votes', value='```' + str(10) + '```', inline=False)

		#reaction = Reaction(new_obj.yes_vote)
		#reaction.count = 100

		#a_message.reactions.append(reaction)

		a_message.embed = embed

		assert await new_obj.close_poll_embed(a_message, embed) == True

	async def test_close_poll_embed_missing_votes(self):
		new_obj = Poll()

		a_channel = channel()
		#a_channel.name = new_obj.post_channel
		a_message = message('', a_channel)
		a_message.guild.channels.append(a_channel)
		role = Role('Moderator')
		a_message.author.roles.append(role)

		embed = discord.Embed(title="Poll",
				color=discord.Color.blue())

		embed.add_field(name='Poll Description', value='This is a test poll', inline=False)
		embed.add_field(name='Creator', value=str(a_message.author.mention), inline=False)

		embed.add_field(name='Status', value='```OPEN```', inline = False)

		embed.add_field(name='Time Left', value='```' + str(10) + '```', inline=False)

		embed.add_field(name='Minimum required "yes" votes', value='```' + str(10) + '```', inline=False)

		#reaction = Reaction(new_obj.yes_vote)
		#reaction.count = -1

		#a_message.reactions.append(reaction)

		#reaction = Reaction(new_obj.no_vote)
		#reaction.count = -2

		#a_message.reactions.append(reaction)

		a_message.embed = embed

		assert await new_obj.close_poll_embed(a_message, embed) == True

	async def test_stop(self):
		await self.obj.stop('potato')

if __name__ == '__main__':
	unittest.main()