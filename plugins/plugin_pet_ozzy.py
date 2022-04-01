import os
import sys
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class PetOzzy():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')
	name = '!petozzy'

	desc = 'Give Ozzy a pet. He deserves it'

	synt = '!petozzy [config|get <config>|set <config> <value>|add/remove <config> <value>]'

	looping = False

	group = '@everyone'

	default_config = {}
	default_config['protected'] = {}
	default_config['protected']['name'] = __file__
	default_config['protected']['guild'] = None
	default_config['standard_groups'] = ['@everyone']
	default_config['admin_groups'] = []
	default_config['blacklisted'] = []
	default_config['post_channel'] = ''

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	is_service = False

	client = None

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
				
		# Create fresh stat file
		if not os.path.isfile('ozzystats.json'):
			# Create fresh json template
			data = {}
			data['name'] = 'Ozzy'
			data['pets'] = 0
			data['members'] = []
			with open('ozzystats.json', 'w') as f:
				json.dump(data, f)

		# Get json data
		f = open('ozzystats.json',)

		json_data = json.load(f)

		f.close()

		# Adjust number of pets by 1
		json_data['pets'] = int(json_data['pets']) + 1

		discord_user = str(message.author)

		found = False

		# Search for member in list of members
		for member in json_data['members']:
			if member['name'] == discord_user:
				found = True
				break

		if not found:
			# Add user to list of members who have done a pet if not there
			json_data['members'].append({'name': str(discord_user)})

		# Write new json data to json file
		with open('ozzystats.json', 'w') as f:
			json.dump(json_data, f)

		await message.channel.send(message.author.mention + ' just pet Ozzy')

		return True

	async def stop(self, message):
		self.looping = False
