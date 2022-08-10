import os
import sys
import json
import discord
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class SearchReact():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	guild_confs = []

	configutils = None

	name = '!searchreact'

	desc = 'Search a message to see if a user has reacted'

	synt = '!searchreact [config|get <config>|set <config> <value>|add/remove <config> <value>][<message id> <@user>]'

	is_service = False

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
	default_config['post_channel'] = {}
	default_config['post_channel']['value'] = ""
	default_config['post_channel']['description'] = "Desitination channel to post messages from this plugin"

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

	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False
	
	async def runCheer(self, user, amount):
		return True

	async def getMessageById(self, guild, id):
		target_message = None
		for channel in guild.channels:
			try:
				target_message = await channel.fetch_message(id)
				#print('Found ' + str(id) + ' in ' + str(channel.name))
				break
			except:
				continue

		return target_message

	
	async def runCheer(self, user, amount):
		return True

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
		message_id = str(arg[1])

		target_message = await self.getMessageById(message.guild, message_id)

		for real_member in message.mentions:
			message_content = None
			for reaction in target_message.reactions:
				async for member in reaction.users():
					if member.name == real_member.name:
						message_content = message_content + message.author.mention + ' User ' + str(member.name) + ' Reacted with ' + str(reaction.emoji) + '\n'
						#await message.channel.send(message.author.mention + ' User ' + str(member.name) + ' Reacted with ' + str(reaction.emoji))
			if message_content is not None:
				await message.channel.send(message_content)

		return True

	async def stop(self, message):
		self.looping = False
