import os
import sys
import discord
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

RCONIP = os.getenv('RCON_IP')
PASSW = os.getenv('RCON_PASSWORD')

class AddUser():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	name = '!add'

	desc = 'Add user to minecraft server whitelist'

	synt = '!add [<minecraft username>|config|get <config>|set <config> <value>|add/remove <config> <value>]'

	looping = False

	guild_confs = []

	configutils = None

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

	client = None

	is_service = False

	group = 'members'

	admin = False
	
	cheer = -1
	
	cat = 'admin'

#	groups = ['People who pooped their pants']
	groups = [
		'Twitch Subscriber',
		'3 Months',
		'6 Months',
		'One Year',
		'Server Booster',
		'Moderator']

	blacklisted = ['Restricted']
	
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

		# Check if user can run this command
		for role in message.author.roles:
			if str(role.name) in self.blacklisted:
				await message.channel.send(message.author.mention + ', Users with the role, `' + str(role.name) + '` are not permitted to run this command')
				return True

		role_found = False
		for role in message.author.roles:
			if str(role.name) in self.groups:
				role_found = True
				break

		if not role_found:
			await message.channel.send(message.author.mention + ', Users require one of these roles to run this command.\n`' + str(self.groups) + '`')
			return True

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

		if found:
			await message.channel.send(message.author.mention + ' There is already a linked minecraft username')
			return
		else:
			minecraft_user = str(message.content).split(' ')[1]
			combo = discord_user + ':' + minecraft_user
			with MCRcon(RCONIP, PASSW) as mcr:
				resp = mcr.command('whitelist add ' + str(minecraft_user))
				mcr.disconnect()

			with open('users.txt', 'a') as f:
				f.write(combo + '\n')
#			await message.channel.send(message.author.mention + ' Added user to whitelist: ' + str(minecraft_user))
			embed=discord.Embed(title="Minecraft Whitelist",
					color=discord.Color.green())

			embed.add_field(name="Discord Username", value='`' + str(discord_user) + '`', inline=True)
			embed.add_field(name="Minecraft Username", value='`' + str(minecraft_user) + '`', inline=True)

			await message.channel.send(embed=embed)

	async def stop(self, message):
		self.loop = False
