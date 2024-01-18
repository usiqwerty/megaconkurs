class ParsingError(Exception):
	def __init__(self, *args):
		self.msg = ""
		if args:
			self.msg = args[0]

	def __repr__(self):
		return f"Error while parsing{': '+self.msg if self.msg else ''}"
