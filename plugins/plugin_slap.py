import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Slap():
	name = '!slap'

	desc = 'Slap someone on the server'

	synt = '!slap <username>'

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
		return True

	async def run(self, message, obj_list):
		if len(message.mentions) <= 0:
			return False
			
		new_msg = message.author.mention + ' just slapped '
		for member in message.mentions:
			new_msg = new_msg + member.mention + ', '

		new_msg = new_msg[:-2]

		await message.channel.send(new_msg)

		return True

	async def stop(self, message):
		self.looping = False
