from bs4 import BeautifulSoup as bs
from datafetcher import web_requests
from concurs import ConcursPlace, PAYMENT_BUDGET, PAYMENT_CONTRACT
from typing import override
from parsers.vuz import VuzRatingList
import re


def parse_subjects(line):
    r=re.search(r"(ВИ \d): ([А-я]+) [А-я\W]+", line)
    if not r:
        return
    key, name = r.groups()
    return key, name
def parse_program_code(line):
    r=re.search(r"Направление: ([0-9.]+) [А-я\W]+", line)
    if not r:
        return
    return r.groups()[0]

class SPbU(VuzRatingList):
    @override
    def discover_links(self, offline=False):
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

    @override
    def parse(self, url):
        data=web_requests.get(url).text.encode('latin1').decode('utf-8')

        soup=bs(data, 'html.parser')
        table=soup.find('table')

        info_block = soup.find("p")

        if "Госбюджетная" in info_block.text:
            payment_type=PAYMENT_BUDGET
        elif "Договорная" in info_block.text:
            payment_type=PAYMENT_CONTRACT
        subjects={}
        program_code = ""
        for info_line in info_block.find_all("b"):
            if info_line:
                r = parse_subjects(info_line.text)
                if r and r[1]!="Творческий":
                    subjects[r[0]]=r[1]
        for line in info_block.text.split('\n'):
            c = parse_program_code(line)
            if c:
                program_code = c
        subjects=list(subjects.values())
        result=[]

        for row in table.find_all('tr'):
            cols=row.find_all('td')
            if not cols: continue
            if payment_type == PAYMENT_BUDGET:
                num, snils, concurs_type, prior, ball, ballege, *ege_scores, balldop, dop, comment = cols
                score_values={}
                for name, value in zip(subjects, ege_scores):
                    if value.text.strip():
                        score_values[name]= int(float(value.text.split('(')[0]))
                bvi = concurs_type == "Без ВИ"
                balls = int(float(ball.text.replace(',', '.'))) if ball.text else -1
                this = ConcursPlace(postition_number=int(num.text), snils=snils.text, score=balls, bvi=bvi,
                                    prior=int(prior.text), payment=payment_type, subjects=score_values, code=program_code)
            elif payment_type == PAYMENT_CONTRACT:
                num, snils, concurs_type, ball, ballege, *ege_scores, balldop, contract_signed, dop, comment = cols
                score_values = {}
                for name, value in zip(subjects, ege_scores):
                    if value.text.strip():
                        score_values[name] = int(float(value.text.split('(')[0]))
                bvi = concurs_type == "Без ВИ"
                confirmed = contract_signed.text.strip() == "Да"
                balls = int(float(ball.text.replace(',', '.'))) if ball.text else -1
                this = ConcursPlace(postition_number=int(num.text), snils=snils.text, score=balls, bvi=bvi,
                                    payment=payment_type, confirmed=confirmed, subjects=score_values, code=program_code)
            result.append(this)

        return result