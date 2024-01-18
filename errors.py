class ParsingError(Exception):
	def __init__(self, msg=None):
		self.msg = ""
		if msg:
			self.msg = msg

	def __repr__(self):
		return f"Error while parsing{': '+self.msg if self.msg else ''}"
