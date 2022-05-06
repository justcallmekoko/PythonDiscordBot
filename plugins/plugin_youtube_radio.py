import os
import sys
import json
import discord
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class YoutubeRadio():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	guild_confs = []

	configutils = None

	name = '!radio'

	desc = 'Play music from a single YouTube video or playlist in your voice channel'

	synt = '!radio <yt video URL> | pause | resume | stop | [config|get <config>|set <config> <value>|add/remove <config> <value>]'

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

	server_players = []

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

	async def stopPlayer(self, message):
		the_guild = str(message.guild.name) + str(message.guild.id)

		found = False
		for player in self.server_players:
			if player[0] == the_guild:
				found = True
				player[1].stop()
				self.server_players.remove(player)

		if not found:
			await message.channel.send(message.author.mention + ' There are no players running on this server')
			return False

		print('Guilds running a player:')
		for player in self.server_players:
			print('\t' + str(player[0]))

	async def startPlayer(self, message, target_vc, url):
		the_guild = str(message.guild.name) + str(message.guild.id)
		vc = await self.client.join_voice_channel(target_vc)

		for player in self.server_players:
			if player[0] == the_guild:
				await message.channel.send(message.author.mention + ' There is already a player running. Stop it before running another.')
				return False

		player = await vc.create_ytdl_player(url)
		player.start()
		self.server_players.append([the_guild, player])

		print('Guilds running a player:')
		for player in self.server_players:
			print('\t' + str(player[0]))

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

		# User wants to stop the current player
		if str(arg[1]) == 'stop':
			self.stopPlayer(message)
			return True

		# User must want to start a new player
		else:
			# Make sure user is actually in a voice channel
			voice_state = message.author.voice
			if voice_state == None:
				await message.channel.send(message.author.mention + ' You need to be in a voice channel to use this plugin')
				return False
			else:
				target_vc = message.author.voice_channel
				self.startPlayer(message, target_vc, str(arg[1]))
				return True

		return True

	async def stop(self, message):
		self.looping = False
