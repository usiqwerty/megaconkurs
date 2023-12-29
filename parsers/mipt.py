import asyncio
from typing import override

from bs4 import BeautifulSoup as bs

from concurs import ConcursPlace
from datafetcher import web_requests
from parsers.vuz import VuzRatingList


def generate_url(name):
	# ="Прикладная математика и информатика"
	return f"https://priem.mipt.ru/applications/bachelor_range/Конкурсные списки Общие места ({name}_Бюджет) (HTML).html"


class MIPT(VuzRatingList):
	@override
	def parse(self, url) -> list[ConcursPlace]:
		r = web_requests.get(url)
		data = r.text

		soup = bs(data, 'html.parser')
		table = soup.find('table')

		res = []
		for row in table.find_all('tr'):

			this = []
			for col in row.find_all('td'):
				this.append(col.text)
			# line=[this[0], this[1], this[2]!='', this[3], this[-4],this[-3]]
			this = ConcursPlace(postition_number=int(this[0]),
								snils=this[1],
								bvi=this[2] != '',
								score=this[3],
								confirmed=this[-4] == "Оригинал",
								prior=int(this[-3])
								)
			res.append(this)
		return res

	@override
	def discover_links(self, offline=False) -> dict[str, str]:
		a = ['Прикладная математика и информатика', "Радиотехника и компьютерные технологии",
			 "Компьютерные технологии (ПМФ)", 'ПИШ РПИ Программная инженерия',
			 'Системное программирование и прикладная математика', 'Компьютерные технологии (ИВТ)',
			 'ВШПИ Программная инженерия', 'Компьютерная безопасность']

		links = dict()
		for x in a:
			links[x] = generate_url(x)
		return links


async def full_update():
	links = discover_links()
	result = dict()
	for name, link in links:
		url = link
		result[name] = parse(url)
		print(f"МФТИ {len(result)}")
		await asyncio.sleep(web_requests.delay)

	return result


if __name__ == "__main__":
	a = ['Прикладная математика и информатика', "Радиотехника и компьютерные технологии",
		 "Компьютерные технологии (ПМФ)", 'ПИШ РПИ Программная инженерия',
		 'Системное программирование и прикладная математика', 'Компьютерные технологии (ИВТ)',
		 'ВШПИ Программная инженерия', 'Компьютерная безопасность']
	for x in a:
		print(generate_url(x))
