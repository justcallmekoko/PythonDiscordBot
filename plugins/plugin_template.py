import os
import json
import discord
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Template():
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	name = '!template'

	desc = 'This does nothing. Developer only'

	synt = '!template [config|get <config>|set <config> <value>|add/remove <config> <value>]'

	is_service = False

	client = None

	looping = False

	guild_confs = []

	full_conf_file = None

	# Server configurable

	group = '@everyone'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	def __init__(self, client = None):
		self.client = client

		# Get each guild configuration
		for entity in os.listdir(self.conf_path):
			if (os.path.isfile(os.path.join(self.conf_path, entity))) and (entity.endswith('_conf.json')):

				# Open guild configuration file
				self.full_conf_file = os.path.join(self.conf_path, entity)
				print(__file__ + ': Loading conf...' + str(entity))

				guild_name = entity.split('_')[0] + entity.split('_')[1]

				# Try to get json stuff
				f = open(self.full_conf_file)
				try:
					json_data = json.load(f)
				except:
					json_data = {}
				f.close()

				# If plugins json doesn't exist, write the key
				if 'plugins' not in json_data:
					print('JSON config does not exist. Creating...')
					data = {}
					data['plugins'] = []
					with open(self.full_conf_file, 'w') as f:
						json.dump(data, f)

				# Get plugin configuration
				with open(self.full_conf_file) as f:
					json_data = json.load(f)

				the_config = None
				for plugin in json_data['plugins']:
					if plugin['name'] == __file__:
						the_config = plugin
						break

				# Plugin config does not exist. Create one
				if the_config == None:
					print('Could not find plugin configuration. Creating...')
					the_config = {}
					the_config['name'] = __file__
					the_config['guild'] = guild_name
					the_config['standard_groups'] = ['@everyone']
					the_config['admin_groups'] = []
					the_config['blacklisted'] = []
					the_config['post_channel'] = ''
					json_data['plugins'].append(the_config)
					with open(self.full_conf_file, 'w') as f:
						json.dump(json_data, f, indent=4)

				self.guild_confs.append(the_config)

		print('\n\nConfigs Loaded:')
		for config in self.guild_confs:
			print('\t' + config['name'] + ': ' + config['guild'])

	def getGuildConfig(self, message, configs):
		guild_config_name = message.guild.name + str(message.guild.id)

		for config in configs:
			if config['guild'] == guild_config_name:
				return config

		return {}

	def hasPerms(self, message, admin_req, configs):
		for role in message.author.roles:
			if (role.permissions.administrator):
				return True

		if admin_req:
			return False
		else:
			user_roles = []
			for role in message.author.roles:
				user_roles.append(role.name)

			
			config = self.getGuildConfig(message, configs)
			if 'standard_groups' not in config:
				return False
			if 'admin_groups' not in config:
				return False

			for user_role in user_roles:
				if user_role in config['standard_groups']:
					return True
				if user_role in config['admin_groups']:
					return True

			return False

	def saveConfig(self, targ_guild):
		for entity in os.listdir(self.conf_path):
			if (os.path.isfile(os.path.join(self.conf_path, entity))) and (entity == str(targ_guild) + '_conf.json'):

				#print('Found target conf file to save')

				full_conf_file = os.path.join(self.conf_path, entity)

				# Get plugin configuration
				with open(full_conf_file) as f:
					json_data = json.load(f)

				
				new_json = {}
				new_json['plugins'] = []

				for that_config in json_data['plugins']:
					found = False
					for this_config in self.guild_confs:
						if (that_config['name'] == this_config['name']) and (that_config['guild'] == this_config['guild']):
							#print('Found target config to save: ' + str(that_config['name']))
							new_json['plugins'].append(this_config)
							found = True
					if not found:
						new_json['plugins'].append(that_config)

				#print('Writing to configuration file: ' + str(full_conf_file))
				with open(full_conf_file, 'w') as f:
					json.dump(new_json, f, indent=4)

				#print(json.dumps(new_json, indent=4, sort_keys=True))

	async def runConfig(self, message, arg, configs):
		if arg[1] == 'config':
			if not self.hasPerms(message, True, configs):
				return True
			embed = discord.Embed(title=self.name,
				color=discord.Color.blue())
			for key in configs[0].keys():
				if isinstance(configs[0][key], str):
					embed.add_field(name=str(key), value='set/get', inline=False)
				else:
					embed.add_field(name=str(key), value='add/remove/get', inline=False)
			
			await message.channel.send(embed=embed)
			return True

		elif arg[1] == 'get':
			if not self.hasPerms(message, True, configs):
				return True
			embed = discord.Embed(title=self.name,
				color=discord.Color.blue())

			the_conf = None
			for conf in configs:
				if conf['guild'] == message.guild.name + str(message.guild.id):
					the_conf = conf
					break

			if the_conf != None:
				if str(arg[2]) in the_conf:
					embed.add_field(name=str(arg[2]), value=str(the_conf[str(arg[2])]), inline=False)
				else:
					embed.add_field(name=str(arg[2]), value='Not Found', inline=False)

			await message.channel.send(embed=embed)
			return True

		elif arg[1] == 'set':
			if not self.hasPerms(message, True, configs):
				return True
			embed = discord.Embed(title=self.name,
				color=discord.Color.blue())

			the_conf = None
			for conf in configs:
				if conf['guild'] == message.guild.name + str(message.guild.id):
					the_conf = conf
					break

			if the_conf != None:
				if str(arg[2]) in the_conf:
					the_conf[str(arg[2])] = arg[3]

			for conf in configs:
				if conf['guild'] == message.guild.name + str(message.guild.id):
					conf = the_conf
					#print(json.dumps(conf, indent=4, sort_keys=True))

			self.saveConfig(message.guild.name + '_' + str(message.guild.id))

			await message.channel.send(embed=embed)
			return True

		return False


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
		if not self.hasPerms(message, False, self.guild_confs):
			await message.channel.send(message.author.mention + ' Permission denied')
			return False

		arg = self.getArgs(message)

		# Check for config stuff
		if arg != None:
			if await self.runConfig(message, arg, self.guild_confs):
				return True

		return True

	async def stop(self, message):
		self.looping = False
