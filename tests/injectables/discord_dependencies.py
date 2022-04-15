from datetime import datetime

class plugin():
	name = None
	desc = None
	synt = None

	def __init__(self, name, desc, synt):
		self.name = name
		self.desc = desc
		self.synt = synt

class Guild():
	name = None
	id = None
	channels = []
	roles = []
	members = []
	member_count = 0

	def __init__(self):
		a_channel = channel()
		self.channels.append(a_channel)
		self.name = 'Guild'
		self.id = 0

class Permissions():
	administrator = None

	def __init__(self, admin):
		self.administrator = admin

class Role():
	name = None
	permissions = None

	def __init__(self, name):
		permissions = Permissions(True)
		self.permissions = permissions
		self.name = name

class User():
	roles = []
	mention = None
	name = None

	def __init__(self, roles, name):
		self.roles = roles
		self.mention = name + '#0000'
		self.name = name

	def __str__(self):
		return self.mention

class Reaction():
	count = 0
	emoji = None

	def __init__(self, emoji):
		self.emoji = emoji
		self.count = self.count + 1

class message():
	reactions = []
	id = None
	content = None
	channel = None
	embed = None
	author = None
	guild = None
	created_at = None

	def __init__(self, content, channel):
		id = 0
		role = Role('member')
		user = User([role], 'user')
		guild = Guild()
		self.guild = guild
		self.author = user
		self.content = content
		self.channel = channel
		self.created_at = datetime.now()
		channel = None

	async def add_reaction(self, reaction):
		self.reactions.append(reaction)

	async def edit(self, embed=None):
		self.embed = embed

class channel():
	name = None
	mention = None

	def __init__(self):
		self.name = "Channel"
		self.mention = '<#0>'
		return

	async def send(self, content=None, embed=None):
		a_message = message('potato', self)
		return a_message

	async def fetch_message(self, message_id):
		a_message = message('potato', self)
		return a_message