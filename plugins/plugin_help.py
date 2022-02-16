import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Help():
	name = '!help'

	desc = 'Display list of commands or specific command usage'

	synt = '!help [command]'

	looping = False

	group = 'members'

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

		if str(message.content) == '!help':
			for obj in obj_list:
				response = response + str(obj.name) + '\t- ' + str(obj.desc) + '\n'

			await message.channel.send(response)
		elif '!help ' in str(message.content):
			for obj in obj_list:
				if str(message.content).split(' ')[1] == str(obj.name):
					response = response + str(obj.synt)
			await message.channel.send(response)

		return

	async def stop(self, message):
		self.looping = False
