import os
import json
import random
import discord
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Giveaway():
	name = '!giveaway'

	desc = 'Start, stop, manage, and join giveaways'

	synt = '!giveaway [start <name>|stop|pick]'

	looping = False

	group = 'members'

	admin = False
	
	cheer = -1
	
	cat = 'admin'

	is_service = True

	giveaway_name = None

	users = []

	winner = None

	winner_list = []

	running = False

	admin_group = 'Moderator'
	
	participant_roles = ['members']
	blacklisted = ['Restricted']

	start_date = datetime.now()

	giveaway_message = None

	post_channel = 'giveaways'
#	post_channel = 'bot-commands'

	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False
	
	async def runCheer(self, user, amount):
		return

	@loop(seconds = 1)
	async def loop_func(self):
		if self.looping:
			cache_message = await self.giveaway_message.channel.fetch_message(self.giveaway_message.id)
			for reaction in cache_message.reactions:
				async for user in reaction.users():
					real_member = user

					# Check if user is blacklisted
					for role in user.roles:
						if str(role.name) in self.blacklisted:
							return

					# Check if user has the required roles
					role_found = False
					for role in user.roles:
						if str(role.name) in self.participant_roles:
							role_found = True
							break

					if not role_found:
						return

					if (real_member not in self.users) and (self.looping):
						print('Adding ' + str(real_member) + ' to giveaway list')
						self.users.append(real_member)
						await self.update_giveaway_embed()

	async def update_giveaway_embed(self):
		the_embed = None
		for embed in self.giveaway_message.embeds:
			if embed.title == 'Giveaway':
#				print('Found the giveaway')
				the_embed = embed
				break

		for i in range(0, len(the_embed.fields)):
			if the_embed.fields[i].name=='Participants':
#				print('Setting the user amount')
				the_embed.set_field_at(i, name=embed.fields[i].name, value='```' + str(len(self.users)) + '```', inline=True)

		await self.giveaway_message.edit(embed=the_embed)

	async def get_post_channel(self, message):
		# Find where the bot will be posting its announcements
		for channel in message.guild.channels:
			if str(channel.name) == self.post_channel:
				return channel
		return None

	async def run(self, message, obj_list):
		embed = discord.Embed(title="Giveaway",
				color=discord.Color.green())

		cmd = str(message.content)
		seg = str(message.content).split(' ')
		if len(seg) < 1:
			await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
			return

		if message.content == '!giveaway':
			if self.running:
#				embed.add_field(name='Title', value='```' + str(self.giveaway_name) + '```', inline=True)
#				embed.add_field(name='Participants', value='```' + str(len(self.users)) + '```', inline=True)

#				embed.add_field(name = chr(173), value = chr(173))

#				embed.add_field(name='Started at', value='```' + str(self.start_time) + '```', inline=False)

#				embed.add_field(name='Required Roles', value='```' + str(self.group) + '```', inline=False)
				await message.channel.send(message.author.mention + ' `' + self.giveaway_name + '` is currently running: ' + str(self.giveaway_message.jump_url))
#				await message.channel.send(embed=embed)
			else:
				await message.channel.send(message.author.mention + ' There are no giveaways running')
			return

		command = seg[1]

		user_groups = []
		for role in message.author.roles:
			user_groups.append(role.name)

		# Starting giveaway
		if command == 'start':
			if self.admin_group not in user_groups:
				await message.channel.send(message.author.mention + ' ' + str(cmd) + ' You must be a member of ' + self.admin_group + ' to run this command')
				return
			if len(seg) < 3:
				await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
				return
			test_name = ''
			for i in range(2, len(seg)):
				test_name = test_name + seg[i] + ' '
			self.giveaway_name = test_name[:-1]
			self.users.clear()
			self.winner = None
			self.running = True
			self.start_time = datetime.now()
			self.winner_list = []
