import os
import sys
import json
import discord
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class ReactRole():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	guild_confs = []

	configutils = None

	name = '!reactrole'

	desc = 'Assign a "react to receive role" capability to a message'

	synt = '!reactrole [<message_id> <emote> <role>; ...][config|get <config>|set <config> <value>|add/remove <config> <value>]\nOptions can be specified with ";" followed by an emote and the role of the option like so...\n!reactrole <message id> <emote> @role1; <emote> @role2; <emote> @role3'

	is_service = True

	client = None

	looping = False

	full_conf_file = None

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
	default_config['backend'] = {}
	default_config['backend']['reaction_messages'] = {}
	default_config['backend']['reaction_messages']['value'] = []
	default_config['backend']['reaction_messages']['description'] = "Messages that have been given the \"react to receive role\" capability"

	running_guilds = []

	# Server configurable

	group = '@everyone'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
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
		for index in self.running_guilds:
			if str(message.guild.name) + str(message.guild.id) == index:
				return True

		return False

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

	async def getMessageById(self, guild, id):
		target_message = None
		for channel in guild.channels:
			try:
				target_message = await channel.fetch_message(id)
				print('Found ' + str(id) + ' in ' + str(channel.name))
				break
			except:
				continue

		return target_message

	
	async def runCheer(self, user, amount):
		return True

	@loop(seconds = 5)
	async def loop_func(self):
		if self.looping:
			# Loop through all guilds
			for guild in self.client.guilds:
				# Only run on guilds that have the service enabled
				if str(guild.name) + str(guild.id) not in self.running_guilds:
					continue

				# Get the configuration of THIS guild
				guild_conf = self.configutils.getGuildConfigByGuild(guild, self.guild_confs)

				# Loop though each reaction message in THIS guild
				for msg in guild_conf['backend']['reaction_messages']['value']:
					real_message = await self.getMessageById(guild, msg['id'])
					if real_message == None: # The message does not exist in this server anymore
						continue

					#Loop through each reaction of THIS message
					for reaction in real_message.reactions:
						# Get the corresponding emote/role structure
						targ_given_reaction = None
						for given_reaction in msg['reactions']:
							if given_reaction['emote'] == str(reaction):
								targ_given_reaction = given_reaction

						# Loop through each user in THIS reaction
						async for user in reaction.users():
							# Check if user already has THIS role
							the_role = None
							for role in guild.roles:
								if str(role.mention) == targ_given_reaction['role']:
									the_role = role

							if the_role == None:
								continue

							if the_role in user.roles:
								continue

							print(str(user.name) + ' does not have ' + str(the_role.mention))

							try:
								user.add_role(the_role)
								print('Gave \'' + str(the_role.mention) + '\' to ' + user.name)
							except Exception as e:
								print('Could not give role: ' + str(e))
								continue

		return

	async def run(self, message, obj_list):
		# Permissions check
		if not self.configutils.hasPerms(message, False, self.guild_confs):
			await message.channel.send(message.author.mention + ' Permission denied')
			return False

		# Parse args
		arg = self.getArgs(message)

		# Config set/get check
		if arg != None:
			if await self.configutils.runConfig(message, arg, self.guild_confs, self.conf_path):
				return True

		# Do Specific Plugin Stuff

		seg = str(message.content).split(' ')
		the_guild = str(message.guild.name) + str(message.guild.id)
		guild_conf = self.configutils.getGuildConfig(message, self.guild_confs)

		# Do service stuff
		if len(seg) == 2:
			# Check if user has admin permissions to run the service
			if not self.configutils.hasPerms(message, True, self.guild_confs):
				await message.channel.send(message.author.mention + ' Permission denied')
				return False

			if str(seg[1]) == 'start':
				if the_guild not in self.running_guilds:
					self.running_guilds.append(the_guild)
					print('Guilds running ' + str(self.name) + ':')
					for gu in self.running_guilds:
						print('\t' + gu)
					await message.channel.send(message.author.mention + ' Starting ' + str(self.name))
					return True

			if str(seg[1]) == 'stop':
				if the_guild in self.running_guilds:
					self.running_guilds.remove(the_guild)
					await message.channel.send(message.author.mention + ' Stopping ' + str(self.name))
					print('Guilds running ' + str(self.name) + ':')
					for gu in self.running_guilds:
						print('\t' + gu)
					return True

			return False

		# User wants status of service
		elif len(seg) == 1:
			if self.looping:
				await message.channel.send(message.author.mention + ' ' + str(self.name) + ' is running')
			else:
				await message.channel.send(message.author.mention + ' ' + str(self.name) + ' is not running')
			return True

		# Get the message id the user wants
		targ_message_id = str(seg[1])
		print('Target message id: ' + targ_message_id)

		# Get the target message by id
		real_targ_message = await self.getMessageById(message.guild, targ_message_id)
		if real_targ_message == None:
			await message.channel.send(message.author.mention + ' ' + targ_message_id + ' does not exist on this server')
			return False

		# Try to get the options
		options_arg = str(message.content).replace(self.name + ' ' + targ_message_id + ' ', '')
		options = []
		for i in range(0, len(options_arg.split('; '))):
			option_emote = options_arg.split('; ')[i].split(' ')[0]
			option_text = options_arg.split('; ')[i].replace(str(option_emote) + ' ', '')
			full_option = [option_emote, option_text]
			options.append(full_option)

		# Show us options we received from user
		print('Received options:')
		for option in options:
			print('\t' + str(option))

		# Check if the given message has a role react
		reaction_messages = guild_conf['backend']['reaction_messages']['value']
		for msg in reaction_messages:
			if msg['id'] == targ_message_id:
				await message.channel.send(message.author.mention + ' ' + targ_message_id + ' already has a role reaction capability')
				return False

		# Create json structure
		json_obj = {}
		json_obj['id'] = targ_message_id
		json_obj['reactions'] = []
		for option in options:
			reaction = {}
			reaction['emote'] = option[0]
			reaction['role'] = option[1]
			json_obj['reactions'].append(reaction)

		print('JSON React Roles:')
		print(json.dumps(json_obj, indent=4, sort_keys=True))

		# Add the new react role message configuration to the plugin configuration
		guild_conf['backend']['reaction_messages']['value'].append(json_obj)

		# Save the configuration to the file (dangerous)
		self.configutils.saveConfig(str(message.guild.name) + '_' + str(message.guild.id), self.guild_confs, self.conf_path)

		# Show us all of the configurations
		print('All react messages for this server:')
		for msg in guild_conf['backend']['reaction_messages']['value']:
			print('\t' + str(msg['id']))

		# Add the reactions to the target message
		for option in options:
			await real_targ_message.add_reaction(option[0])

		# End of plugin stuff	

		return True

	async def stop(self, message):
		self.looping = False
