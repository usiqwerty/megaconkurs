import asyncio
from typing import override

import pandas
from bs4 import BeautifulSoup as bs

from concurs import ConcursPlace
from datafetcher import web_requests
from parsers.vuz import VuzRatingList


def generate_url():
	year = 2023
	city = 'moscow'
	name = 'Ant_Ist'
	# return f"https://enrol.hse.ru/storage/public_report_{year}/{city}/Bachelors/KS_M_B_OM_M_{name}.xlsx"
	return f"https://enrol.hse.ru/storage/public_report_{year}/{city}/Bachelors/BD_{name}.xlsx"


class HSE(VuzRatingList):
	@override
	def parse(self, url) -> list[ConcursPlace]:
		df = pandas.read_excel(url)  # sheet index starting 0
		empty = False

		table = []
		for index, row in df.iterrows():
			if all(pandas.isna(x) for x in row.values):
				empty = True
			else:
				if empty and pandas.notna(row.values[0]):
					table.append(['' if pandas.isna(x) else x for x in row.values])
		table.pop(0)  # remove header
		stripped = []
		for row in table:
			snils = row[2]
			bvi = row[4] == "Да"
			osoboe = row[6] == 'Да'
			celevoe = row[8] == 'Да'
			otdelnoe = row[10] == "Да"
			prior_cel = row[12]
			prior_other = row[14]
			prior_contract = row[16]
			ball = row[26]
			orig = row[-7]
			if not ball:
				ball = -1
			# print(snils, score, bvi)
			if not (osoboe or celevoe or otdelnoe):
				this = ConcursPlace(snils=snils, score=int(ball), bvi=bvi, prior=prior_other, confirmed=orig)
				# stripped.append([snils, int(score), bvi, prior_other, orig])
				stripped.append(this)

		stripped.sort(key=lambda x: (not x.bvi, -x.score))
		number = 0
		for x in stripped:
			number += 1
			x.position_number = number
		return stripped

	@override
	def discover_links(self, offline=False) -> dict[str, str]:
		r = web_requests.get("https://ba.hse.ru/base2023")  # https://ba.hse.ru/finlist
		data = r.text
		# with open('data.html', 'w', encoding='utf-8') as f:
		#    f.write(data)

		result = dict()

		soup = bs(data, 'html.parser')
		table = soup.find_all('table')[0]

		for row in table.find_all('tr')[1:]:
			cols = row.find_all('td')
			if cols:
				name, link = cols
				link = link.find('a')['href']
				result[name.text] = link

				if cols[1] and cols[1].has_attr('href'):
					link = cols[1]['href']

		return result


async def full_update() -> dict[str, list[ConcursPlace]]:
	dictlinks = discover_links()
	take = [4, 13, 14, 15, 21, 22, 36, 37, 38, 41]
	links = dictlinks.items()  # [list(dictlinks.items())[i] for i in take]
	print(links)
	result = dict()

	for name, link in links:
		result[name] = parse(link)
		print(f"ВШЭ {len(result)}")
		await asyncio.sleep(web_requests.delay)
	return result


if __name__ == "__main__":
	i = 0
# dictlinks=discover_links()
# for name, link in dictlinks.items():
#    print(i, name, link)
#    i+=1
