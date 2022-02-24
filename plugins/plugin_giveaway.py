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

	synt = '!giveaway [start <name>|stop|pick|join]'

	looping = False

	group = 'members'

	admin = False
	
	cheer = -1
	
	cat = 'admin'

	is_service = False

	giveaway_name = None

	users = []

	winner = None

	running = False

	admin_group = 'Moderator'
	
	start_date = datetime.now()

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
		embed = discord.Embed(title="Giveaway",
				color=discord.Color.green())

		cmd = str(message.content)
		seg = str(message.content).split(' ')
		if len(seg) < 1:
			await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
			return

		if message.content == '!giveaway':
			if self.running:
				embed.add_field(name='Title', value='```' + str(self.giveaway_name) + '```', inline=True)
				embed.add_field(name='Participants', value='```' + str(len(self.users)) + '```', inline=True)

				embed.add_field(name = chr(173), value = chr(173))

				embed.add_field(name='Started at', value='```' + str(self.start_time) + '```', inline=False)

				embed.add_field(name='Required Roles', value='```' + str(self.group) + '```', inline=False)
#				await message.channel.send(message.author.mention + ' `' + self.giveaway_name + '` is currently running with ' + str(len(self.users)) + ' participant(s)')
				await message.channel.send(embed=embed)
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
#			await message.channel.send(message.author.mention + '`' + str(self.giveaway_name) + '` giveaway started')
			embed.add_field(name='Title', value='```' + str(self.giveaway_name) + '```', inline=True)
			embed.add_field(name='Participants', value='```' + str(len(self.users)) + '```', inline=True)

			embed.add_field(name = chr(173), value = chr(173))

			embed.add_field(name='Started at', value='```' + str(self.start_time) + '```', inline=False)

			embed.add_field(name='Required Roles', value='```' + str(self.group) + '```', inline=False)
			await message.channel.send(embed=embed)

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
			self.winner = None
			self.running = False
			await message.channel.send(message.author.mention + '`' + str(self.giveaway_name) + '` giveaway stopped')
			self.giveaway_name = None
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
			self.users.remove(self.winner)
			await message.channel.send('The winner of `' + self.giveaway_name + '` is ' + str(self.winner.mention))
#			await message.channel.send(embed=embed)

		# Join giveaway
		if command == 'join':
			if not self.running:
				await message.channel.send(message.author.mention + ' There are no giveaways running')
				return
			if len(seg) != 2:
				await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
				return
			discord_user = message.author

			if discord_user in self.users:
				await message.channel.send(message.author.mention + '`' + str(message.content) + '` You have *already* joined the giveaway')
			else:
				self.users.append(discord_user)
				await message.channel.send(message.author.mention + 'Welcome to the giveaway: `' + self.giveaway_name + '`')

#			await message.channel.send(embed=embed)
		return

	async def stop(self, message):
		self.looping = False
