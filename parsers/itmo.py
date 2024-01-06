import json
import time
from typing import override

from concurs import ConcursPlace
from datafetcher import web_requests
from parsers.vuz import VuzRatingList

freaking_api_key = "9e2eee80b266b31c8d65f1dd3992fa26eb8b4c118ca9633550889a8ff2cac429"

class ITMO(VuzRatingList):
	@override
	def discover_links(self, offline=False) -> dict[str, str]:
		progs = "01.03.02 09.03.01 09.03.02 09.03.03 09.03.04 10.05.01 38.03.05 02.03.01 02.03.02".split()
		results = dict()
		for program in progs:

			url = f"https://abitlk.itmo.ru/api/v1/{freaking_api_key}/rating/directions?degree=bachelor&title={program}"

			data = json.loads(web_requests.get(url).text)
			#
			if not data['result']['items']:
				#print(data)
				#print("itmo discover error")
				continue
			prog = data['result']['items'][0]['competitive_group_id']
			link = f"https://abit.itmo.ru/_next/data/AEhS1JbONUKUlFJoZiZEa/ru/rating/bachelor/budget/{prog}.json?degree=bachelor&financing=budget&id={prog}"
			results[program] = link

			if not offline:
				# TODO: why synchronous sleep???
				print('synchronous sleep 10 seconds')
				time.sleep(10)
		return results

	@override
	def parse(self, url) -> list[ConcursPlace]:
		bvis = json.loads(web_requests.get(url).text)['pageProps']["programList"]["without_entry_tests"]

		unusual = json.loads(web_requests.get(url).text)['pageProps']["programList"]["by_unusual_quota"]

		spec = json.loads(web_requests.get(url).text)['pageProps']["programList"]["by_special_quota"]
		target = json.loads(web_requests.get(url).text)['pageProps']["programList"]["by_target_quota"]
		general = json.loads(web_requests.get(url).text)['pageProps']["programList"]["general_competition"]

		result = []
		for x in bvis:
			number = x['position']
			snils = x['snils']
			ball = x['total_scores']
			prior = x['priority']
			orig = x['is_send_original']
			this = ConcursPlace(postition_number=number, snils=snils, bvi=True, score=ball, confirmed=orig, prior=prior)
			result.append(this)
		for x in unusual + spec + target + general:
			number = x['position']
			snils = x['snils']
			ball = x['total_scores']
			prior = x['priority']
			orig = x['is_send_original']
			this = ConcursPlace(postition_number=number, snils=snils, bvi=False, score=ball, confirmed=orig, prior=prior)
			result.append(this)
		return result
