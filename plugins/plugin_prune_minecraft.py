import os
from dotenv import load_dotenv
from mcrcon import MCRcon
from discord.ext.tasks import loop
from requests import get

RCONIP = os.getenv('RCON_IP')
PASSW = os.getenv('RCON_PASSWORD')

class PruneMinecraft():
	name = '!pruneminecraft'

	desc = 'Keep list of permitted minecraft users up to date'

	synt = '!pruneminecraft [start|stop]'

	looping = False

	group = 'Moderator'

	admin = False
	
	cheer = -1
	
	cat = 'admin'

	groups = ['Twitch Subscriber',
                '3 Months',
                '6 Months',
                'One Year',
                'Server Booster',
                'Moderator']

	blacklist = ['Restricted']

	global_message = None
	
	def checkCat(self, check_cat):
		if self.cat == check_cat:
			return True
		else:
			return False
	
	def checkBits(self, bits):
		return False
	
	async def runCheer(self, user, amount):
		return

	@loop(seconds = 5)
	async def loop_func(self):
#		print ('Running pruneminecraft...')
		if not self.looping:
			return

		message = self.global_message

		discord_user = str(message.author)
		if not os.path.isfile('users.txt'):
			with open('users.txt', 'w') as f:
				f.close()

		with open('users.txt', 'r') as f:
			lines = f.readlines()

		for line in lines:
			target_user = str(line).split(':')[0]

			found = False

			# Found user in server
			for member in message.guild.members:
				if str(target_user).split('#')[0] == str(member.name):
					found = True
					target_user = member
					break

			if not found:
				continue

#			print ('Running for ' + str(target_user))


			do_remove = False
			role_found = False

			for role in target_user.roles:
				if str(role.name) in self.blacklist:
#					print('Found blacklisted role')
					do_remove = True
					break
				if str(role.name) in self.groups:
					role_found = True

			if not role_found:
				do_remove = True

			if not do_remove:
				continue
			else:
				the_line = line

				minecraft_user = the_line.split(':')[1].replace('\n', '')

				lines.remove(the_line)

				with open('users.txt', 'w') as f:
					f.writelines(lines)

				with MCRcon(RCONIP, PASSW) as mcr:
					resp = mcr.command('whitelist remove ' + str(minecraft_user))
					mcr.disconnect()

				print('Removed user from whitelist: ' + str(the_line))

	async def run(self, message):
		self.global_message = message
		cmd = message.content
		if len(cmd.split(' ')) > 1:
			arg = cmd.split(' ')[1]
		else:
			arg = None

		if cmd == self.name:
			if self.looping:
				await message.channel.send(message.author.mention + ' ' + str(self.name) + ' is running')
			else:
				await message.channel.send(message.author.mention + ' ' + str(self.name) + ' is not running')
		if arg == None:
			return

		if str(arg) == 'start':
			if not self.looping:
				self.looping = True
				await message.channel.send(message.author.mention + ' Starting ' + str(self.name))
				self.loop_func.start()

		if str(arg) == 'stop':
			if self.looping:
				self.looping = False
				await message.channel.send(message.author.mention + ' Stopping ' + str(self.name))
				self.loop_func.stop()
		return

	async def stop(self, message):
		self.looping = False
