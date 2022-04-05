import os
import sys
import json
import discord
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class UserInfo():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	name = '!userinfo'

	desc = 'Get information regarding discord user'

	synt = '!userinfo <user>|[config|get <config>|set <config> <value>|add/remove <config> <value>]'

	looping = False

	group = '@everyone'

	admin = False

	guild_confs = []

	configutils = None
	
	cheer = -1
	
	cat = 'admin'

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

		target_user = str(message.content).split(' ')[1]

		# Search for the user
		found = False

		for member in message.guild.members:
			if str(member.display_name) == target_user:
				found = True
				real_member = member
				break

		# Did not find the user
		if not found:
			await message.channel.send(message.author.mention + ', The user was not found')
		# Found the user
		else:
			embed=discord.Embed(title="User Info",
					color=discord.Color.blue())

			member_roles = []
			member_perms = ''
			mem_join = real_member.joined_at
			now = datetime.now()
			print(str(mem_join) + ' - ' + str(now))
			join_days = (now - mem_join).days
			for role in real_member.roles:
				member_roles.append(role.name)
			for perm in real_member.permissions_in(message.channel):
				if perm[1]:
					member_perms = member_perms + str(perm[0]) + '\n'

#			await message.channel.send(message.author.mention + ', ' + real_member.mention + ' joined ' + str(join_days) + ' day(s) ago')
			embed.add_field(name="Username", value='`' + str(real_member.name) + '#' + str(real_member.discriminator) + '`', inline=True)
			embed.add_field(name="User ID", value='`' + str(real_member.id) + '`', inline=True)
			embed.add_field(name="Nickname", value='`' + str(real_member.display_name) + '`', inline=True)

			embed.add_field(name="Created", value='```' + str(real_member.created_at) + '```', inline=False)

			embed.add_field(name="Joined", value='```' + str(mem_join) + '```', inline=True)
			embed.add_field(name="Days on server", value='```' + str(join_days) + '```', inline=True)

			embed.add_field(name="Roles", value='```' + str(member_roles) + '```', inline=False)

			embed.add_field(name="Permissions in this channel", value='```' + str(member_perms) + '```', inline=False)

			await message.channel.send(embed=embed)

		return

	async def stop(self, message):
		self.looping = False
