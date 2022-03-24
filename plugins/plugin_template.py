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

	synt = '!template'

	is_service = False

	client = None

	looping = False

	guild_confs = []

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
				full_conf_file = os.path.join(self.conf_path, entity)
				print(__file__ + ': Loading conf...' + str(entity))

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
					with open(full_conf_file, 'w') as f:
						json.dump(json_data, f, indent=4)

				self.guild_confs.append(the_config)

		print('\n\nConfigs Loaded:')
		for config in self.guild_confs:
			print('\t' + config['name'] + ': ' + config['guild'])

#			print(json.dumps(config, indent=4, sort_keys=True))



	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False

	def getArgs(self, message):
		cmd = str(message.content)
		seg = str(message.content).split(' ')

		if len(seg) > 1:
			return seg
		else:
			return None
	
	async def runCheer(self, user, amount):
		return True

	async def run(self, message, obj_list):
		arg = self.getArgs(message)

		if arg != None:
			if arg[1] == 'config':
				embed = discord.Embed(title=self.name,
					color=discord.Color.blue())
				for key in self.guild_confs[0].keys():
					if isinstance(self.guild_confs[0][key], str):
						embed.add_field(name=str(key), value='set/get', inline=False)
					else:
						embed.add_field(name=str(key), value='add/remove/get', inline=False)
				
				await message.channel.send(embed=embed)

			elif arg[1] == 'get':
				embed = discord.Embed(title=self.name,
					color=discord.Color.blue())

				the_conf = None
				for conf in self.guild_confs:
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

	async def stop(self, message):
		self.looping = False
