import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class MontyStats():
	name = '!montystats'

	desc = 'Check how many times Monty was pet'

	synt = '!montystats'

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
		return True

	async def run(self, message, obj_list):
		# Create fresh stat file
		if not os.path.isfile('montystats.json'):
			# Create fresh json template
			data = {}
			data['name'] = 'Monty'
			data['pets'] = 0
			data['members'] = []
			with open('montystats.json', 'w') as f:
				json.dump(data, f)

		# Get json data
		f = open('montystats.json',)

		json_data = json.load(f)

		f.close()

		await message.channel.send(message.author.mention + ', Monty has been pet ' + str(json_data['pets']) + ' time(s)')

		return True
	async def stop(self, message):
		self.looping = False
