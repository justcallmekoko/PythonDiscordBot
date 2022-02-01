import os
import json
import random
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class SearchAndDestroy():
	name = '!searchanddestroy'

	desc = 'Plant the bomb. The server will have to defuse it.'

	synt = '''`!searchanddestroy [bombplant|bombdefuse <code>]`

The bomb defusal code is randomly generated once it's planted.
The code is only 4 digits long, the digits can repeat themselves,
and it will only contain integers.
If you guess the correct number in the correct index, you will receive an 'X'.
If you guess the correct number in the incorrect index, you will receive an 'O'.
For example, the code is 1234 but you guess 1235.
You would receive an 'XXX'.
If you guess 1243, you would receive an 'XXOO'.

Get the number of guess you have left by typing `!searchanddestroy`'''

	loop = False

	group = 'members'

	admin = False
	
	cheer = -1
	
	cat = 'admin'

	announcements = 'bot-announcements'

	planted = False

	defuse_code = ''
	
	remaining_guesses = 10

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
		announcements_channel = None

		# Find where the bot will be posting its announcements
		for channel in message.guild.channels:
			if str(channel.name) == self.announcements:
				announcements_channel = channel

		cmd = str(message.content)
		seg = cmd.split(' ')

		# Check input syntax
		if len(seg) < 1:
			await message.channel.send(message.author.mention + '`' + str(message.content) + '` is not the proper syntax')
			return

		# Show status of the bomb
		if message.content == self.name:
			if self.planted:
				await message.channel.send(message.author.mention + ' A bomb has been planted. Locate and defuse it. Remaining guesses: ' + str(self.remaining_guesses))
			else:
				await message.channel.send(message.author.mention + ' There are no bombs planted.')
			return

		command = seg[1]

		# Plant the bomb
		if command == 'bombplant':
			if self.planted:
				await message.channel.send(message.author.mention + ' A bomb has *already* been planted')
				return

			self.remaining_guesses = 10
			self.defuse_code = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))

			if announcements_channel != None:
				await announcements_channel.send('@everyone, ' + message.author.mention + ' has planted the bomb')

			await message.channel.send(message.author.mention + ' has planted the bomb')

			self.planted = True

			print(self.defuse_code)

		# Defuse the bomb
		if command == 'bombdefuse':
			if not self.planted:
				return

			xs = 0
			oss = 0
			code_guess = seg[2]

			code_guess_list = list(code_guess)
			defuse_code_list = list(self.defuse_code)

			# User did not send numeric code
			if not code_guess.isnumeric():
				await message.channel.send(message.author.mention + ' The code may only contain numbers.')

			# Bomb has been defused
			if str(code_guess) == str(self.defuse_code):
				if announcements_channel != None:
					await announcements_channel.send('@everyone, ' + message.author.mention + ' has defused the bomb!')

				await message.channel.send(message.author.mention + ' has defused the bomb!')
				self.planted = False
				self.defuse_code = ''
				self.remaining_guesses = 10
				return

			for i in range(0, 4):
				# Correct integer, correct index
				if code_guess_list[i] == defuse_code_list[i]:
					xs = xs + 1
					code_guess_list[i] = "-1"
					defuse_code_list[i] = "-1"

			try:
				while True:
					code_guess_list.remove('-1')
			except ValueError:
				pass

			try:
				while True:
					defuse_code_list.remove('-1')
			except ValueError:
				pass

			print('Comparing: ' + str(code_guess_list) + ' | ' + str(defuse_code_list))

			for i in range(0, len(defuse_code_list)):
				# Correct integer, incorrect index
				try:
					if code_guess_list[i] in defuse_code_list:
						oss = oss + 1
						defuse_code_list.remove(code_guess_list[i])
						code_guess_list[i] = '-1'
				except:
					fuck = True

			self.remaining_guesses = self.remaining_guesses - 1

			if self.remaining_guesses <= 0:
				if announcements_channel != None:
					await announcements_channel.send('@everyone, ' + message.author.mention + ' You are out of guesses. The bomb has detonated!')

				await message.channel.send(message.author.mention + ' You are out of guesses. The bomb has detonated!')
				self.planted = False
				return

			response_string = ('X' * xs) + ('O' * oss) + ' remaining attempts: ' + str(self.remaining_guesses)

			await message.channel.send(message.author.mention + ' ' + str(response_string))

		return

	async def stop(self, message):
		self.loop = False
