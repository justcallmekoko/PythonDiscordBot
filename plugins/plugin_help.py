import os
import sys
import json
import discord
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class Help():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	name = '!help'

	desc = 'Display list of commands or specific command usage'

	synt = '!help [command]'

	looping = False

	default_config = {}
	default_config['protected'] = {}
	default_config['protected']['name'] = __file__
	default_config['protected']['guild'] = None
	default_config['standard_groups'] = {}
	default_config['standard_groups']['value'] = ["@everyone"]
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

	group = '@everyone'

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

		embed = discord.Embed(title="Help",
				color=discord.Color.blue())

		if str(message.content) == '!help':
			for obj in obj_list:
				embed.add_field(name=str(obj.name), value='`' + str(obj.desc) + '`', inline=False)

			await message.channel.send(embed=embed)
		elif '!help ' in str(message.content):
			for obj in obj_list:
				if str(message.content).split(' ')[1] == str(obj.name):
					embed.add_field(name="Command", value='`' + str(obj.name) + '`', inline=True)
					embed.add_field(name="Description", value='`' + str(obj.synt) + '`', inline=True)
			await message.channel.send(embed=embed)

		return

	async def stop(self, message):
		self.looping = False
