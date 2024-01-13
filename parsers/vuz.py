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

from concurs import ConcursPlace


class VuzRatingList:
	def discover_links(self, offline=False) -> dict[str, str]:
		"""Получить ссылки на рейтинги по программам"""
		raise NotImplementedError

	def parse(self, url: str) -> list[ConcursPlace]:
		"""Получить конкурсный список по URL страницы"""
		raise NotImplementedError
