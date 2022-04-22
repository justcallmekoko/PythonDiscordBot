import os
import sys
import json
import random
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class SearchAndDestroy():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	guild_confs = []

	configutils = None

	name = '!searchanddestroy'

	desc = 'Plant the bomb. The server will have to defuse it.'

	synt = '''`!searchanddestroy [bombplant|bombdefuse <code>]`

The bomb defusal code is randomly generated once it's planted.
The code is only 4 digits long, the digits can repeat themselves,
and it will only contain integers.
If you guess the correct number in the correct index, you will receive an 'X'.
If you guess the correct number in the incorrect index, you will receive an 'O'.
For example, the code is 1234 but you guess 1235.
You would receive an 'XXX'.
If you guess 1243, you would receive an 'XXOO'.

Get the number of guess you have left by typing `!searchanddestroy`'''

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

	bombs = []

	looping = False

	group = '@everyone'

	admin = False
	
	cheer = -1
	
	cat = 'admin'

	defuse_code = ''
	
	remaining_guesses = 10

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

		# Get the guild config for this message
		the_config = self.configutils.getGuildConfig(message, self.guild_confs)
		
		announcements_channel = None

		# Find where the bot will be posting its announcements
		for channel in message.guild.channels:
			if str(channel.mention) == str(the_config['post_channel']['value']):
				announcements_channel = channel
				break

		cmd = str(message.content)
		seg = cmd.split(' ')

		# Check input syntax
		if len(seg) < 1:
			await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
			return

		# Check if there is a bomb for this channel
		check_bomb = None
		for bomb in self.bombs:
			if str(bomb[0]) == str(message.guild.name) + str(message.guild.id):
				check_bomb = bomb
				break

		# Show status of the bomb
		if message.content == self.name:
			if check_bomb != None:
				await message.channel.send(message.author.mention + ' A bomb has been planted. Locate and defuse it. Remaining guesses: ' + str(self.remaining_guesses))
			else:
				await message.channel.send(message.author.mention + ' There are no bombs planted.')
			return

		command = seg[1]

		# Plant the bomb
		if command == 'bombplant':
			# Check if this guild already has a bomb planted
			found = False
			for bomb in self.bombs:
				if str(bomb[0]) == str(message.guild.name) + str(message.guild.id):
					found = True
					break

			# The bomb has already been planted
			if found:
				await message.channel.send(message.author.mention + ' A bomb has *already* been planted')
				return

			# Build this guild's bomb [guild, defuse, remaining, message]
			remaining_guesses = 10
			defuse_code = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
			self.bombs.append([str(message.guild.name) + str(message.guild.id), defuse_code, remaining_guesses, message])

			# Let everyone know the bomb has been planted
			if announcements_channel != None:
				await announcements_channel.send(message.author.mention + ' has planted the bomb')
			else:
				await message.channel.send(message.author.mention + ' has planted the bomb')

			# Show backend what bombs are active
			print('Planted bombs:')
			for bomb in self.bombs:
				print('\t' + str(bomb))

		# Defuse the bomb
		if command == 'bombdefuse':
			# Check if there is even a bomb planted for this guild
			check_bomb = None
			for bomb in self.bombs:
				if str(bomb[0]) == str(message.guild.name) + str(message.guild.id):
					check_bomb = bomb
					break

			# Exit if no bomb
			if check_bomb == None:
				return

			xs = 0
			oss = 0
			code_guess = seg[2]

			code_guess_list = list(code_guess)
			defuse_code_list = list(check_bomb[1])

			# User did not send numeric code
			if not code_guess.isnumeric():
				await message.channel.send(message.author.mention + ' The code may only contain numbers.')

			# Bomb has been defused
			if str(code_guess) == str(check_bomb[1]):
				if announcements_channel != None:
					await announcements_channel.send(message.author.mention + ' has defused the bomb!')
				else:
					await message.channel.send(message.author.mention + ' has defused the bomb!')
					
				self.bombs.remove(check_bomb)

				# Show backend what bombs are active
				print('Planted bombs:')
				for bomb in self.bombs:
					print('\t' + str(bomb))
					
				return True

			for i in range(0, 4):
				# Correct integer, correct index
				if code_guess_list[i] == defuse_code_list[i]:
					xs = xs + 1
					code_guess_list[i] = "-1"
					defuse_code_list[i] = "-1"

			try:
				while True:
					code_guess_list.remove('-1')
			except ValueError:
				pass

			try:
				while True:
					defuse_code_list.remove('-1')
			except ValueError:
				pass

			print('Comparing: ' + str(code_guess_list) + ' | ' + str(defuse_code_list))

			for i in range(0, len(defuse_code_list)):
				# Correct integer, incorrect index
				try:
					if code_guess_list[i] in defuse_code_list:
						oss = oss + 1
						defuse_code_list.remove(code_guess_list[i])
						code_guess_list[i] = '-1'
				except:
					fuck = True

			check_bomb[2] = check_bomb[2] - 1

			# Guesses used up
			if check_bomb[2] <= 0:
				if announcements_channel != None:
					await announcements_channel.send(message.author.mention + ' You are out of guesses. The bomb has detonated!')

				await message.channel.send(message.author.mention + ' You are out of guesses. The bomb has detonated!')
				self.bombs.remove(check_bomb)

				# Show backend what bombs are active
				print('Planted bombs:')
				for bomb in self.bombs:
					print('\t' + str(bomb))

				return False

			response_string = ('X' * xs) + ('O' * oss) + ' remaining attempts: ' + str(check_bomb[2])

			await message.channel.send(message.author.mention + ' ' + str(response_string))

		return True

	async def stop(self, message):
		self.looping = False
