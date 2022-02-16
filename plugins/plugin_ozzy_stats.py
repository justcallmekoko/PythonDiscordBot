import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class OzzyStats():
	name = '!ozzystats'

	desc = 'Check how many times Ozzy was pet'

	synt = '!ozzystats'

	looping = False

	group = 'members'

	admin = False
	
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
		# Create fresh stat file
		if not os.path.isfile('ozzystats.json'):
			# Create fresh json template
			data = {}
			data['name'] = 'Ozzy'
			data['pets'] = 0
			data['members'] = []
			with open('ozzystats.json', 'w') as f:
				json.dump(data, f)

		# Get json data
		f = open('ozzystats.json',)

		json_data = json.load(f)

		f.close()

		await message.channel.send(message.author.mention + ', Ozzy has been pet ' + str(json_data['pets']) + ' time(s)')

	async def stop(self, message):
		self.looping = False
