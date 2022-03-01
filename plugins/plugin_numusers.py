import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Numusers():
	name = '!numusers'

	desc = 'Get the number of users in the server'

	synt = '!numusers'

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
		num_users = len(message.guild.members)
		await message.channel.send(message.author.mention + ', There are ' + str(num_users) + ' users on the server')

	async def stop(self, message):
		self.looping = False
