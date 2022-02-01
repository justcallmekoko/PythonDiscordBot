import os
import json
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Joined():
	name = '!joined'

	desc = 'Get the date when a member joined the server'

	synt = '!joined <user>'

	loop = False

	group = 'Moderator'

	admin = True
	
	cheer = -1
	
	cat = 'admin'
	
	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False
	
	async def runCheer(self, user, amount):
		return

	async def run(self, message):
		target_user = str(message.content).split(' ')[1]

		# Search for the user
		found = False

		for member in message.guild.members:
			if str(member.name) == target_user:
				found = True
				real_member = member
				break

		# Did not find the user
		if not found:
			await message.channel.send(message.author.mention + ', The user was not found')
		# Found the user
		else:
			mem_join = real_member.joined_at
			now = datetime.now()
			print(str(mem_join) + ' - ' + str(now))
			join_days = (now - mem_join).days
			await message.channel.send(message.author.mention + ', ' + real_member.mention + ' joined ' + str(join_days) + ' day(s) ago')

		return

	async def stop(self, message):
		self.loop = False
