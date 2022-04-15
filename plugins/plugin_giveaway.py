import os
import sys
import json
import random
import discord
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class Giveaway():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	guild_confs = []

	configutils = None

	name = '!giveaway'

	desc = 'Start, stop, manage, and join giveaways'

	synt = '!giveaway [start <name>|stop|pick][config|get <config>|set <config> <value>|add/remove <config> <value>]'

	default_config = {}
	default_config['protected'] = {}
	default_config['protected']['name'] = __file__
	default_config['protected']['guild'] = None
	default_config['standard_groups'] = {}
	default_config['standard_groups']['value'] = []
	default_config['standard_groups']['description'] = "Authorized groups to use this command"
	default_config['admin_groups'] = {}
	default_config['admin_groups']['value'] = []
	default_config['admin_groups']['description'] = "Authorized groups to use admin functions of this command"
	default_config['blacklisted'] = {}
	default_config['blacklisted']['value'] = []
	default_config['blacklisted']['description'] = "Groups explicitly denied access to this command"
	default_config['post_channel'] = {}
	default_config['post_channel']['value'] = ""
	default_config['post_channel']['description'] = "Desitination channel to post messages from this plugin"

	running_giveaways = []

	looping = False

	group = '@everyone'

	admin = False
	
	cheer = -1
	
	cat = 'admin'

	is_service = True

	client = None

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

	def __init__(self, client = None):
		self.client = client
		self.configutils = ConfigUtils()

		# Load configuration if it exists
		self.guild_confs = self.configutils.loadConfig(self.conf_path, self.default_config, __file__)


		print('\n\nConfigs Loaded:')
		for config in self.guild_confs:
			print('\t' + config['protected']['name'] + ': ' + config['protected']['guild'])

	def getArgs(self, message):
		cmd = str(message.content)
		seg = str(message.content).split(' ')

		if len(seg) > 1:
			return seg
		else:
			return None

	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False
	
	async def runCheer(self, user, amount):
		return True

	@loop(seconds = 1)
	async def loop_func(self):
		if self.looping:
			# Loop through all running giveaway messages
			for index in self.running_giveaways:
				msg = index[0]
				cache_message = await msg.channel.fetch_message(msg.id)
				for reaction in cache_message.reactions:
					async for user in reaction.users():
						real_member = user

						# Get the configuration of this specific message
						the_config = self.configutils.getGuildConfig(msg, self.guild_confs)
						if not self.configutils.hasPermsUser(cache_message, real_member, False, self.guild_confs):
							print('does not have permission to join the giveaway')
							continue
						# Check if user is blacklisted or has perms

#						for role in user.roles:
#							if str(role.name) in self.blacklisted:
#								return True

						# Check if user has the required roles
#						role_found = False
#						for role in user.roles:
#							if str(role.name) in self.participant_roles:
#								role_found = True
#								break

#						if not role_found:
#							return False

						if (real_member not in index[1]) and (self.looping):
							print('Adding ' + str(real_member) + ' to giveaway list')
							index[1].append(real_member)
							await self.update_giveaway_embed(index)

	async def update_giveaway_embed(self, index):
		msg = index[0]
		the_embed = None
		for embed in msg.embeds:
			if embed.title == 'Giveaway':
#				print('Found the giveaway')
				the_embed = embed
				break

		for i in range(0, len(the_embed.fields)):
			if the_embed.fields[i].name=='Participants':
#				print('Setting the user amount')
				the_embed.set_field_at(i, name=embed.fields[i].name, value='```' + str(len(index[1])) + '```', inline=True)

		await msg.edit(embed=the_embed)

	async def get_post_channel(self, message, the_config):
		# Find where the bot will be posting its announcements
		for channel in message.guild.channels:
			try:
				if str(channel.mention) == str(the_config['post_channel']['value']):
					print('Found post_channel: ' + str(channel.mention))
					return channel
			except:
				return None
		return None

	async def run(self, message, obj_list):
		# Permissions check
		if not self.configutils.hasPerms(message, False, self.guild_confs):
			await message.channel.send(message.author.mention + ' Permission denied')
			return False

		the_config = self.configutils.getGuildConfig(message, self.guild_confs)

		# Parse args
		arg = self.getArgs(message)

		# Config set/get check
		if arg != None:
			if await self.configutils.runConfig(message, arg, self.guild_confs, self.conf_path):
				return True

		# Do Specific Plugin Stuff

		embed = discord.Embed(title="Giveaway",
				color=discord.Color.green())

		cmd = str(message.content)
		seg = str(message.content).split(' ')
		if len(seg) < 1:
			await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
			return False

		# User just wants status of giveaway
		if message.content == '!giveaway':
			if self.running:
				await message.channel.send(message.author.mention + ' `' + self.giveaway_name + '` is currently running: ' + str(self.giveaway_message.jump_url))
			else:
				await message.channel.send(message.author.mention + ' There are no giveaways running')
			return True

		# Get commands args...again
		command = seg[1]

		user_groups = []
		for role in message.author.roles:
			user_groups.append(role.name)

		# Anything beyond this point requires admin privs

		# Another permissions check
		if not self.configutils.hasPerms(message, True, self.guild_confs):
			await message.channel.send(message.author.mention + ' Permission denied')
			return False

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
			embed.add_field(name='Title', value='```' + str(self.giveaway_name) + '```', inline=True)
			embed.add_field(name='Participants', value='```' + str(len(self.users)) + '```', inline=True)

			embed.add_field(name = chr(173), value = chr(173))

			embed.add_field(name='Started at', value='```' + str(self.start_time) + '```', inline=False)

			embed.add_field(name='Required Roles', value='```' + str(self.participant_roles) + '```', inline=False)
			embed.add_field(name='How to join', value='```React with any emote```', inline=False)
			embed.add_field(name='Status', value='```OPEN```', inline=False)
			embed.add_field(name='Winners', value='``` ```', inline=False)

			# Get the channel where stuff is going to be posted
			local_post_channel = await self.get_post_channel(message, the_config)
			if local_post_channel == None:
				return False
			self.giveaway_message = await local_post_channel.send(embed=embed)

			# Add giveaway message to list of running giveaways
			self.running_giveaways.append([self.giveaway_message, [], [], test_name[:-1]])

			# Show us the list of running giveaway messages
			print('Giveaway messages: ')
			for msg in self.running_giveaways:
				print('\t' + str(msg.id))

			if not self.looping:
				self.looping = True
				self.loop_func.start()

			return self.giveaway_name

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
		return True

	async def stop(self, message):
		self.looping = False
