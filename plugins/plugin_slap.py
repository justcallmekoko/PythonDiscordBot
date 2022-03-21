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
			return False
		# Found the user
		else:
			await message.channel.send(message.author.mention + ' just slapped ' + real_member.mention)

		return True

	async def stop(self, message):
		self.looping = False
