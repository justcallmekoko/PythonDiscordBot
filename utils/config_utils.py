import os
import copy
import json
import discord
from logger import logger
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class ConfigUtils():
	protected_key = 'protected'
	backend_key = 'backend'

	def generateConfig(self, conf_path, default_config, file_name, plugin_name):
		guild_name = file_name.replace('_config.json', '').replace('_', '')
		configs = []
		full_conf_file = os.path.join(conf_path, file_name)

		# Try to get json stuff
		f = open(full_conf_file)
		try:
			json_data = json.load(f)
		except:
			json_data = {}
		f.close()

		# If plugins json doesn't exist, write the key
		if 'plugins' not in json_data:
			logger.debug('JSON config does not exist. Creating...')
			data = {}
			data['plugins'] = []
			with open(full_conf_file, 'w') as f:
				json.dump(data, f)

		# Get plugin configuration
		with open(full_conf_file) as f:
			json_data = json.load(f)

		the_config = None
		for plugin in json_data['plugins']:
			if plugin[self.protected_key]['name'] == file_name:
				the_config = plugin
				break

		if the_config == None:
			new_conf = None
			new_conf = copy.copy(default_config)
			new_conf[self.protected_key]['guild'] = guild_name
			logger.debug('Could not find plugin configuration. Creating...' + str(new_conf[self.protected_key]['guild']))
			configs.append(copy.deepcopy(new_conf)) # Needs to be deepcopy or all list items are changed
			json_data['plugins'].append(new_conf)
			with open(full_conf_file, 'w') as f:
				json.dump(json_data, f, indent=4)
		else:
			configs.append(the_config)

		return configs


	def loadConfig(self, conf_path, default_config, file_name):
		configs = []

		for entity in os.listdir(conf_path):
			# Make sure the file is a config file
			if (os.path.isfile(os.path.join(conf_path, entity))) and (entity.endswith('_conf.json')):
				guild_name = entity.split('_')[0] + entity.split('_')[1]

				full_conf_file = os.path.join(conf_path, entity)
				logger.debug(file_name + ': Loading conf...' + str(entity))

				guild_name = entity.split('_')[0] + entity.split('_')[1]

				# Try to get json stuff
				f = open(full_conf_file)
				try:
					json_data = json.load(f)
				except:
					json_data = {}
				f.close()

				# If plugins json doesn't exist, write the key
				if 'plugins' not in json_data:
					logger.debug('JSON config does not exist. Creating...')
					data = {}
					data['plugins'] = []
					with open(full_conf_file, 'w') as f:
						json.dump(data, f)

				# Get plugin configuration
				with open(full_conf_file) as f:
					json_data = json.load(f)

				the_config = None
				for plugin in json_data['plugins']:
					if plugin[self.protected_key]['name'] == file_name:
						the_config = plugin
						break

				if the_config == None:
					new_conf = None
					new_conf = copy.copy(default_config)
					new_conf[self.protected_key]['guild'] = guild_name
					logger.debug('Could not find plugin configuration. Creating...' + str(new_conf[self.protected_key]['guild']))
					configs.append(copy.deepcopy(new_conf)) # Needs to be deepcopy or all list items are changed
					json_data['plugins'].append(new_conf)
					with open(full_conf_file, 'w') as f:
						json.dump(json_data, f, indent=4)
				else:
					configs.append(the_config)

		return configs

	def getGuildConfigByGuildConfigName(self, guild_config_name, configs):
		for config in configs:
			if config[self.protected_key]['guild'] == guild_config_name:
				return config

		return {}

	def getGuildConfigByGuild(self, guild, configs):
		guild_config_name = guild.name + str(guild.id)

		for config in configs:
			if config[self.protected_key]['guild'] == guild_config_name:
				return config

		return {}

	def getGuildConfig(self, message, configs):
		guild_config_name = message.guild.name + str(message.guild.id)

		for config in configs:
			#print(config[self.protected_key]['guild'])
			if config[self.protected_key]['guild'] == guild_config_name:
				#print('Found config')
				return config

		return {}

	def hasPermsUser(self, message, user, admin_req, configs):
		for role in user.roles:
			if (role.permissions.administrator):
				#print(role.name + ' has administrator permissions')
				return True

		if admin_req:
			return False
		else:
			user_roles = []
			for role in user.roles:
				user_roles.append(role.name)

			
			config = self.getGuildConfig(message, configs)
			if 'standard_groups' not in config:
				return False
			if 'admin_groups' not in config:
				return False

			# Check if user is blacklisted
			for role in user.roles:
				if 'value' in config['blacklisted']:
					if role.mention in config['blacklisted']['value']:
						#print(str(role.mention) + ' found in blacklisted')
						return False

			# Check role objects
			for role in user.roles:
				if 'value' in config['standard_groups']:
					if role.mention in config['standard_groups']['value']:
						#print(str(role.mention) + ' found in standard_groups')
						return True
				if 'value' in config['admin_groups']:
					if role.mention in config['admin_groups']['value']:
						#print(str(role.mention) + ' found in admin_groups')
						return True

			# Check string roles (old)
			for user_role in user_roles:
				if 'value' in config['standard_groups']:
					if user_role in config['standard_groups']['value']:
						#print(user_role + ' found in standard_groups')
						return True
				if 'value' in config['admin_groups']:
					if user_role in config['admin_groups']['value']:
						#print(user_role + ' found in admin_groups')
						return True

			return False

	def hasPerms(self, message, admin_req, configs):
		for role in message.author.roles:
			if (role.permissions.administrator):
				#print(role.name + ' has administrator permissions')
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

			# Check if user is blacklisted
			for role in message.author.roles:
				if 'value' in config['blacklisted']:
					if role.mention in config['blacklisted']['value']:
						#print(str(role.mention) + ' found in blacklisted')
						return False

			# Check role objects
			for role in message.author.roles:
				if 'value' in config['standard_groups']:
					if role.mention in config['standard_groups']['value']:
						#print(str(role.mention) + ' found in standard_groups')
						return True
				if 'value' in config['admin_groups']:
					if role.mention in config['admin_groups']['value']:
						#print(str(role.mention) + ' found in admin_groups')
						return True

			# Check string roles (old)
			for user_role in user_roles:
				if 'value' in config['standard_groups']:
					if user_role in config['standard_groups']['value']:
						#print(user_role + ' found in standard_groups')
						return True
				if 'value' in config['admin_groups']:
					if user_role in config['admin_groups']['value']:
						#print(user_role + ' found in admin_groups')
						return True

			return False

	def saveConfig(self, targ_guild, configs, conf_path):
		for entity in os.listdir(conf_path):
			if (os.path.isfile(os.path.join(conf_path, entity))) and (entity == str(targ_guild) + '_conf.json'):

				logger.debug('Found target conf file to save')

				full_conf_file = os.path.join(conf_path, entity)

				# Get plugin configuration
				with open(full_conf_file) as f:
					json_data = json.load(f)

				
				new_json = {}
				new_json['plugins'] = []

				for that_config in json_data['plugins']:
					found = False
					for this_config in configs:
						# This if statement is really fucking disgusting
						if (that_config[self.protected_key]['name'] == this_config[self.protected_key]['name']) and (that_config[self.protected_key]['guild'] == this_config[self.protected_key]['guild']):
							logger.debug('Found target config to save: ' + str(that_config[self.protected_key]['name']))
							new_json['plugins'].append(this_config)
							found = True
					if not found:
						new_json['plugins'].append(that_config)

				logger.debug('Writing to configuration file: ' + str(full_conf_file))
				with open(full_conf_file, 'w') as f:
					json.dump(new_json, f, indent=4)

				#print(json.dumps(new_json, indent=4, sort_keys=True))

	async def runConfig(self, message, arg, configs, conf_path):
		# Get all available config keys
		if arg[1] == 'config':
			if not self.hasPerms(message, True, configs):
				return True
			embed = discord.Embed(title=str(arg[0]),
				color=discord.Color.blue())

			the_config = self.getGuildConfig(message, configs)

			for key in the_config.keys():
				if (key == self.protected_key) or (key == self.backend_key):
					continue
				if isinstance(the_config[key]['value'], str):
					embed.add_field(name=str(key), value=str(the_config[key]['description'] + '\nset/get'), inline=False)
				else:
					embed.add_field(name=str(key), value=str(the_config[key]['description'] + '\nadd/remove/get'), inline=False)
			
			await message.channel.send(embed=embed)
			return True

		# Get a config key's value
		elif arg[1] == 'get':
			if not self.hasPerms(message, True, configs):
				return True
			embed = discord.Embed(title=str(arg[0]),
				color=discord.Color.blue())

			the_conf = None
			for conf in configs:
				if conf[self.protected_key]['guild'] == message.guild.name + str(message.guild.id):
					the_conf = conf
					break

			if the_conf != None:
				if str(arg[2]) in the_conf:
					embed.add_field(name=str(arg[2]), value=str(the_conf[str(arg[2])]['value']), inline=False)
				else:
					embed.add_field(name=str(arg[2]), value='Not Found', inline=False)
			else:
				logger.debug('Did not find configuration')

			await message.channel.send(embed=embed)
			return True

		# Set a single value key
		elif arg[1] == 'set':
			# Check if the user has permissions to do this
			if not self.hasPerms(message, True, configs):
				return True
			embed = discord.Embed(title=str(arg[0]),
				color=discord.Color.blue())

			# Get the specific guild config
			the_conf = None
			for conf in configs:
				if conf[self.protected_key]['guild'] == message.guild.name + str(message.guild.id):
					the_conf = conf
					break

			if the_conf != None:
				# Check if key exists, is not protected, and is not a list
				if (str(arg[2]) in the_conf) and (str(arg[2]) != self.protected_key) and (not isinstance(the_conf[str(arg[2])]['value'], list)):
					the_conf[str(arg[2])]['value'] = arg[3]
				else:
					return True

			# Set the config in the objects list of configs
			for conf in configs:
				if conf[self.protected_key]['guild'] == message.guild.name + str(message.guild.id):
					conf = the_conf
					#print(json.dumps(conf, indent=4, sort_keys=True))

			# Save the new config and reply with message
			self.saveConfig(message.guild.name + '_' + str(message.guild.id), configs, conf_path)

			if 'value' in the_conf[str(arg[2])]:
				embed.add_field(name=str(arg[2]), value=str(the_conf[str(arg[2])]['value']), inline=False)
			else:
				embed.add_field(name=str(arg[2]), value=str(the_conf[str(arg[2])]), inline=False)

			await message.channel.send(embed=embed)
			return True

		# Add a value to a list key
		elif (arg[1] == 'add') or (arg[1] == 'remove'):
			# Check if the user has permissions to do this
			if not self.hasPerms(message, True, configs):
				return True
			embed = discord.Embed(title=str(arg[0]),
				color=discord.Color.blue())

			# Get the specific guild config
			the_conf = None
			for conf in configs:
				if conf[self.protected_key]['guild'] == message.guild.name + str(message.guild.id):
					the_conf = conf
					break

			if the_conf != None:
				# Make sure key exists and is a list
				if (str(arg[2]) in the_conf) and (isinstance(the_conf[str(arg[2])]['value'], list)) and (arg[1] == 'add'):
					the_conf[str(arg[2])]['value'].append(str(arg[3]))
				elif (str(arg[2]) in the_conf) and (isinstance(the_conf[str(arg[2])]['value'], list)) and (arg[1] == 'remove'):
					the_conf[str(arg[2])]['value'].remove(str(arg[3]))
				else:
					return True
			else:
				return True

			# Set the config in the objects list of configs
			for conf in configs:
				if conf[self.protected_key]['guild'] == message.guild.name + str(message.guild.id):
					conf = the_conf

			# Save the new config and reply with message
			self.saveConfig(message.guild.name + '_' + str(message.guild.id), configs, conf_path)

			embed.add_field(name=str(arg[2]), value=str(the_conf[str(arg[2])]['value']), inline=False)

			await message.channel.send(embed=embed)
			return True
		return False
