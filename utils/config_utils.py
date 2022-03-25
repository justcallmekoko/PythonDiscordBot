import os
import json
import discord
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class ConfigUtils():
	def loadConfig(self, conf_path, default_config, file_name):
		configs = []

		for entity in os.listdir(conf_path):
			# Make sure the file is a config file
			if (os.path.isfile(os.path.join(conf_path, entity))) and (entity.endswith('_conf.json')):
				guild_name = entity.split('_')[0] + entity.split('_')[1]

				full_conf_file = os.path.join(conf_path, entity)
				print(file_name + ': Loading conf...' + str(entity))

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
					print('JSON config does not exist. Creating...')
					data = {}
					data['plugins'] = []
					with open(full_conf_file, 'w') as f:
						json.dump(data, f)

				# Get plugin configuration
				with open(full_conf_file) as f:
					json_data = json.load(f)

				the_config = None
				for plugin in json_data['plugins']:
					if plugin['name'] == file_name:
						the_config = plugin
						break

				if the_config == None:
					print('Could not find plugin configuration. Creating...')
					default_config['guild'] = guild_name
					json_data['plugins'].append(default_config)
					with open(full_conf_file, 'w') as f:
						json.dump(json_data, f, indent=4)
					configs.append(default_config)
				else:
					configs.append(the_config)

		return configs

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

	def saveConfig(self, targ_guild, configs, conf_path):
		for entity in os.listdir(conf_path):
			if (os.path.isfile(os.path.join(conf_path, entity))) and (entity == str(targ_guild) + '_conf.json'):

				print('Found target conf file to save')

				full_conf_file = os.path.join(conf_path, entity)

				# Get plugin configuration
				with open(full_conf_file) as f:
					json_data = json.load(f)

				
				new_json = {}
				new_json['plugins'] = []

				for that_config in json_data['plugins']:
					found = False
					for this_config in configs:
						if (that_config['name'] == this_config['name']) and (that_config['guild'] == this_config['guild']):
							print('Found target config to save: ' + str(that_config['name']))
							new_json['plugins'].append(this_config)
							found = True
					if not found:
						new_json['plugins'].append(that_config)

				print('Writing to configuration file: ' + str(full_conf_file))
				with open(full_conf_file, 'w') as f:
					json.dump(new_json, f, indent=4)

				#print(json.dumps(new_json, indent=4, sort_keys=True))

	async def runConfig(self, message, arg, configs, conf_path):
		if arg[1] == 'config':
			if not self.hasPerms(message, True, configs):
				return True
			embed = discord.Embed(title=str(arg[0]),
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
			embed = discord.Embed(title=str(arg[0]),
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
			embed = discord.Embed(title=str(arg[0]),
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

			self.saveConfig(message.guild.name + '_' + str(message.guild.id), configs, conf_path)

			await message.channel.send(embed=embed)
			return True

		return False
