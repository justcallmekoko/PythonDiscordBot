import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Roleinfo():
	name = '!roleinfo'

	desc = 'Get list of roles and number of users in the roles'

	synt = '!roleinfo'

	loop = False

	group = 'members'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False
	
	async def runCheer(self, user, amount):
		return

	async def run(self, message):
		roles = message.guild.roles
		output = ''
		for role in roles:
			if role.name == '@everyone':
				continue
			output = output + str(role.name) + ': ' + str(len(role.members)) + '\n'

		await message.channel.send(message.author.mention + '\n' + output)

	async def stop(self, message):
		self.loop = False
