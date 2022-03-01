import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Roleinfo():
	name = '!roleinfo'

	desc = 'Get list of roles and number of users in the roles'

	synt = '!roleinfo'

	looping = False

	group = 'members'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	is_service = False

	client = None

	def __init__(self, client = None):
		self.client = client

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
		roles = message.guild.roles
		output = ''
		for role in roles:
			if role.name == '@everyone':
				continue
			output = output + str(role.name) + ': ' + str(len(role.members)) + '\n'

		await message.channel.send(message.author.mention + '\n' + output)

	async def stop(self, message):
		self.looping = False
