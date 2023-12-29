from concurs import ConcursPlace


class VuzRatingList:
	def discover_links(self, offline=False) -> dict[str, str]:
		"""Получить ссылки на рейтинги по программам"""
		raise NotImplementedError

	def parse(self, url: str) -> list[ConcursPlace]:
		"""Получить конкурсный список по URL страницы"""
		raise NotImplementedError
