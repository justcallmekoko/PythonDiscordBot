from logger import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.DEBUG)

# Add an ECS formatter to the Handler
handler = RotatingFileHandler('/var/log/discord_bot/my_log.log', maxBytes=2000, backupCount=10)
logger.addHandler(handler)

streamhandler = logging.StreamHandler()
logger.addHandler(streamhandler)

logger.debug('Logger started')