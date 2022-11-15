import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.DEBUG)

# Add an ECS formatter to the Handler
handler = RotatingFileHandler('/var/log/discord_bot/discord_bot.log', maxBytes=20000, backupCount=10)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)

logger.debug('Logger started')