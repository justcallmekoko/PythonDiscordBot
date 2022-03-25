import os
import sys
import json
import discord
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class Template():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	name = '!template'

	desc = 'This does nothing. Developer only'

	synt = '!template [config|get <config>|set <config> <value>|add/remove <config> <value>]'

	is_service = False

	client = None

	looping = False

	guild_confs = []

	full_conf_file = None

	configutils = None

	default_config = {}
	default_config['name'] = __file__
	default_config['guild'] = None
	default_config['standard_groups'] = ['@everyone']
	default_config['admin_groups'] = []
	default_config['blacklisted'] = []
	default_config['post_channel'] = ''

	# Server configurable

	group = '@everyone'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	def __init__(self, client = None):
		self.client = client
		self.configutils = ConfigUtils()

		# Get each guild configuration
		for entity in os.listdir(self.conf_path):
			# Make sure the file is a config file
			if (os.path.isfile(os.path.join(self.conf_path, entity))) and (entity.endswith('_conf.json')):

				# Load configuration if it exists
				the_config, json_data, full_conf_file = self.configutils.loadConfig(self.conf_path, entity, __file__)

				guild_name = entity.split('_')[0] + entity.split('_')[1]

				# Plugin config does not exist. Create one
				if the_config == None:
					print('Could not find plugin configuration. Creating...')
					self.default_config['guild'] = guild_name
					json_data['plugins'].append(self.default_config)
					with open(full_conf_file, 'w') as f:
						json.dump(json_data, f, indent=4)

				else:
					self.guild_confs.append(the_config)

		print('\n\nConfigs Loaded:')
		for config in self.guild_confs:
			print('\t' + config['name'] + ': ' + config['guild'])

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

		return True

	async def stop(self, message):
		self.looping = False
