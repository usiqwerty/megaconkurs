import json
import time
from typing import override

from concurs import ConcursPlace
from datafetcher import web_requests
from parsers.vuz import VuzRatingList


class SPbSTU(VuzRatingList):
	@override
	def discover_links(self, offline=False) -> dict[str, str]:
		results = dict()
		page_count = 8
		for page in range(1, page_count + 1):

			url = f"https://enroll.spbstu.ru/applications-manager/api/v1/directions/all-pageable?name=&educationFormId=2&educationLevelId=2,5&admissionBasis=BUDGET&showClosed=true&page={page}"
			r = web_requests.get(url)
			data = json.loads(r.text)

			if data['totalPages'] != 8:
				print(f"WARNING, update page limit to this value: {data['totalPages'] = }")

			for prog in data['result']:
				prog_id = prog['id']
				name = prog['title']
				link = f"https://enroll.spbstu.ru/applications-manager/api/v1/admission-list/form-rating?applicationEducationLevel=BACHELOR&directionEducationFormId=2&directionId={prog_id}"
				results[name] = link

			if not offline:
				# TODO: why synchronous sleep???
				print('synchronous sleep 10 seconds')
				time.sleep(10)
		return results

	@override
	def parse(self, url):
		data = json.loads(web_requests.get(url).text)

		results = []
		num = 0
		for row in data['list']:
			num += 1
			snils = row['userSnils']
			prior = row['priority']
			bvi = row['withoutExam']
			ball = row['fullScore']
			orig = row['hasOriginalDocuments']

			this = ConcursPlace(postition_number=num, snils=snils, score=ball, bvi=bvi, prior=prior, confirmed=orig)
			results.append(this)
		return results
