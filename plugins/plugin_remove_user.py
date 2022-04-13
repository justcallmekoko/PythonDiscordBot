import os
import sys
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

RCONIP = os.getenv('RCON_IP')
PASSW = os.getenv('RCON_PASSWORD')

class RemoveUser():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	guild_confs = []

	configutils = None

	name = '!clear'

	desc = 'Clear your user from minecraft server whitelist'

	synt = '!clear'

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

	looping = False

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
		
		discord_user = str(message.author)
		if not os.path.isfile('users.txt'):
			with open('users.txt', 'w') as f:
				f.close()

		with open('users.txt', 'r') as f:
			lines = f.readlines()

		found = False

		for line in lines:
			if discord_user == line.split(':')[0]:
				found = True
				break

		if not found:
			await message.channel.send(message.author.mention + ' There is no linked minecraft username')
			return
		else:
			for line in lines:
				if discord_user in line:
					the_line = line

			minecraft_user = the_line.split(':')[1].replace('\n', '')

			lines.remove(the_line)

			with open('users.txt', 'w') as f:
				f.writelines(lines)

			with MCRcon(RCONIP, PASSW) as mcr:
				resp = mcr.command('whitelist remove ' + str(minecraft_user))
				mcr.disconnect()

			await message.channel.send(message.author.mention + ' Removed user from whitelist: ' + str(minecraft_user))

	async def stop(self, message):
		self.looping = False
