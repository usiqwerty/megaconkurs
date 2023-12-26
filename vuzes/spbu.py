from bs4 import BeautifulSoup as bs
from datafetcher import web_requests
from classes import ConcursPlace

def discover_links():
    url="https://cabinet.spbu.ru/Lists/1k_EntryLists/index_comp_groups.html"
    r=web_requests.get(url)
    soup=bs(r.text, 'html.parser')
    name = soup.findChild("h3")

    results=dict()
    while name:

        budg =  name.findNext("a")
        contract = name.findNext("a")
        celevaya = name.findNext("a")
        osobaya = name.findNext("a")
        other = name.findNext("a")

        prog = str(name.text.encode('latin1').decode('utf-8'))

        results [prog] = "https://cabinet.spbu.ru/Lists/1k_EntryLists/" + budg['href']
        name = name.findNext("h3")
    return results

def parse(url):
    data=web_requests.get(url).text.encode('latin1').decode('utf-8')

    soup=bs(data, 'html.parser')
    table=soup.find('table')


    result=[]

    for row in table.find_all('tr'):
        cols=row.find_all('td')
        if not cols: continue
        num,snils,concurs_type,prior,ball,ballege,_,_,_,balldop,dop,comment=cols
        bvi = concurs_type == "Без ВИ"
        this=ConcursPlace(postition_number=int(num.text), snils=snils.text, score=int(float(ball.text.replace(',', '.'))), bvi=bvi, prior=int(prior.text))
        result.append(this)

    return result