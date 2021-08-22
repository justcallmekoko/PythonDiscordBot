import os
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop
from requests import get

RCONIP = os.getenv('RCON_IP')
PASSW = os.getenv('RCON_PASSWORD')

class RemoveUser():
	name = '!clear'

	desc = 'Clear your user from minecraft server whitelist'

	synt = '!clear'

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

		if not found:
			await message.channel.send(message.author.mention + ' There is no linked minecraft username')
			return
		else:
			for line in lines:
				if discord_user in line:
					the_line = line

			minecraft_user = the_line.split(':')[1].replace('\n', '')

			lines.remove(the_line)

			with open('users.txt', 'w') as f:
				f.writelines(lines)

			with MCRcon(RCONIP, PASSW) as mcr:
				resp = mcr.command('whitelist remove ' + str(minecraft_user))
				mcr.disconnect()

			await message.channel.send(message.author.mention + ' Removed user from whitelist: ' + str(minecraft_user))

	async def stop(self, message):
		self.loop = False
