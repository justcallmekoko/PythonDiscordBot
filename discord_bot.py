import os
import re
import sys
import asyncio
import discord
import time
import socket
import threading
from string import printable
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop
import random
import pkgutil

sys.dont_write_bytecode = True

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
RCONIP = os.getenv('RCON_IP')
PASSW = os.getenv('RCON_PASSWORD')

global obj_list
global channels_list
obj_list = []
channels_list = []

path = os.path.join(os.path.dirname(__file__), "plugins")
modules = pkgutil.iter_modules(path=[path])

class CustomClient(discord.Client):
	global obj_list
	global members_list
	global channels_list

	members_list = []

	def __init__(self, discord_intents: discord.Intents):
		super().__init__(intents=discord_intents)
		print('Init done')


	# Bot connects to discord server
	async def on_ready(self):
		print (f'{self.user} has connected to Discord!')

		for guild in client.guilds:
			if guild.name == GUILD:
				break

		print(
			f'\n{client.user} is connected to the following guild:\n'
			f'{guild.name}(id: {guild.id})\n'
		)

		print('Member count: ' + str(guild.member_count))

		for member in guild.members:
			members_list.append(member.name)

		print('len(members_list): ' + str(len(members_list)))

		print ('Guild Roles:')
		for role in guild.roles:
			print('\t' + role.name)


		print ()

		print('Guild text channels:')
		for channel in guild.channels:
			if str(channel.type) == 'text':
				channels_list.append(channel)
				print('\t' + str(channel.name))

		print ()



	# Member joins the discord server
	async def on_member_join(self, member):
		print(f'{member.name}, welcome to the WillStunForFood server. Be sure to check out the "rules" channel so you can pick your roles. If you would like to support me, consider following me on Twitch at https://twitch.tv/willstunforfood')
		await member.create_dm()
		await member.dm_channel.send(f'{member.name}, welcome to the WillStunForFood server. Be sure to check out the "rules" channel so you can pick your roles. If you would like to support me, consider following me on Twitch at https://twitch.tv/willstunforfood')

	# Bot received a message on discord server
	async def on_message(self, message):
		admin = False

		user_groups = []

		output = ''

		# Get all guilds
		for guild in client.guilds:
                        if guild.name == GUILD:
                                break

		# Ignore bot's own messages
		if message.author == client.user:
			return

		# Check if this is admin
		try:
			for role in message.author.roles:
				output = output + '['

				user_groups.append(str(role.name))

				if (role.permissions.administrator) and (role.guild.id == guild.id):
					admin = True
					output = output + T
				elif str(role.name) == 'Twitch Subscriber':
					output = output + C
				else:
					output = output + W

				output = output + role.name + W + ']'
		except Exception as e:
			output = output + '[' + str(e) + ']'

		output = output + ' ' + message.author.name + ': ' + message.content

		print (output)

		# Work response
#		if client.user.mentioned_in(message):
#			await message.channel.send(message.author.mention + ' Don\'t talk to me')

		if message.content == '!muster':
                        await message.channel.send(message.author.mention + ' Here')

		# Check plugins
		found = False

		# Check if multipart command
		if ' ' in str(message.content):
			cmd = str(message.content).split(' ')[0]
		else:
			cmd = str(message.content)

		# Start reponse
		response = message.author.mention + '\n'

		# Check if general help
		if str(message.content) == '!help':
			found = True
			for obj in obj_list:
				response = response + str(obj.name) + '\t- ' + str(obj.desc) + '\n'

			await message.channel.send(response)
		elif '!help ' in str(message.content):
			found = True
			for obj in obj_list:
				if str(message.content).split(' ')[1] == str(obj.name):
					response = response + str(obj.synt)
			await message.channel.send(response)

		for obj in obj_list:
			if cmd == obj.name:
				found = True
				if obj.admin and not admin:
					await message.channel.send(message.author.mention + ' ' + str(cmd) + ' only admins may run this command')
					break

				if obj.group not in user_groups:
					await message.channel.send(message.author.mention + ' ' + str(cmd) + ' You must be a member of ' + obj.group + ' to run this command')
					break

				await obj.run(message)
				break

#		try:
#			if list(str(cmd))[0] == '!' and not found:
#				await message.channel.send(message.author.mention + ' ' + str(cmd) + ' is not a recognized command')
#		except Exception as e:
#			print('Hit exception parsing message: ' + str(e))


def get_class_name(mod_name):
	output = ""

	words = mod_name.split("_")[1:]

	for word in words:
		output += word.title()
	return output

for loader, mod_name, ispkg in modules:
	if mod_name not in sys.modules:

		loaded_mod = __import__(path+"."+mod_name, fromlist=[mod_name])

		class_name = get_class_name(mod_name)
		loaded_class = getattr(loaded_mod, class_name)

		instance = loaded_class()
		obj_list.append(instance)

intents = discord.Intents.all()
client = CustomClient(intents)
client.run(TOKEN)
client.main.start()
