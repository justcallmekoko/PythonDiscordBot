import os
import json
import discord
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class ServerInfo():
	name = '!serverinfo'

	desc = 'Get server information'

	synt = '!serverinfo'

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
		embed = discord.Embed(title="Server Information",
				color=discord.Color.blue())

		embed.add_field(name='Name', value='```' + str(message.guild.name) + '```', inline=True)
		embed.add_field(name='Owner', value='```' + str(message.guild.owner) + '```', inline=True)
		embed.add_field(name='Created', value='```' + str(message.guild.created_at) + '```', inline=True)

#		embed.add_field(name = chr(173), value = chr(173))

		embed.add_field(name='Members', value='```' + str(message.guild.member_count) + '```', inline=True)
		embed.add_field(name='Roles', value='```' + str(len(message.guild.roles)) + '```', inline=True)

		await message.channel.send(embed=embed)
		return

	async def stop(self, message):
		self.looping = False