#			await message.channel.send(message.author.mention + '`' + str(self.giveaway_name) + '` giveaway started')
			embed.add_field(name='Title', value='```' + str(self.giveaway_name) + '```', inline=True)
			embed.add_field(name='Participants', value='```' + str(len(self.users)) + '```', inline=True)

			embed.add_field(name = chr(173), value = chr(173))

			embed.add_field(name='Started at', value='```' + str(self.start_time) + '```', inline=False)

			embed.add_field(name='Required Roles', value='```' + str(self.participant_roles) + '```', inline=False)
			embed.add_field(name='How to join', value='```React with any emote```', inline=False)
			embed.add_field(name='Status', value='```OPEN```', inline=False)
			embed.add_field(name='Winners', value='``` ```', inline=False)

			local_post_channel = await self.get_post_channel(message)
			self.giveaway_message = await local_post_channel.send(embed=embed)
			self.looping = True
			self.loop_func.start()

		# Stoping giveaway
		if command == 'stop':
			if not self.running:
				await message.channel.send(message.author.mention + ' There are no giveaways running')
				return
			if self.admin_group not in user_groups:
                                await message.channel.send(message.author.mention + ' ' + str(cmd) + ' You must be a member of ' + self.admin_group + ' to run this command')
                                return
			if len(seg) != 2:
				await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
				return
			self.users.clear()
			self.winner_list = []
			self.winner = None
			self.running = False
			await message.channel.send(message.author.mention + '`' + str(self.giveaway_name) + '` giveaway stopped')
			self.giveaway_name = None
			the_embed = None
			for embed in self.giveaway_message.embeds:
				if embed.title == 'Giveaway':
					the_embed = embed
					break

			for i in range(0, len(the_embed.fields)):
				if the_embed.fields[i].name=='Status':
					embed.set_field_at(i, name=embed.fields[i].name, value='```CLOSED```', inline=False)

			await self.giveaway_message.edit(embed=the_embed)
			self.giveaway_message = None
			self.looping = False
			self.loop_func.stop()
#			await message.channel.send(embed=embed)

		# Pick winner
		if command == 'pick':
			if not self.running:
				await message.channel.send(message.author.mention + ' There are no giveaways running')
				return
			if self.admin_group not in user_groups:
				await message.channel.send(message.author.mention + ' ' + str(cmd) + ' You must be a member of ' + self.admin_group + ' to run this command')
				return
			if len(seg) != 2:
				await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
				return
			if len(self.users) <= 0:
				await message.channel.send(message.author.mention + ' There are no participants in the giveaway')
				return
			self.winner = random.choice(self.users)
			self.winner_list.append(self.winner)
			self.users.remove(self.winner)
			await message.channel.send('The winner of `' + self.giveaway_name + '` is ' + str(self.winner.mention))

			# Update the embed...again
			the_embed = None
			for embed in self.giveaway_message.embeds:
				if embed.title == 'Giveaway':
					the_embed = embed
					break

			for i in range(0, len(the_embed.fields)):
				if the_embed.fields[i].name=='Winners':
					value_str = ''
					for winr in self.winner_list:
						value_str = value_str + str(winr) + '\n'
					embed.set_field_at(i, name=embed.fields[i].name, value='```' + str(value_str) + '```', inline=False)

			await self.giveaway_message.edit(embed=the_embed)
			await self.update_giveaway_embed()
#			await message.channel.send(embed=embed)

		# Join giveaway
		if command == 'asdfahsdlfkjahwefw8efh23487fhwed8f7ahsdfkqw43h':
			# Giveaway is not running
			if not self.running:
				await message.channel.send(message.author.mention + ' There are no giveaways running')
				return

			# Improper syntax
			if len(seg) != 2:
				await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
				return
			discord_user = message.author

			# They are already in the giveaway
			if discord_user in self.users:
				await message.channel.send(message.author.mention + '`' + str(message.content) + '` You have *already* joined the giveaway')
			# Here is your ticket
			else:
				self.users.append(discord_user)
				await message.channel.send(message.author.mention + 'Welcome to the giveaway: `' + self.giveaway_name + '`')

				await self.update_giveaway_embed()

#			await message.channel.send(embed=embed)
		return

	async def stop(self, message):
		self.looping = False
