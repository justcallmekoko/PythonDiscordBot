class plugin():
	name = None
	desc = None
	synt = None

	def __init__(self, name, desc, synt):
		self.name = name
		self.desc = desc
		self.synt = synt

class Guild():
	channels = []

	def __init__(self):
		a_channel = channel()
		self.channels.append(a_channel)

class Role():
	name = None

	def __init__(self, name):
		self.name = name

class User():
	roles = []
	mention = None
	name = None

	def __init__(self, roles, name):
		self.roles = roles
		self.mention = name + '#0000'
		self.name = name

class message():
	reactions = []
	id = None
	content = None
	channel = None
	embed = None
	author = None
	guild = None

	def __init__(self, content, channel):
		id = 0
		role = Role('member')
		user = User([role], 'user')
		guild = Guild()
		self.guild = guild
		self.author = user
		self.content = content
		self.channel = channel
		channel = None

class channel():
	name = None

	def __init__(self):
		self.name = "Channel"
		return

	async def send(self, content=None, embed=None):
		a_message = message('potato', self)
		return a_message

	async def fetch_message(self, message_id):
		a_message = message('potato', self)
		return a_message