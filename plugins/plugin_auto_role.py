import os
import json
from datetime import datetime
from dotenv import load_dotenv
from discord.ext.tasks import loop
from discord.utils import get
from requests import get

class AutoRole():
	name = '!autorole'

	desc = 'Apply roles automatically based on time spent'

	synt = '!autorole [start|stop]'

	looping = False

	group = 'Moderator'

	admin = True
	
	cheer = -1
	
	cat = 'admin'

	global_message = None

	days_to_role = [[365, 'One Year'],
			[180, '6 Months']]

	@loop(seconds = 3600)
	async def loop_func(self):
		if self.looping:
			print('Running auto role check...')
			for member in self.global_message.guild.members:
				if not self.looping:
					print('Exiting from auto role check...')
					self.loop_func.stop()
					return
				mem_join = member.joined_at
				now = datetime.now()
				#print(str(mem_join) + ' - ' + str(now))
				join_days = (now - mem_join).days

				for role_index in self.days_to_role:
					if int(join_days) >= int(role_index[0]):
						the_role = None
						for role in self.global_message.guild.roles:
							if role.name == str(role_index[1]):
								the_role = role
								#print('Found the role: ' + str(the_role.name))
								break
						if the_role == None:
							continue

						if the_role in member.roles:
							continue

#						role = get(self.global_message.guild.roles, name = str(role_index[1]))
						await member.add_roles(the_role)
						print('Gave \'' + str(role_index[1]) + '\' to ' + member.name)

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
		self.global_message = message
		cmd = message.content
		if len(cmd.split(' ')) > 1:
			arg = cmd.split(' ')[1]
		else:
			arg = None

		if cmd == '!autorole':
			if self.looping:
				await message.channel.send(message.author.mention + ' autorole is running')
			else:
				await message.channel.send(message.author.mention + ' autorole is not running')
		if arg == None:
			return

		if str(arg) == 'start':
			if not self.looping:
				self.looping = True
				await message.channel.send(message.author.mention + ' Starting autorole')
				self.loop_func.start()

		if str(arg) == 'stop':
			if self.looping:
				self.looping = False
				await message.channel.send(message.author.mention + ' Stopping autorole')
				self.loop_func.stop()
		return

	async def stop(self, message):
		self.looping = False
