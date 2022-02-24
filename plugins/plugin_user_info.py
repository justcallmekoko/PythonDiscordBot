import os
import json
import discord
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class UserInfo():
	name = '!userinfo'

	desc = 'Get information regarding discord user'

	synt = '!userinfo <user>'

	looping = False

	group = 'Moderator'

	admin = True
	
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
		# Found the user
		else:
			embed=discord.Embed(title="User Info",
					color=discord.Color.blue())

			member_roles = []
			member_perms = ''
			mem_join = real_member.joined_at
			now = datetime.now()
			print(str(mem_join) + ' - ' + str(now))
			join_days = (now - mem_join).days
			for role in real_member.roles:
				member_roles.append(role.name)
			for perm in real_member.permissions_in(message.channel):
				if perm[1]:
					member_perms = member_perms + str(perm[0]) + '\n'
#			await message.channel.send(message.author.mention + ', ' + real_member.mention + ' joined ' + str(join_days) + ' day(s) ago')
			embed.add_field(name="Username", value='`' + str(real_member.name) + '#' + str(real_member.discriminator) + '`', inline=True)
			embed.add_field(name="User ID", value='`' + str(real_member.id) + '`', inline=True)
			embed.add_field(name="Nickname", value='`' + str(real_member.display_name) + '`', inline=True)

			embed.add_field(name="Created", value='```' + str(real_member.created_at) + '```', inline=False)

			embed.add_field(name="Joined", value='```' + str(mem_join) + '```', inline=True)
			embed.add_field(name="Days on server", value='```' + str(join_days) + '```', inline=True)

			embed.add_field(name="Roles", value='```' + str(member_roles) + '```', inline=False)

			embed.add_field(name="Permissions in this channel", value='```' + str(member_perms) + '```', inline=False)

			await message.channel.send(embed=embed)

		return

	async def stop(self, message):
		self.looping = False
