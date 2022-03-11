import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Butts():
	name = '!butts'

	desc = 'Use this only if you like butts'

	synt = '!butts'

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
		await message.channel.send(message.author.mention + ' likes butts.')
		return

	async def stop(self, message):
		self.looping = False
