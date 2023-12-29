import re
from typing import override

from bs4 import BeautifulSoup as bs

from concurs import ConcursPlace, PAYMENT_BUDGET, PAYMENT_CONTRACT
from datafetcher import web_requests
from parsers.vuz import VuzRatingList


def parse_subjects(line):
	r = re.search(r"(ВИ \d): ([А-я]+) [А-я\W]+", line)
	if not r:
		return
	key, name = r.groups()
	return key, name


def parse_program_code(line):
	r = re.search(r"Направление: ([0-9.]+) [А-я\W]+", line)
	if not r:
		return
	return r.groups()[0]


class SPbU(VuzRatingList):
	@override
	def discover_links(self, offline=False):
		url = "https://cabinet.spbu.ru/Lists/1k_EntryLists/index_comp_groups.html"
		r = web_requests.get(url)
		soup = bs(r.text, 'html.parser')
		name = soup.findChild("h3")

		results = dict()
		while name:
			budg = name.findNext("a")
			contract = name.findNext("a")
			celevaya = name.findNext("a")
			osobaya = name.findNext("a")
			other = name.findNext("a")

			prog = str(name.text.encode('latin1').decode('utf-8'))

			results[prog] = "https://cabinet.spbu.ru/Lists/1k_EntryLists/" + budg['href']
			name = name.findNext("h3")
		return results

	@override
	def parse(self, url):
		data = web_requests.get(url).text.encode('latin1').decode('utf-8')

		soup = bs(data, 'html.parser')
		table = soup.find('table')
		info_block = soup.find("p")

		subjects = self.extract_subjects(info_block)

		program_code = self.extract_program_code(info_block)

		result = []

		if "Госбюджетная" in info_block.text:
			payment_type = PAYMENT_BUDGET
		elif "Договорная" in info_block.text:
			payment_type = PAYMENT_CONTRACT

		for row in table.find_all('tr'):
			cols = row.find_all('td')
			if not cols: continue
			if payment_type == PAYMENT_BUDGET:
				num, snils, concurs_type, prior, rating_score, ball_ege, *ege_scores, ball_dop, dop_name, comment = cols
				confirmed = None
				priority = int(prior.text)
			elif payment_type == PAYMENT_CONTRACT:
				num, snils, concurs_type, rating_score, ball_ege, *ege_scores, ball_dop, contract_signed, dop_name, comment = cols
				confirmed = contract_signed.text.strip() == "Да"
				priority = None
			else:
				raise Exception(f"Unknown payment type at {url}")
			score_values = {}
			for name, value in zip(subjects, ege_scores):
				if value.text.strip():
					score_values[name] = int(float(value.text.split('(')[0]))

			bvi = concurs_type == "Без ВИ"
			balls = int(float(rating_score.text.replace(',', '.'))) if rating_score.text else -1

			result.append(ConcursPlace(postition_number=int(num.text),
			                           snils=snils.text,
			                           score=balls,
			                           bvi=bvi,
			                           prior=priority,
			                           payment=payment_type,
			                           confirmed=confirmed,
			                           subjects=score_values,
			                           code=program_code))

		return result

	def extract_program_code(self, info_block):
		program_code = ""
		for line in info_block.text.split('\n'):
			c = parse_program_code(line)
			if c:
				program_code = c
		return program_code

	def extract_subjects(self, info_block):
		subjects = {}
		for info_line in info_block.find_all("b"):
			if info_line:
				subject = parse_subjects(info_line.text)
				if subject and subject[1] != "Творческий":
					subjects[subject[0]] = subject[1]
		subjects = list(subjects.values())
		return subjects
