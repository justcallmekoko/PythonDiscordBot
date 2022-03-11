import os
import json
import discord
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class SetStatus():
	name = '!setstatus'

	desc = 'Set the status of the bot'

	synt = '!setstatus <status>'

	looping = False

	group = 'Owner'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
	is_service = False

	client = None

	status = None

	def __init__(self, client):
		self.client = client
		print(str(self.client))

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
		cmd = str(message.content)
		seg = str(message.content).split(' ')

		test_name = ''
		for i in range(1, len(seg)):
			test_name = test_name + seg[i] + ' '
		self.status = test_name[:-1]

		await self.client.change_presence(activity = discord.Game(str(self.status)))
		return

	async def stop(self, message):
		self.looping = False
