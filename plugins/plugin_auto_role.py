import os
import sys
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.tasks import loop
from discord.utils import get
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class AutoRole():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	guild_confs = []

	configutils = None

	name = '!autorole'

	desc = 'Apply roles automatically based on time spent in server'

	synt = '!autorole [config|get <config>|set <config> <value>|add/remove <config> <value>|start|stop]'

	looping = False

	group = '@everyone'

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
	default_config['time_groups'] = {}
	default_config['time_groups']['value'] = []
	default_config['time_groups']['description'] = "List of roles and days required to join roles 'days:group'"

	running_guilds = []

	admin = False
	
	cheer = -1
	
	cat = 'admin'

	is_service = True

	client = None

	def __init__(self, client = None):
		self.client = client
		self.configutils = ConfigUtils()

		# Load configuration if it exists
		self.guild_confs = self.configutils.loadConfig(self.conf_path, self.default_config, __file__)


		print('\n\nConfigs Loaded:')
		for config in self.guild_confs:
			print('\t' + config['protected']['name'] + ': ' + config['protected']['guild'])

#		loop = asyncio.new_event_loop()
#		asyncio.set_event_loop(loop)

#		self.looping = True
#		self.loop_func.start()


	def getArgs(self, message):
		cmd = str(message.content)
		seg = str(message.content).split(' ')

		if len(seg) > 1:
			return seg
		else:
			return None


	@loop(seconds = 3600)
	async def loop_func(self):
		if self.looping:
			# Loop through all guilds running this service
			for the_guild_string in self.running_guilds:
				# Get the roles and days
				the_config = self.configutils.getGuildConfigByGuildConfigName(the_guild_string, self.guild_confs)

				# Get the actual guild
				guild = None
				for g in self.client.guilds:
					list_guild_string = str(g.name) + str(g.id)
					if list_guild_string == the_guild_string:
						guild = g

				# Skip to next guild if we can't find the current guild in client
				if guild == None:
					continue

				# Loop through all members in the guild
				print('Running auto role check...')
				for member in guild.members:
					if not self.looping:
						print('Exiting from auto role check...')
						self.loop_func.stop()
						return
					# Get days since member joined server
					mem_join = member.joined_at
					now = datetime.now()
					#print(str(mem_join) + ' - ' + str(now))
					join_days = (now - mem_join).days

					# Check days list and the role for those days
					for day_role_group in the_config['time_groups']['value']:
						# Unpack list of days to roles
						role_index = day_role_group.split(':')

						# Check if user surpassed days
						if int(join_days) >= int(role_index[0]):
							the_role = None
							# Get the actual role from the guild using the saved mention
							for role in guild.roles:
								if role.mention == str(role_index[1]):
									the_role = role
									#print('Found the role: ' + str(the_role.name))
									break
							if the_role == None:
								continue

							if the_role in member.roles:
								continue

	#						role = get(self.global_message.guild.roles, name = str(role_index[1]))
							await member.add_roles(the_role)
							print('Gave \'' + str(role_index[1]) + '\' to ' + member.name)

	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False

	async def startService(self):
		if not self.looping:
			self.looping = True
			self.loop_func.start()
			return True
		return False
	
	async def runCheer(self, user, amount):
		return

	async def run(self, message, obj_list):
		# Permissions check
		if not self.configutils.hasPerms(message, True, self.guild_confs):
			await message.channel.send(message.author.mention + ' Permission denied')
			return False

		# Parse args
		arg = self.getArgs(message)

		# Config set/get check
		if arg != None:
			if await self.configutils.runConfig(message, arg, self.guild_confs, self.conf_path):
				return True


		self.global_message = message
		cmd = message.content
		if len(cmd.split(' ')) > 1:
			arg = cmd.split(' ')[1]
		else:
			arg = None

		if cmd == '!autorole':
			if self.looping:
				await message.channel.send(message.author.mention + ' autorole is running')
			else:
				await message.channel.send(message.author.mention + ' autorole is not running')
		if arg == None:
			return

		the_guild = str(message.guild.name) + str(message.guild.id)

		if str(arg) == 'start':
			if the_guild not in self.running_guilds:
				#self.looping = True
				self.running_guilds.append(the_guild)
				print('Guilds running autorole:')
				for gu in self.running_guilds:
					print('\t' + gu)
				await message.channel.send(message.author.mention + ' Starting autorole')
				#self.loop_func.start()

		if str(arg) == 'stop':
			if the_guild in self.running_guilds:
				#self.looping = False
				self.running_guilds.remove(the_guild)
				await message.channel.send(message.author.mention + ' Stopping autorole')
				#self.loop_func.stop()
		return

	async def stop(self, message):
		self.looping = False
