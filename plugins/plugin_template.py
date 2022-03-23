import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class TargGuild():
	name = None
	groups = []
	blacklist = []
	post_channel = None

	def __init__(self, name):
		self.name = name

	def has_perms(self, message):
		user_groups = []

		for role in message.author.roles:
			user_groups.append(role.name)

		if isinstance(self.groups, str):
			if self.group in user_groups:
				return True
			else:
				return False

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

		for entity in os.listdir(self.conf_path):
			if (os.path.isfile(os.path.join(self.conf_path, entity))) and (entity.endswith('_conf.json')):
				full_conf_file = os.path.join(self.conf_path, entity)
				print(__file__ + ': Loading conf...' + str(entity))
				guild_name = entity.split('_')[0] + entity.split('_')[1]
				targ_guild = TargGuild(guild_name)
				self.guild_confs.append(targ_guild)




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
		print('User ran template')
		return True

	async def stop(self, message):
		self.looping = False
