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

	synt = '!giveaway [start <name>|stop <msg id>|pick <msg id>][config|get <config>|set <config> <value>|add/remove <config> <value>]'

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
	
	start_date = datetime.now()

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

	def generatePluginConfig(self, file_name):
		for new_conf in self.configutils.generateConfig(self.conf_path, self.default_config, file_name, __file__):
			self.guild_confs.append(new_conf)

	# Required method for services (content may vary)
	async def getStatus(self, message):
		# Return True if there is a giveaway running in the source message's server
		for index in self.running_giveaways:
			if index[0].guild == message.guild:
				return True

		return False

	# Required method for services
	async def startService(self):
		if not self.looping:
			self.looping = True
			self.loop_func.start()
			return True
		return False

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

						if (real_member not in index[1]) and (self.looping):
							print('Adding ' + str(real_member) + ' to giveaway: ' + str(msg.id))
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
			return True
		#	if self.running:
		#		await message.channel.send(message.author.mention + ' `' + self.giveaway_name + '` is currently running: ' + str(self.giveaway_message.jump_url))
		#	else:
		#		await message.channel.send(message.author.mention + ' There are no giveaways running')
		#	return True

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
			test_name = ''
			for i in range(2, len(seg)):
				test_name = test_name + seg[i] + ' '
			self.giveaway_name = test_name[:-1]
			self.users.clear()
			self.winner = None
			self.running = True
			self.start_time = datetime.now()
			embed.add_field(name='Title', value='```' + str(self.giveaway_name) + '```', inline=True)
			embed.add_field(name='Participants', value='```' + str(len(self.users)) + '```', inline=True)

			embed.add_field(name = chr(173), value = chr(173))

			embed.add_field(name='Started at', value='```' + str(self.start_time) + '```', inline=False)

			role_string = ''
			try:
				for standard_role in the_config['standard_groups']['value']:
					for role in message.guild.roles:
						if str(role.mention) == standard_role:
							role_string = role_string + role.mention + ' '
							continue
			except:
				pass

			embed.add_field(name='Required Roles (at least one)', value=str(role_string), inline=False)
			embed.add_field(name='How to join', value='```React with any emote```', inline=False)
			embed.add_field(name='Status', value='```OPEN```', inline=False)
			embed.add_field(name='Winners', value='``` ```', inline=False)

			# Get the channel where stuff is going to be posted
			local_post_channel = await self.get_post_channel(message, the_config)
			if local_post_channel == None:
				return False
			giveaway_message = await local_post_channel.send('@everyone', embed=embed)

			# Add giveaway message to list of running giveaways
			self.running_giveaways.append([giveaway_message, [], [], test_name[:-1]])

			# Show us the list of running giveaway messages
			print('Giveaway messages: ')
			for index in self.running_giveaways:
				msg = index[0]
				print('\t' + str(msg.id))

			#if not self.looping:
			#	self.looping = True
			#	self.loop_func.start()

			return self.giveaway_name

		# Stoping giveaway
		if command == 'stop':
			check_msg_id = str(arg[2])
			print('Checking ' + check_msg_id)

			# Check if this message is even part of the user's server
			# This will prevent someone with admin privs on another server from picking
			# A winner on a server where they don't have admin privs
			the_index = None
			for index in self.running_giveaways:
				msg = index[0]
				if (msg.guild == message.guild) and (check_msg_id == str(msg.id)):
					the_index = index
					break

			# User tried to pick a winner for a giveaway that wasn't running in their server
			if the_index == None:
				print('Source msg guild and target giveaway guild did not match')
				await message.channel.send(message.author.mention + ' That giveaway is not running on this server')
				return False

			# Remove the target giveaway from the list of running giveaways
			self.running_giveaways.remove(the_index)
			await message.channel.send(message.author.mention + '`' + str(self.giveaway_name) + '` giveaway stopped')
			the_embed = None
			for embed in the_index[0].embeds:
				if embed.title == 'Giveaway':
					the_embed = embed
					break

			for i in range(0, len(the_embed.fields)):
				if the_embed.fields[i].name=='Status':
					embed.set_field_at(i, name=embed.fields[i].name, value='```CLOSED```', inline=False)

			await the_index[0].edit(embed=the_embed)

			# Show us the list of running giveaway messages
			print('Giveaway messages: ')
			for index in self.running_giveaways:
				msg = index[0]
				print('\t' + str(msg.id))

		# Pick winner
		if command == 'pick':

			check_msg_id = str(arg[2])
			print('Checking ' + check_msg_id)

			# Check if this message is even part of the user's server
			# This will prevent someone with admin privs on another server from picking
			# A winner on a server where they don't have admin privs
			the_index = None
			for index in self.running_giveaways:
				msg = index[0]
				if (msg.guild == message.guild) and (check_msg_id == str(msg.id)):
					the_index = index
					break

			# User tried to pick a winner for a giveaway that wasn't running in their server
			if the_index == None:
				print('Source msg guild and target giveaway guild did not match')
				await message.channel.send(message.author.mention + ' That giveaway is not running on this server')
				return False

			if len(the_index[1]) <= 0:
				await message.channel.send(message.author.mention + ' There are no particpants for that giveaway')
				return False
				
			self.winner = random.choice(the_index[1])
			the_index[2].append(self.winner) # Add winner to index list of winners
			the_index[1].remove(self.winner) # Remove winner from index list of users
			await message.channel.send('The winner of `' + the_index[3] + '` is ' + str(self.winner.mention))

			# Update the embed...again
			the_embed = None
			for embed in the_index[0].embeds:
				if embed.title == 'Giveaway':
					the_embed = embed
					break

			for i in range(0, len(the_embed.fields)):
				if the_embed.fields[i].name=='Winners':
					value_str = ''
					for winr in the_index[2]:
						value_str = value_str + str(winr) + '\n'
					embed.set_field_at(i, name=embed.fields[i].name, value='```' + str(value_str) + '```', inline=False)

			await the_index[0].edit(embed=the_embed)
			await self.update_giveaway_embed(the_index)

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

		return True

	async def stop(self, message):
		self.looping = False
		try:
			self.loop_func.stop()
		except:
			return
