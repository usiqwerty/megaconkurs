import requests
import os
import json
from classes import FakeResponse

headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
#'Referer': 'https://enroll.spbstu.ru/'
}
delay = 30 #seconds
cache: dict[str, FakeResponse] = dict()
filemap: dict[str, str] = dict()  # url -> filename

def add_cache_file_in_index(url: str) -> str:
    filename=f"{len(cache)+1}.cache"
    filemap[url]=filename
    return filename

def get(url: str, force=False, do_not_update=False) -> FakeResponse:
    "Выполняет запрос GET с сохранением в кэш"
    if (not do_not_update) and (url not in cache or force):
        print(f"[WEB] {url}")
        cache[url] = FakeResponse(requests.get(url, headers=headers).text)
        add_cache_file_in_index(url)
    return cache[url]


def load_cache_from_disk():
    global filemap
    with open(os.sep.join(['cache', 'map.json']), encoding='utf-8') as f:
        print('Loading mapping...')
        filemap = json.load(f)
    for url in filemap:
        fn=filemap[url]
        with open(os.sep.join(['cache', fn]), encoding='utf-8') as f:
            print(fn)
            cache[url] = FakeResponse(f.read())  #  f.read()

def save_cache_to_disk():
    with open(os.sep.join(['cache', 'map.json']), 'w', encoding='utf-8') as f:
        print('Saving mapping...')
        json.dump(filemap, f)
    for url in filemap:
        fn=filemap[url]

        with open(os.sep.join(['cache', fn]), 'w', encoding='utf-8') as f:
            if cache[url]:
                print(f'Saving {fn}')
                f.write(cache[url].text)