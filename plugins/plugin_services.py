import os
import json
import discord
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
		embed=discord.Embed(title="Services",
				color=discord.Color.blue())
		response = ''

		for obj in obj_list:
			if obj.is_service:
				response = response + str(obj.name)
				if obj.looping:
					response = response + ': `running`\n'
				else:
					response = response + ': `not running`\n'

		embed.add_field(name='Status', value='```' + str(response) + '```', inline=True)
		await message.channel.send(embed=embed)

		return

	async def stop(self, message):
		self.looping = False
