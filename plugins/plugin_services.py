import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Services():
	name = '!services'

	desc = 'Displays a list of services and their status'

	synt = '!services'

	looping = False

	group = 'Moderator'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	is_service = False

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
		response = message.author.mention + '\n'

		for obj in obj_list:
			if obj.is_service:
				response = response + str(obj.name)
				if obj.looping:
					response = response + ': `running`\n'
				else:
					response = response + ': `not running`\n'

		await message.channel.send(response)

		return

	async def stop(self, message):
		self.looping = False
