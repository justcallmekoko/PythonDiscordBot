import os
import re
import sys
import openai
import asyncio
import discord
import time
import socket
import threading
from logger import logger
from string import printable
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop
from datetime import datetime
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

# Chicken

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
RCONIP = os.getenv('RCON_IP')
PASSW = os.getenv('RCON_PASSWORD')
OPENAI_KEY = os.getenv('OPENAI_KEY')

global obj_list
global channels_list
global modules
obj_list = []
channels_list = []

path = os.path.join(os.path.dirname(__file__), "plugins")
modules = pkgutil.iter_modules(path=[path])

class CustomClient(discord.Client):
	global obj_list
	global members_list
	global channels_list
	global modules

	conf_path = os.path.join(os.path.dirname(__file__), "plugins/configs")
	#conf_path = os.path.dirname(os.path.abspath(__file__))

	members_list = []
	start_chat_log = '''Human: Hello, who are you?
AI: I am doing great. How can I help you today?
'''
	chat_log = None

	openai.api_key = os.environ.get('OPENAI_KEY')
	completion = openai.Completion()

	def __init__(self, discord_intents: discord.Intents):
		super().__init__(intents=discord_intents)

		logger.debug('Init done')

	def get_class_name(self, mod_name):
		output = ""

		words = mod_name.split("_")[1:]

		for word in words:
			output += word.title()
		return output


	# Bot connects to discord server
	async def on_ready(self):
		logger.debug (f'{self.user} has connected to Discord!')

		for guild in client.guilds:

			logger.debug(
				f'\n{client.user} is connected to the following guild:\n'
				f'{guild.name}(id: {guild.id})\n'
			)

			file_name = str(guild.name) + '_' + str(guild.id) + '_conf.json'

			if not os.path.isfile(os.path.join(self.conf_path, file_name)):
				logger.debug('Guild configuration file not found. Creating...')
				with open(os.path.join(self.conf_path, file_name), 'w'):
					pass

			logger.debug('Member count: ' + str(guild.member_count))

			for member in guild.members:
				members_list.append(member.name)

			logger.debug('len(members_list): ' + str(len(members_list)))

			logger.debug('Guild Roles:')
			for role in guild.roles:
				logger.debug('\t' + role.name)


			print ()

			logger.debug('Guild text channels:')
			for channel in guild.channels:
				if str(channel.type) == 'text':
					channels_list.append(channel)
					logger.debug('\t' + str(channel.name))

			print ()

		# This needs to be AFTER creating/importing guild config files
		for loader, mod_name, ispkg in modules:
			if (mod_name not in sys.modules) and (mod_name.startswith('plugin_')):
			
				loaded_mod = __import__(path+"."+mod_name, fromlist=[mod_name])

				class_name = self.get_class_name(mod_name)
				loaded_class = getattr(loaded_mod, class_name)

				instance = loaded_class(client)
				obj_list.append(instance)

		# Show all plugins and start all services that can be started
		logger.debug('Plugins loaded:')
		for obj in obj_list:
			logger.debug('\t' + str(obj.name))
			if obj.is_service:
				try:
					await obj.startService()
				except:
					continue

	async def on_guild_join(self, guild):
		file_name = str(guild.name) + '_' + str(guild.id) + '_conf.json'

		if not os.path.isfile(os.path.join(self.conf_path, file_name)):
			logger.debug('Guild configuration file not found. Creating...')
			with open(os.path.join(self.conf_path, file_name), 'w'):
				pass

		for obj in obj_list:
			logger.debug('Generating config for ' + str(obj.name))
			obj.generatePluginConfig(file_name)

	async def ask_openai(self, question, chat_log = None):
		if self.chat_log is None:
			self.chat_log = self.start_chat_log
		prompt = f'{chat_log}Human: {question}\nAI:'
		response = self.completion.create(
			prompt=prompt, engine='davinci', stop=['\nHuman'], temperature=0.9,
			top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
			max_tokens=150)
		answer = response.choices[0].text.strip()
		return answer

	async def append_interaction_to_chat_log(self, question, answer, chat_log=None):
		if self.chat_log is None:
			self.chat_log = self.start_chat_log
		return f'{chat_log}Human: {question}\nAI: {answer}\n'

	# Bot received a message on discord server
	async def on_message(self, message):
		try:
			output = '[' + str(datetime.now()) + '][' + str(message.channel.name) + ']'
		except:
			output = '[' + str(datetime.now()) + ']'

		# Ignore bot's own messages
		if message.author == client.user:
			return

		output = output + ' ' + message.author.name + ': ' + message.content

		logger.info(output)

		# Check if having conversation
		if client.user.mentioned_in(message):
			new_question = message.content.replace(client.user.mention + ' ', '')
			logger.debug('Getting openAI response to: ' + str(new_question))

			try:
				answer = await self.ask_openai(new_question, self.chat_log)
			except Exception as e:
				logger.error('Could not prompt OpenAI: ' + str(e))

			logger.info(answer)

			try:
				self.chat_log = await self.append_interaction_to_chat_log(message.content, answer, self.chat_log)
			except Exception as e:
				logger.error('Could not add to chat log')

#			await message.channel.send(message.author.mention + str(answer))
			await message.channel.send(str(answer), reference=message)

		# Work response
		if message.content == '!muster':
			await message.channel.send(message.author.mention + ' Here')

		# Check if multipart command
		if ' ' in str(message.content):
			cmd = str(message.content).split(' ')[0]
		else:
			cmd = str(message.content)

		for obj in obj_list:
			if cmd == obj.name:
				await obj.run(message, obj_list)
				break

intents = discord.Intents.all()
client = CustomClient(intents)

client.run(TOKEN)
client.main.start()
