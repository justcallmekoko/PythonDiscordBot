import os
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.DEBUG)

# Check/Create log dir
if not os.path.exists('log'):
	os.makedirs('log')

# Add a file rotating handler to logger
try:
	handler = RotatingFileHandler('log/discord_bot.log', maxBytes=1000000, backupCount=10)
except:
	handler = RotatingFileHandler('discord_bot.log', maxBytes=1000000, backupCount=10)
	
formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)

logger.debug('Logger started')