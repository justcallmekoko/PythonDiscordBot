import os
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

	loop = False

	group = 'Twitch Subscriber'

	admin = False
	
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
			await message.channel.send(message.author.mention + ' Added user to whitelist: ' + str(minecraft_user))

	async def stop(self, message):
		self.loop = False
