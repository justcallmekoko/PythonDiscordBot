import os
import sys
import json
import discord
import pytz
from datetime import datetime
from logger import logger
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils

class CleanupRaid():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	guild_confs = []

	configutils = None

	name = '!cleanupraid'

	desc = 'Remove all users who joined at a specific datetime except for those with <@exempt role>'

	synt = '!cleanupraid <YYYYMMDD;HH:mm> <@exempt role> / [start/stop] / [config|get <config>|set <config> <value>|add/remove <config> <value>]'

	is_service = True

	client = None

	looping = False

	full_conf_file = None

	time_zone = 'US/Eastern'

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
	default_config['yes_vote'] = {}
	default_config['yes_vote']['value'] = ""
	default_config['yes_vote']['description'] = "The emote to signify 'yes'"
	default_config['no_vote'] = {}
	default_config['no_vote']['value'] = ""
	default_config['no_vote']['description'] = "The emote to signify 'no'"

	# Server configurable

	group = '@everyone'

	admin = False
	
	cheer = -1
	
	cat = 'admin'

	current_draft = []

	running_guilds = []
	
	def __init__(self, client = None):
		self.client = client
		self.configutils = ConfigUtils()

		# Load configuration if it exists
		self.guild_confs = self.configutils.loadConfig(self.conf_path, self.default_config, __file__)


		logger.debug('\n\nConfigs Loaded:')
		for config in self.guild_confs:
			logger.debug('\t' + config['protected']['name'] + ': ' + config['protected']['guild'])

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
	
	async def convert_to_datetime(self, datetime_str):
		# Parse the input string
		date, time = datetime_str.split(';')
		year, month, day = date[:4], date[4:6], date[6:]
		hour, minute = time.split(':')
		
		# Convert the year, month, day, hour, and minute to integers
		year, month, day, hour, minute = map(int, [year, month, day, hour, minute])
		
		# Create and return the datetime object
		return datetime(year, month, day, hour, minute)
	
	async def get_users_by_join_time(self, message, str_time, role):
		usest = pytz.timezone(self.time_zone)
		
		# Convert the join time string to a datetime object in the UTC timezone
		join_time = usest.localize(await self.convert_to_datetime(str_time))

		# Get the guild associated with the message
		guild = message.guild

		# Get a list of members in the guild
		members = guild.members

		# Initialize an empty list to store the filtered members
		filtered_members = []

		# Iterate through the members in the guild
		for member in members:
			# Convert the member's join time to the UTC timezone
			member_join_time = pytz.utc.localize(member.joined_at)
			# Check if the member joined at the specified time and does not have the specified role
			if member_join_time.strftime("%Y%m%d;%H:%M") == join_time.strftime("%Y%m%d;%H:%M") and role not in member.roles:
				# Add the member to the filtered list
				filtered_members.append(member)

			# Print the name and join time of the member
			#logger.debug(str(member.name) + ': ' + str(member_join_time.strftime("%Y%m%d;%H:%M")))
			
		return filtered_members
	
	async def get_role_from_mention(self, message, role_mention):
		# Get the guild associated with the message
		guild = message.guild

		# Get the role ID from the role mention string
		role_id = role_mention.strip("<@&>")

		# Get the role object from the guild
		role = discord.utils.get(guild.roles, id=role_id)

		logger.debug('Got role: ' + str(role.name))

		return role
	
	# Required method for services (content may vary)
	async def getStatus(self, message):
		# Return True if there is a giveaway running in the source message's server
		for index in self.running_guilds:
			if str(message.guild.name) + str(message.guild.id) == index:
				return True

		return False

	async def startService(self):
		if not self.looping:
			self.looping = True
			self.loop_func.start()
			return True
		return False
	
	async def executeEmoji(self, message, cleanup_list = None, do_kick = False):
		if not do_kick:
			await message.channel.send('Canceling cleanup')
		else:
			await message.channel.send('The referenced users have been kicked from the server')
			
		return

	
	@loop(seconds = 5)
	async def loop_func(self):
		if self.looping:
			for guild in self.client.guilds:
				# Only run on guilds that have the service enabled
				if str(guild.name) + str(guild.id) not in self.running_guilds:
					continue

				# Get the current guild conf
				guild_conf = self.configutils.getGuildConfigByGuild(guild, self.guild_confs)

				# Get the current guild drafts
				this_guild_draft = None

				for draft in self.current_draft:
					if draft[0].guild.id == guild.id:
						this_guild_draft = draft
						break

				if this_guild_draft == None:
					continue

				msg = this_guild_draft[0]
				executor = this_guild_draft[1]

				# Check reactions of this draft's message
				targ_reaction = None
				cache_message = await msg.channel.fetch_message(msg.id)

				# Check if the reaction if from the executor
				for reaction in cache_message.reactions:
					async for user in reaction.users():
						if user.id == executor.id:
							targ_reaction = reaction
							break

				if not targ_reaction:
					continue

				# Execute based on reaction
				logger.debug('Executor\'s reaction: ' + str(targ_reaction.emoji))
				if targ_reaction.emoji == guild_conf['yes_vote']['value']:
					logger.debug('Executor confirmed cleanup: ' + str(msg.id))
					await self.executeEmoji(msg, this_guild_draft[2], True)
				elif targ_reaction.emoji == guild_conf['no_vote']['value']:
					logger.debug('Executor canceled cleanup: ' + str(msg.id))
					await self.executeEmoji(msg)
				else:
					logger.debug('Executor did not properly react: ' + str(msg.id))
				
				self.current_draft.remove(this_guild_draft)

				


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
			
		the_guild = str(message.guild.name) + str(message.guild.id)

		# Do service stuff
		if len(arg) == 2:
			# Check if user has admin permissions to run the service
			if not self.configutils.hasPerms(message, True, self.guild_confs):
				await message.channel.send(message.author.mention + ' Permission denied')
				return False

			if str(arg[1]) == 'start':
				if the_guild not in self.running_guilds:
					self.running_guilds.append(the_guild)
					logger.debug('Guilds running ' + str(self.name) + ':')
					for gu in self.running_guilds:
						logger.debug('\t' + gu)
					await message.channel.send(message.author.mention + ' Starting ' + str(self.name))
					return True

			if str(arg[1]) == 'stop':
				if the_guild in self.running_guilds:
					self.running_guilds.remove(the_guild)
					await message.channel.send(message.author.mention + ' Stopping ' + str(self.name))
					logger.debug('Guilds running ' + str(self.name) + ':')
					for gu in self.running_guilds:
						logger.debug('\t' + gu)
					return True

			return False

		# User wants status of service
		elif len(arg) == 1:
			if self.looping:
				await message.channel.send(message.author.mention + ' ' + str(self.name) + ' is running')
			else:
				await message.channel.send(message.author.mention + ' ' + str(self.name) + ' is not running')
			return True
		
		# Only take the first mention in the message
		exempt_role = message.role_mentions[0]
		datetime_str = arg[1]

		cleanup_list = await self.get_users_by_join_time(message, datetime_str, exempt_role)

		guild_conf = self.configutils.getGuildConfig(message, self.guild_confs)

		yes_emote = guild_conf['yes_vote']['value']
		no_emote = guild_conf['no_vote']['value']

		if (yes_emote == '') or (no_emote == ''):
			await message.channel.send(message.author.mention + ', The yes and no emotes have not been set')
			return

		str_users = ''

		logger.debug('Cleanup List:')
		for item in cleanup_list:
			logger.debug('\t' + str(item.name))
			str_users = str_users + str(item.name) + '\n'
		logger.debug('Done with cleanup list')

		# Build message with embed to confirm
		embed = discord.Embed(title="Raid Cleanup Draft",
				color=discord.Color.red())
		
		embed.add_field(name='Executor', value = '```' + str(message.author.name) + '```', inline=False)
		embed.add_field(name='Datetime', value = '```' + str(datetime_str) + '```', inline=True)
		embed.add_field(name='Exempt Role', value = '```' + str(exempt_role.name) + '```', inline=True)
		embed.add_field(name='Users To Kick', value = '```' + str(str_users) + '```', inline=False)
		embed.add_field(name='Confirmation', value = 'Select ' + str(yes_emote) + ' to confirm or ' + str(no_emote) + ' to cancel', inline=False)

		msg = await message.channel.send("Here is your cleanup draft", reference=message, embed=embed)

		await msg.add_reaction(yes_emote)
		await msg.add_reaction(no_emote)

		self.current_draft.append([msg, message.author, cleanup_list])

		#logger.debug('Message ID: ' + str(self.current_draft[0].id) + ' -> User: ' + str(self.current_draft[1].name))

		return True

	async def stop(self, message):
		self.looping = False
