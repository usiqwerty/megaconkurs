"""
	This file is part of megaconcurs.

	megaconcurs is free software: you can redistribute it and/or modify it under the terms of the
	GNU General Public License as published by the Free Software Foundation, either version 2 of the License,
	or (at your option) any later version.

	megaconcurs is distributed in the hope that it will be useful, but WITHOUT ANY
	WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
	General Public License for more details.

	You should have received a copy of the GNU General Public License along with
	Foobar. If not, see <https://www.gnu.org/licenses/>.
"""

DEGREE_BACHELOR = 1
DEGREE_MASTER = 2

PAYMENT_BUDGET = 1
PAYMENT_CONTRACT = 2
PAYMENT_TARGETED = 3


class ConcursPlace:
	"""
	Позиция в конкурсном списке
	"""
	position_number: int
	snils: int
	bvi: bool
	prior: int
	confirmed: bool
	score: int
	subjects: dict[str, int]
	degree: int
	code: str

	def __init__(self, snils: str = None, postition_number: int = None, bvi: bool = None, prior: int = None,
	             confirmed: bool = None, score: int = None, degree: int = None,
	             payment: int = PAYMENT_BUDGET, subjects: dict[str, int] = None, code: str = None):
		"""
		@param code:
		@param snils: СНИЛС абитуриента (будет преобразован из строки в число)
		@param postition_number: Позиция в рейтинге
		@param bvi: Поступает БВИ
		@param prior: Приоритет
		@param confirmed: Отдан оригинал аттестата или заключён договор
		@param score: Сумма баллов при поступлении
		@param degree: Уровень поступления
		@param payment: Форма оплаты обучения
		@param subjects:
		"""
		self.position_number = postition_number
		self.snils = int((snils or "0").replace(' ', '').replace('-', '')) or None
		self.bvi = bvi
		self.prior = prior
		self.confirmed = confirmed
		self.score = score
		self.degree = degree
		self.payment = payment
		self.subjects = subjects
		self.code = code

	def __repr__(self):
		return f"{self.position_number}@{self.code}: {self.snils} ({self.score}) p{self.prior} {'БВИ' if self.bvi else ''} {'ОРИГ' if self.confirmed else ''} {self.subjects}"
