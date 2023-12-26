from datafetcher import web_requests
from bs4 import BeautifulSoup as bs
import json
from classes import ConcursPlace
import time
def discover_links(progs, offline=False):

    results=dict()
    for name in progs:
        freaking_api_key="9e2eee80b266b31c8d65f1dd3992fa26eb8b4c118ca9633550889a8ff2cac429"
        url=f"https://abitlk.itmo.ru/api/v1/{freaking_api_key}/rating/directions?degree=bachelor&title={name}"

        data=json.loads(web_requests.get(url).text)
        if not data['result']['items']:
            print("itmo discover error")
            continue
        prog=data['result']['items'][0]['competitive_group_id']
        #link=f'https://abit.itmo.ru/rating/bachelor/budget/{prog}'
        link=f"https://abit.itmo.ru/_next/data/AEhS1JbONUKUlFJoZiZEa/ru/rating/bachelor/budget/{prog}.json?degree=bachelor&financing=budget&id={prog}"
        results[name]=link

        if not offline:
            # TODO: why synchronous sleep???
            print('synchronous sleep 10 seconds')
            time.sleep(10)
    return results
def parse(url):
    #url="https://abit.itmo.ru/_next/data/AEhS1JbONUKUlFJoZiZEa/ru/rating/bachelor/budget/1801.json?degree=bachelor&financing=budget&id=1801"
    bvis=json.loads(web_requests.get(url).text)['pageProps']["programList"]["without_entry_tests"]

    unusual= json.loads(web_requests.get(url).text)['pageProps']["programList"]["by_unusual_quota"]

    spec = json.loads(web_requests.get(url).text)['pageProps']["programList"]["by_special_quota"]
    target = json.loads(web_requests.get(url).text)['pageProps']["programList"]["by_target_quota"]
    general = json.loads(web_requests.get(url).text)['pageProps']["programList"]["general_competition"]

    result=[]
    for x in bvis:
        number=x['position']
        snils=x['snils']
        ball=x['total_scores']
        prior=x['priority']
        orig=x['is_send_original']
        this = ConcursPlace(number=number, snils=snils, bvi=True, ball=ball,attestat=orig, prior=prior)
        result.append(this)
    for x in unusual+spec+target+general:
        number=x['position']
        snils=x['snils']
        ball=x['total_scores']
        prior=x['priority']
        orig=x['is_send_original']
        this = ConcursPlace(number=number, snils=snils, bvi=False, ball=ball,attestat=orig, prior=prior)
        result.append(this)
    return result
    """soup= bs(data, 'html.parser')
    rows= list(filter(  lambda x: x.get('class') and "RatingPage_table__item" in x['class'][0], soup.find_all("div")  ))
    for row in rows:
        a, b = row.children
        #print(a.text)
        num, snils, *_ = a.text.split()
        snils=snils[1:12]
        print(num, snils)"""
