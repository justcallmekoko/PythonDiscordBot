import os
import json
import discord
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Poll():
	global client
	name = '!poll'

	desc = 'Start a poll'

	synt = '!poll <description>'

	looping = False

	group = 'members'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	is_service = False

	poll_desc = None

	post_channel = 'polls-and-suggestions'

	groups = ['Twitch Subscriber',
		'3 Months',
		'6 Months',
		'One Year',
		'Server Booster',
		'Moderator']

	blacklisted = ['Restricted']

	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False
	
	async def runCheer(self, user, amount):
		return

	async def run(self, message, obj_list):
		# Check if user can run this command
		for role in message.author.roles:
			if str(role.name) in self.blacklisted:
				await message.channel.send(message.author.mention + ', Users with the role, `' + str(role.name) + '` are not permitted to run this command')
				return

		role_found = False
		for role in message.author.roles:
			if str(role.name) in self.groups:
				role_found = True
				break

		if not role_found:
			await message.channel.send(message.author.mention + ', Users require one of these roles to run this command.\n`' + str(self.groups) + '`')
			return

		cmd = str(message.content)
		seg = str(message.content).split(' ')
		if len(seg) < 1:
			await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
			return

		test_name = ''
		for i in range(1, len(seg)):
			test_name = test_name + seg[i] + ' '
		self.poll_desc = test_name[:-1]

#		await message.channel.send(self.poll_desc)

		embed = discord.Embed(title="Poll",
				color=discord.Color.blue())

		embed.add_field(name='Poll Description', value=str(self.poll_desc), inline=False)
		embed.add_field(name='Creator', value=str(message.author.mention), inline=False)

#		embed.add_field(name='Rules', value='Vote with <:plusone:> or <:minusone:>', inline=False)

		post_channel = None

		# Find where the bot will be posting its announcements
		for channel in message.guild.channels:
			if str(channel.name) == self.post_channel:
				post_channel = channel

		if post_channel != None:
			msg = await post_channel.send(embed=embed)

			await msg.add_reaction('<:plusone:912765835184074785>')

			await msg.add_reaction('<:minusone:912765865789898793>')

		return

	async def stop(self, message):
		self.looping = False
