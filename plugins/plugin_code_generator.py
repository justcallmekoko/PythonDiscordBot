import os
import sys
import json
import discord
import openai
from logger import logger
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

sys.path.append(os.path.abspath('utils'))

from utils.config_utils import ConfigUtils
from utils.Examples import examples

class Example():
	"""Stores an input, output pair and formats it to prime the model."""

	def __init__(self, inp, out):
		self.input = inp
		self.output = out

	def get_input(self):
		"""Returns the input of the example."""
		return self.input

	def get_output(self):
		"""Returns the intended output of the example."""
		return self.output

	def format(self):
		"""Formats the input, output pair."""
		return f"input: {self.input}\noutput: {self.output}\n"
	
class GPT:
	"""The main class for a user to interface with the OpenAI API.
	A user can add examples and set parameters of the API request."""

	def __init__(self, engine='code-davinci-002',
				temperature=0.5,
				max_tokens=150):
		self.examples = []
		self.engine = engine
		self.temperature = temperature
		self.max_tokens = max_tokens

	def add_example(self, ex):
		"""Adds an example to the object. Example must be an instance
		of the Example class."""
		assert isinstance(ex, Example), "Please create an Example object."
		self.examples.append(ex.format())

	def get_prime_text(self):
		"""Formats all examples to prime the model."""
		return '\n'.join(self.examples) + '\n'

	def get_engine(self):
		"""Returns the engine specified for the API."""
		return self.engine

	def get_temperature(self):
		"""Returns the temperature specified for the API."""
		return self.temperature

	def get_max_tokens(self):
		"""Returns the max tokens specified for the API."""
		return self.max_tokens

	def craft_query(self, prompt):
		"""Creates the query for the API request."""
		return self.get_prime_text() + "input: " + prompt + "\n"

	def submit_request(self, prompt):
		"""Calls the OpenAI API with the specified parameters."""
		response = openai.Completion.create(engine=self.get_engine(),
											prompt=self.craft_query(prompt),
											max_tokens=self.get_max_tokens(),
											temperature=self.get_temperature(),
											top_p=1,
											n=1,
											stream=False,
											stop="\ninput:")
		return response

	def get_top_reply(self, prompt):
		"""Obtains the best result as returned by the API."""
		response = self.submit_request(prompt)
		return response['choices'][0]['text']



class CodeGenerator():
	# Required for all plugins
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	guild_confs = []

	configutils = None

	name = '!codegenerator'

	desc = 'Ask it for some Python code. (TESTING)'

	synt = '!codegenerator [<prompt>][config|get <config>|set <config> <value>|add/remove <config> <value>]'

	is_service = False

	client = None

	looping = False

	full_conf_file = None

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

	# Server configurable

	group = '@everyone'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	gpt = None

	def __init__(self, client = None):
		self.client = client
		self.configutils = ConfigUtils()

		load_dotenv()
		openai.api_key = os.environ.get('OPENAI_KEY')
		self.gpt = GPT(engine="code-davinci-002", temperature=0.5, max_tokens=500)

		# Load configuration if it exists
		self.guild_confs = self.configutils.loadConfig(self.conf_path, self.default_config, __file__)

		for example in examples:
			logger.debug('Loading example: ' + example[0])
			self.gpt.add_example(Example(example[0], example[1]))


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
	
	async def get_post_channel(self, message, the_config):
		# Find where the bot will be posting its announcements
		for channel in message.guild.channels:
			try:
				if str(channel.mention) == str(the_config['post_channel']['value']):
					logger.debug('Found post_channel: ' + str(channel.mention))
					return channel
			except:
				return None
		return None

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
			
		output = self.gpt.submit_request(message.content.replace(self.name + ' ', ''))

		new_output = ''
		if output.choices[0].text.startswith('output: '):
			new_output = output.choices[0].text[9:]

		embed = discord.Embed(title="Code Reponse",
				color=discord.Color.green())
		
		embed.add_field(name='Completion Tokens', value='```' + str(output.usage.completion_tokens) + '```', inline=True)
		embed.add_field(name='Prompt Tokens', value='```' + str(output.usage.prompt_tokens) + '```', inline=True)
		embed.add_field(name='Total Tokens', value='```' + str(output.usage.total_tokens) + '```', inline=True)
		embed.add_field(name='Code Body', value='```Python\n' + new_output + '```', inline=False)

		the_config = self.configutils.getGuildConfig(message, self.guild_confs)

		local_post_channel = await self.get_post_channel(message, the_config)

		if not local_post_channel:
			await message.channel.send("Here is your code", reference=message, embed=embed)
		else:
			await local_post_channel.send("Here is your code", reference=message, embed=embed)

		return True

	async def stop(self, message):
		self.looping = False
