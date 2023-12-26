class ConcursPlace:
	"""
	Позиция в конкурсном списке
	"""
	position_number: int
	snils: str
	bvi: bool
	prior: int
	attestat: bool
	score: int
	subjects: dict[str, int]

	def __init__(self, snils=None, postition_number=None, bvi=None, prior=None, attestat=None, score=None):
		self.position_number = postition_number
		self.snils = snils
		self.bvi = bvi
		self.prior = prior
		self.attestat = attestat
		self.score = score

		self.subjects = dict()

	def __repr__(self):
		return f"{self.position_number}: {self.snils} ({self.score}) p{self.prior} {'БВИ' if self.bvi else ''} {'ОРИГ' if self.attestat else ''}"


class FakeResponse:
	"Имитирует response от модуля requests"
	text: str

	def __init__(self, text):
		self.text = text
