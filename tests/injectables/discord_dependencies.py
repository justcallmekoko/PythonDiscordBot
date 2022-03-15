class plugin():
	name = None
	desc = None
	synt = None

	def __init__(self, name, desc, synt):
		self.name = name
		self.desc = desc
		self.synt = synt

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
	content = None
	channel = None
	embed = None
	author = None

	def __init__(self, content, channel):
		role = Role('member')
		user = User([role], 'user')
		self.author = user
		self.content = content
		self.channel = channel
		channel = None

class channel():
	def __init__(self):
		return

	async def send(self, content=None, embed=None):
		return True