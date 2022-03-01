import os
import json
import discord
import pytz
from pytz import utc
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Poll():
	name = '!poll'

	desc = 'Start a poll and start the poll service'

	synt = '!poll [<description>]|[start]|[stop]'

	looping = False

	group = 'members'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	is_service = True

	client = None

	poll_desc = None

	poll_time_limit = 604800 #seconds

	global_message = None

	time_zone = 'US/Eastern'

	message_history_limit = 100

	post_channel = 'polls-and-suggestions'
#	post_channel = 'bot-commands'

	groups = ['Twitch Subscriber',
		'3 Months',
		'6 Months',
		'One Year',
		'Server Booster',
		'Moderator']

	blacklisted = ['Restricted']

	service_roles = ['Moderator']

	yes_vote = '<:plusone:912765835184074785>'
	no_vote = '<:minusone:912765865789898793>'

	def __init__(self, client = None):
		self.client = client

	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False
	
	async def runCheer(self, user, amount):
		return

	async def update_poll_embed(self, msg, embed, seconds_diff):
		# Convert seconds to datetime
		day = seconds_diff // (24 * 3600)
		seconds_diff = seconds_diff % (24 * 3600)
		hour = seconds_diff // 3600
		seconds_diff %= 3600
		minutes = seconds_diff // 60
		seconds_diff %= 60
		seconds = seconds_diff
		time_left = "%d(days) %d(hours) %d(minutes) %d(seconds)" % (day, hour, minutes, seconds)

		poll_desc = ''
		for field in embed.fields:
			if field.name == 'Poll Description':
				poll_desc = field.value

#		print(str(poll_desc) + ': ' + str(time_left))

		field_found = False
		for i in range(0, len(embed.fields)):
			if embed.fields[i].name=='Time Left':
				embed.set_field_at(i, name=embed.fields[i].name, value='```' + str(time_left) + '```', inline=False)
				field_found = True

		if not field_found:
			embed.add_field(name='Time Left', value='```' + str(time_left) + '```', inline=False)

		await msg.edit(embed=embed)

	async def close_poll_embed(self, msg, embed):
		for i in range(0, len(embed.fields)):
			if embed.fields[i].name=='Status':
				embed.set_field_at(i, name=embed.fields[i].name, value='```CLOSED```', inline=False)

				# Check votes
				yes_count = 0
				no_count = 0
				for reaction in msg.reactions:
					print(str(reaction) + ': ' + str(reaction.count))
					if str(reaction.emoji) == self.yes_vote:
						yes_count = reaction.count
					elif str(reaction.emoji) == self.no_vote:
						no_count = reaction.count

				print(str(yes_count) + ' | ' + str(no_count))

				if yes_count > no_count:
					embed.add_field(name='Result', value='```APPROVED```', inline=False)
				elif yes_count < no_count:
					embed.add_field(name='Result', value='```DENIED```', inline=False)
				else:
					embed.add_field(name='Result', value='```TIE```', inline=False)

		await msg.edit(embed=embed)

	async def check_poll_embed(self, msg, embed):
		for field in embed.fields:
			if (field.name == 'Status') and (field.value == '```OPEN```'):
#				print('Found open Poll')

				usest = pytz.timezone(self.time_zone)
				msg_time = utc.localize(msg.created_at)

				now = datetime.now()
				now = usest.localize(now)

				message_hist_sec = (now - msg_time).total_seconds()

#				print('Message time: ' + str(msg_time))
#				print('Current time: ' + str(now))
#				print('Elapsed time: ' + str(message_hist_sec))
#				print('Seconds left: ' + str(self.poll_time_limit - message_hist_sec))

				await self.update_poll_embed(msg, embed, self.poll_time_limit - message_hist_sec)

				if message_hist_sec > self.poll_time_limit:
					print(str(now) + ' - ' + str(msg_time))
					print('Found open Poll that needs to be closed: ' + str(message_hist_sec))
					await self.close_poll_embed(msg, embed)

	@loop(seconds = 30)
	async def loop_func(self):
		if self.looping:
			post_channel = None
			# Find where the bot will be posting its announcements
			for channel in self.global_message.guild.channels:
				if str(channel.name) == self.post_channel:
					post_channel = channel

			if post_channel == None:
				return

			# Get the messages
			messages = await post_channel.history(limit=self.message_history_limit).flatten()
			for msg in messages:
				embeds = msg.embeds
				# Check for message Poll embeds
				for embed in embeds:
					if embed.title == 'Poll':
						await self.check_poll_embed(msg, embed)
			return

	async def run(self, message, obj_list):
		self.global_message = message
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


		# Do service stuff
		if len(seg) == 2:
			# Check permissions
			role_found = False
			for role in message.author.roles:
	                        if str(role.name) in self.service_roles:
	                                role_found = True
	                                break
			# Only do service stuff if user has role
			if role_found:
				# Service is being started
				if str(seg[1]) == 'start':
					if not self.looping:
						self.looping = True
						await message.channel.send(message.author.mention + ' Starting ' + str(self.name))
						self.loop_func.start()
						return
				if str(seg[1]) == 'stop':
					if self.looping:
						self.looping = False
						await message.channel.send(message.author.mention + ' Stopping ' + str(self.name))
						self.loop_func.stop()
						return
			else:
				return

		elif len(seg) == 1:
			if self.looping:
				await message.channel.send(message.author.mention + ' ' + str(self.name) + ' is running')
			else:
				await message.channel.send(message.author.mention + ' ' + str(self.name) + ' is not running')
			return

		# Start the pole here
		test_name = ''
		for i in range(1, len(seg)):
			test_name = test_name + seg[i] + ' '
		self.poll_desc = test_name[:-1]

#		await message.channel.send(self.poll_desc)

		embed = discord.Embed(title="Poll",
				color=discord.Color.blue())

		embed.add_field(name='Poll Description', value=str(self.poll_desc), inline=False)
		embed.add_field(name='Creator', value=str(message.author.mention), inline=False)

		embed.add_field(name='Status', value='```OPEN```', inline = False)

#		embed.add_field(name='Rules', value='Vote with <:plusone:> or <:minusone:>', inline=False)

		post_channel = None

		# Find where the bot will be posting its announcements
		for channel in message.guild.channels:
			if str(channel.name) == self.post_channel:
				post_channel = channel

		if post_channel != None:
			msg = await post_channel.send(embed=embed)

			await msg.add_reaction(self.yes_vote)

			await msg.add_reaction(self.no_vote)

		return

	async def stop(self, message):
		self.looping = False
