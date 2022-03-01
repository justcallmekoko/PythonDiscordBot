import os
import json
import discord
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
#		response = message.author.mention + '\n'
		embed = discord.Embed(title="Help",
				color=discord.Color.blue())

		if str(message.content) == '!help':
			for obj in obj_list:
				embed.add_field(name=str(obj.name), value='`' + str(obj.desc) + '`', inline=False)
#				embed.add_field(name="Description", value='`' + str(obj.desc) + '`', inline=True)
#				embed.add_field(name = chr(173), value = chr(173))
#				response = response + str(obj.name) + '\t- ' + str(obj.desc) + '\n'

			await message.channel.send(embed=embed)
		elif '!help ' in str(message.content):
			for obj in obj_list:
				if str(message.content).split(' ')[1] == str(obj.name):
					embed.add_field(name="Command", value='`' + str(obj.name) + '`', inline=True)
					embed.add_field(name="Description", value='`' + str(obj.synt) + '`', inline=True)
#					response = response + str(obj.synt)
			await message.channel.send(embed=embed)

		return

	async def stop(self, message):
		self.looping = False
