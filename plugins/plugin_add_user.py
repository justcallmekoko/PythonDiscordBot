import os
import discord
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop
from requests import get

RCONIP = os.getenv('RCON_IP')
PASSW = os.getenv('RCON_PASSWORD')

class AddUser():
	name = '!add'

	desc = 'Add user to minecraft server whitelist'

	synt = '!add <minecraft username>'

	looping = False

	group = 'members'

	admin = False
	
	cheer = -1
	
	cat = 'admin'

	is_service = False

#	groups = ['People who pooped their pants']
	groups = [
		'Twitch Subscriber',
		'3 Months',
		'6 Months',
		'One Year',
		'Server Booster',
		'Moderator']

	blacklisted = ['Restricted']
	
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
		# Check if user can run this command
		for role in message.author.roles:
			if str(role.name) in self.blacklisted:
				await message.channel.send(message.author.mention + ', Users with the role, `' + str(role.name) + '` are not permitted to run this command')
				return

		role_found = False
		for role in message.author.roles:
			if str(role.name) in self.groups:
				role_found = True
				break

		if not role_found:
			await message.channel.send(message.author.mention + ', Users require one of these roles to run this command.\n`' + str(self.groups) + '`')
			return

		discord_user = str(message.author)
		if not os.path.isfile('users.txt'):
			with open('users.txt', 'w') as f:
				f.close()

		with open('users.txt', 'r') as f:
			lines = f.readlines()

		found = False

		for line in lines:
			if discord_user == line.split(':')[0]:
				found = True
				break

		if found:
			await message.channel.send(message.author.mention + ' There is already a linked minecraft username')
			return
		else:
			minecraft_user = str(message.content).split(' ')[1]
			combo = discord_user + ':' + minecraft_user
			with MCRcon(RCONIP, PASSW) as mcr:
				resp = mcr.command('whitelist add ' + str(minecraft_user))
				mcr.disconnect()

			with open('users.txt', 'a') as f:
				f.write(combo + '\n')
#			await message.channel.send(message.author.mention + ' Added user to whitelist: ' + str(minecraft_user))
			embed=discord.Embed(title="Minecraft Whitelist",
					color=discord.Color.green())

			embed.add_field(name="Discord Username", value='`' + str(discord_user) + '`', inline=True)
			embed.add_field(name="Minecraft Username", value='`' + str(minecraft_user) + '`', inline=True)

			await message.channel.send(embed=embed)

	async def stop(self, message):
		self.loop = False
