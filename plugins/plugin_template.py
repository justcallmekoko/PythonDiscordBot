import os
import json
from dotenv import load_dotenv
from discord.ext.tasks import loop
from requests import get

class Template():
	conf_path = os.path.join(os.path.dirname(__file__), 'configs')

	name = '!template'

	desc = 'This does nothing. Developer only'

	synt = '!template'

	is_service = False

	client = None

	looping = False

	# Server configurable

	group = 'Owner'

	admin = False
	
	cheer = -1
	
	cat = 'admin'
	
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
		return True

	async def stop(self, message):
		self.looping = False
